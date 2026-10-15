"""Generate C0-C5 evidence conditions for each pilot case. Deterministic; no API calls.

C1r (repeats of C1) is a run-time repeat, not a separate input, so it is not generated here.
"""
import argparse
import json
import random
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES_PATH = ROOT / "data" / "pilot_cases.json"
JSONL_PATH = ROOT / "data" / "pilot_conditions.jsonl"
REVIEW_PATH = ROOT / "data" / "pilot_conditions_review.md"

SEED = 590
CONDITIONS = ["C0", "C1", "C2", "C3", "C4", "C5"]
DOC_NAMES = ["d1", "d2", "d3"]


def replace_ci(text, old, new):
    """Case-insensitive replace of every occurrence of `old` (literal) by `new`."""
    return re.sub(re.escape(old), lambda _: new, text, flags=re.IGNORECASE)


def matched_form(case):
    """The form of the answer to replace in the target sentence, as written there.

    Prefer the case's own `answer` string (so the counterfactual replaces exactly what the answer covers, e.g. "206"
    and not "206 bones"); otherwise fall back to the longest accepted form found in the sentence.
    """
    target = case["d1"][case["target_index"]]
    forms = sorted({case["answer"], *case["accepted_answers"]}, key=lambda f: (-len(f), f))
    form = case["answer"] if case["answer"].lower() in target.lower() else next(
        f for f in forms if f.lower() in target.lower())
    return re.search(re.escape(form), target, flags=re.IGNORECASE).group(0)


def unrelated_index(case):
    return next(i for i in range(len(case["d1"])) if i not in (0, case["target_index"]))


def assign_d1_positions(cases):
    """Counterbalance D1 position (1, 2, 3) across cases; which case gets which is seeded.

    Positions cycle 1,2,3 to length N (each appears N/3 times; counts differ by at most 1 when
    N is not divisible by 3), then are shuffled with the fixed seed and assigned in file order.
    """
    positions = [i % 3 + 1 for i in range(len(cases))]
    random.Random(f"{SEED}:d1_position").shuffle(positions)
    return {c["case_id"]: p for c, p in zip(cases, positions)}


def doc_order(case, d1_position):
    """D1 at its assigned position; the two distractors fill the other slots in seeded order.

    Computed once per case and reused by every condition.
    """
    others = ["d2", "d3"]
    random.Random(f"{SEED}:{case['case_id']}").shuffle(others)
    order = others[:d1_position - 1] + ["d1"] + others[d1_position - 1:]
    return order


def d1_variants(case):
    """Return {condition: (clean D1 text or None, marked D1 text or None, change dict or None)}."""
    s, t, u = list(case["d1"]), case["target_index"], unrelated_index(case)
    out = {"C1": (" ".join(s), " ".join(s), None)}

    # C2: D1 removed
    out["C2"] = (None, "~~" + " ".join(s) + "~~", {"kind": "remove_d1"})

    # C3: target sentence deleted
    clean = [x for i, x in enumerate(s) if i != t]
    marked = [f"~~{x}~~" if i == t else x for i, x in enumerate(s)]
    out["C3"] = (" ".join(clean), " ".join(marked), {"kind": "delete_target_sentence", "old": s[t]})

    # C4: answer replaced with counterfactual in the target sentence only
    form = matched_form(case)
    new_t = replace_ci(s[t], form, case["counterfactual_value"])
    clean = [new_t if i == t else x for i, x in enumerate(s)]
    marked_t = replace_ci(s[t], form, f"~~{form}~~ **{case['counterfactual_value']}**")
    marked = [marked_t if i == t else x for i, x in enumerate(s)]
    out["C4"] = (" ".join(clean), " ".join(marked),
                 {"kind": "replace_answer", "old": form, "new": case["counterfactual_value"]})

    # C5: negative control, edit inside the unrelated sentence only
    c5 = case["c5"]
    assert s[u].count(c5["original"]) == 1, (case["case_id"], "c5 original not unique in unrelated sentence")
    new_u = s[u].replace(c5["original"], c5["replacement"])
    clean = [new_u if i == u else x for i, x in enumerate(s)]
    marked_u = s[u].replace(c5["original"], f"~~{c5['original']}~~ **{c5['replacement']}**")
    marked = [marked_u if i == u else x for i, x in enumerate(s)]
    out["C5"] = (" ".join(clean), " ".join(marked),
                 {"kind": "edit_unrelated_sentence", "old": c5["original"], "new": c5["replacement"]})
    return out


def build_case(case, d1_position):
    """Return (records, marked) for one case: JSONL records and per-condition marked-up docs."""
    order = doc_order(case, d1_position)
    display = {name: f"Doc {pos + 1}" for pos, name in enumerate(order)}
    d1_position = order.index("d1") + 1
    variants = d1_variants(case)
    records, marked = [], {}

    for cond in CONDITIONS:
        if cond == "C0":
            clean_d1, marked_d1, change = None, None, None
            names = []
            marked_names = []
        else:
            clean_d1, marked_d1, change = variants[cond]
            names = [n for n in order if not (cond == "C2" and n == "d1")]
            marked_names = order
        texts = {"d1": clean_d1, "d2": case["d2"], "d3": case["d3"]}
        marked_texts = {"d1": marked_d1, "d2": case["d2"], "d3": case["d3"]}
        records.append({
            "case_id": case["case_id"],
            "condition": cond,
            "tier": case["tier"],
            "question": case["question"],
            "seed": SEED,
            "order": order,
            "d1_position": d1_position,
            "docs": [{"display_id": display[n], "internal": n, "text": texts[n]} for n in names],
            "change": change,
        })
        marked[cond] = [(display[n], n, marked_texts[n]) for n in marked_names]
    return records, marked


def check(case, records):
    """Self-checks on the generated conditions."""
    by = {r["condition"]: r for r in records}
    text = lambda r, n: next((d["text"] for d in r["docs"] if d["internal"] == n), None)
    t = case["d1"][case["target_index"]]
    form = matched_form(case)
    cid = case["case_id"]
    assert by["C0"]["docs"] == [], cid
    assert len({tuple(r["order"]) for r in records}) == 1, cid
    for c in ("C1", "C3", "C4", "C5"):
        assert [d["internal"] for d in by[c]["docs"]] == by["C1"]["order"], (cid, c)
    assert [d["internal"] for d in by["C2"]["docs"]] == [n for n in by["C1"]["order"] if n != "d1"], cid
    ids = {(d["internal"]): d["display_id"] for d in by["C1"]["docs"]}
    for c in ("C2", "C3", "C4", "C5"):
        assert all(ids[d["internal"]] == d["display_id"] for d in by[c]["docs"]), (cid, c)
        assert text(by[c], "d2") == case["d2"] and text(by[c], "d3") == case["d3"], (cid, c)
    assert t not in text(by["C3"], "d1"), cid
    assert form.lower() not in text(by["C4"], "d1").lower(), cid
    assert case["counterfactual_value"] in text(by["C4"], "d1"), cid
    assert t in text(by["C5"], "d1") and case["c5"]["replacement"] in text(by["C5"], "d1"), cid


def render_review(cases, all_marked, all_records):
    lines = ["# Pilot conditions: review", "",
             f"Seed {SEED}. Generated by `src/interventions.py`. `~~old~~` = removed text, `**new**` = inserted text.", ""]
    for case, marked, records in zip(cases, all_marked, all_records):
        order = records[0]["order"]
        lines += [f"## {case['case_id']} ({case['tier']}, {case['domain']})", "",
                  f"**Question:** {case['question']}",
                  f"**Expected answer:** {case['answer']}  |  **Counterfactual (C4):** {case['counterfactual_value']}",
                  f"**Document order:** {', '.join(order)}  |  **D1 position:** {records[0]['d1_position']}", ""]
        for cond in CONDITIONS:
            lines.append(f"### {case['case_id']} {cond}")
            if cond == "C0":
                lines += ["_No documents._", ""]
                continue
            for display_id, name, text in marked[cond]:
                lines.append(f"- **{display_id}** ({name.upper()}): {text}")
            lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=str(CASES_PATH), help="cases JSON (default: the pilot cases)")
    ap.add_argument("--name", default="pilot", help="outputs are data/<name>_conditions.jsonl and ..._review.md")
    args = ap.parse_args()
    jsonl_path = ROOT / "data" / f"{args.name}_conditions.jsonl"
    review_path = ROOT / "data" / f"{args.name}_conditions_review.md"
    cases = json.loads(Path(args.cases).read_text())
    positions = assign_d1_positions(cases)
    all_records, all_marked = [], []
    for case in cases:
        records, marked = build_case(case, positions[case["case_id"]])
        check(case, records)
        all_records.append(records)
        all_marked.append(marked)
    jsonl_path.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for recs in all_records for r in recs))
    review_path.write_text(render_review(cases, all_marked, all_records) + "\n")
    counts = Counter(positions.values())
    print(f"{len(cases)} cases x {len(CONDITIONS)} conditions = {sum(map(len, all_records))} lines")
    print(f"D1 position counts (seed {SEED}): " + ", ".join(f"position {p}: {counts[p]}" for p in sorted(counts)))
    print(f"wrote {jsonl_path.relative_to(ROOT)} and {review_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
