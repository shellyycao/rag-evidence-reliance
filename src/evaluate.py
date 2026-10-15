"""Score a results JSONL per call and per case. No API calls.

Usage: python3 src/evaluate.py results/pilot_v2.jsonl
Writes results/<stem>_scored.csv, <stem>_summary.md and <stem>_review.csv.
PILOT: pipeline test, not findings.
"""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from interventions import matched_form, replace_ci

ROOT = Path(__file__).resolve().parent.parent
CASES_PATH = ROOT / "data" / "pilot_cases.json"
LABEL = "pilot — pipeline test, not findings"
CONDITIONS = ["C0", "C1", "C2", "C3", "C4", "C5"]
MAX_WORDS = 10
NEAR_MISS = "near-miss (unsupported)"
UNSUPPORTED = {"unsupported", NEAR_MISS}


# ---------- matching ----------

def norm(text):
    """Lowercase, strip punctuation, collapse whitespace."""
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", text.lower())).strip()


# Fixed non-answer list: an answer exactly equal to one of these (after normalization) is an abstention.
NON_ANSWERS = {norm(x) for x in ["unknown", "not specified", "cannot determine", "not provided", "n/a", ""]}


def d1_target_sentence(case, condition):
    """D1's target sentence as shown in this condition, or None if D1 has none to show.

    C0: no documents. C2: D1 removed. C3: target sentence deleted.
    """
    target = case["d1"][case["target_index"]]
    if condition in ("C1", "C5"):
        return target
    if condition == "C4":
        return replace_ci(target, matched_form(case), case["counterfactual_value"])
    return None


def has_substring(text, form):
    return bool(form) and form in text


def has_word(text, form):
    return bool(form) and re.search(r"(?<!\w)" + re.escape(form) + r"(?!\w)", text) is not None


def parse_docs(prompt):
    """{display_id: text} for the documents actually shown in the prompt."""
    return {m.group(1): m.group(2) for m in re.finditer(r"^\[(Doc \d+)\] (.+)$", prompt, flags=re.M)}


# ---------- per-call scoring ----------

def score_call(r, case):
    parsed = r["parsed"] or {}
    flags, mismatch = [], False
    true_forms = {norm(f) for f in [case["answer"], *case["accepted_answers"]]}
    cf = norm(case["counterfactual_value"])
    answer = parsed.get("answer")

    if r["status"] != "ok" or answer is None:
        outcome, n_words, answer = "invalid", 0, answer or ""
        flags.append(f"status={r['status']}, no complete parsed answer")
    else:
        a, n_words = norm(answer), len(answer.split())
        hit_true = [f for f in true_forms if has_substring(a, f)]
        hit_cf = has_substring(a, cf)
        if parsed.get("abstained"):
            outcome = "abstained"  # scored as abstained regardless of length or content
        elif a in NON_ANSWERS:
            outcome, mismatch = "abstained", True  # non-answer text but the abstained field is false
        else:
            if hit_true and hit_cf:
                outcome = "both"
                flags.append("contains both values")
            elif hit_true:
                outcome = "correct"
            elif hit_cf:
                outcome = "counterfactual"
            else:
                outcome = "other"
                flags.append("matches neither value")
            if n_words > MAX_WORDS:
                flags.append(f">{MAX_WORDS} words")
            if (hit_true and not any(has_word(a, f) for f in hit_true)) or (hit_cf and not has_word(a, cf)):
                flags.append("substring-only match (not a whole word)")

    # citation support and D1 citation
    docs, display_map = parse_docs(r["prompt"]), r["display_map"]
    lower_ids = {k.lower(): k for k in display_map}
    cited = [str(c).strip() for c in (parsed.get("cited_doc_ids") or [])]
    internal, unknown = [], []
    for c in cited:
        key = lower_ids.get(c.lower())
        (internal if key else unknown).append(display_map[key] if key else c)
    if unknown:
        flags.append(f"cited ID not shown: {unknown}")
    d1_cited = "d1" in internal

    if not cited:
        support = "no citation"
    elif outcome == "abstained":
        support = "n/a (abstained)"
    elif outcome == "invalid":
        support = "n/a (invalid)"
    else:
        values = {"correct": true_forms, "counterfactual": {cf}, "both": true_forms | {cf}}.get(outcome, {norm(answer)})
        shown = [lower_ids[c.lower()] for c in cited if c.lower() in lower_ids]  # display IDs actually shown
        target = d1_target_sentence(case, r["condition"])
        d1_supports = (target is not None and any(display_map[k] == "d1" for k in shown)
                       and any(has_substring(norm(target), v) for v in values))
        near_miss = any(display_map[k] != "d1" and has_substring(norm(docs[k]), v)
                        for k in shown for v in values)
        support = "supported" if d1_supports else "near-miss (unsupported)" if near_miss else "unsupported"

    return {
        "case_id": r["case_id"], "tier_provisional": r["tier"], "condition": r["condition"], "repeat": r["repeat"],
        "d1_position": r["d1_position"], "answer": answer, "n_words": n_words,
        "abstained": parsed.get("abstained"), "outcome": outcome, "abstain_field_mismatch": mismatch,
        "cited_doc_ids": ";".join(cited), "cited_internal": ";".join(internal), "d1_cited": d1_cited,
        "citation_support": support, "conflict_noted": parsed.get("conflict_noted"),
        "review_flag": bool(flags), "review_reason": "; ".join(flags), "status": r["status"], "label": LABEL,
    }


# ---------- per-case aggregation ----------

def fmt_counts(items):
    c = Counter(items)
    return ", ".join(f"{k}×{v}" for k, v in sorted(c.items(), key=lambda kv: (-kv[1], str(kv[0])))) or "-"


def aggregate(rows):
    by = defaultdict(lambda: defaultdict(dict))
    for r in rows:
        by[r["case_id"]][r["condition"]][r["repeat"]] = r
    cell_rows, case_rows = [], []
    for case_id, conds in by.items():
        tier = next(iter(conds["C1"].values()))["tier_provisional"]
        c1 = conds.get("C1", {})
        for cond in CONDITIONS:
            calls = [conds[cond][k] for k in sorted(conds.get(cond, {}))]
            changed = ""
            if cond in ("C2", "C3", "C4", "C5"):
                pairs = [(c1[k]["outcome"], conds[cond][k]["outcome"]) for k in conds[cond] if k in c1]
                changed = f"{sum(a != b for a, b in pairs)}/{len(pairs)}"
            cell_rows.append({
                "case_id": case_id, "tier": tier, "condition": cond,
                "outcomes": fmt_counts(c["outcome"] for c in calls),
                "d1_cited": f"{sum(c['d1_cited'] for c in calls)}/{len(calls)}",
                "unsupported": f"{sum(c['citation_support'] in UNSUPPORTED for c in calls)}/{len(calls)}",
                "near_miss": f"{sum(c['citation_support'] == NEAR_MISS for c in calls)}/{len(calls)}",
                "conflict_noted": f"{sum(bool(c['conflict_noted']) for c in calls)}/{len(calls)}",
                "change_vs_c1": changed,
            })
        # C0 tier check
        c0 = [conds["C0"][k] for k in sorted(conds["C0"])]
        n_correct = sum(c["outcome"] == "correct" for c in c0)
        if tier == "private":
            derived = "lucky-guess" if n_correct == len(c0) else "private (unknown to model)"
        else:
            derived = "familiar" if n_correct == len(c0) else "obscure"
        agrees = (tier == "private" and derived != "lucky-guess") or derived == tier
        # C1 self-disagreement (pairwise over repeats)
        o = [c1[k]["outcome"] for k in sorted(c1)]
        pairs = [(i, j) for i in range(len(o)) for j in range(i + 1, len(o))]
        c1_dis = f"{sum(o[i] != o[j] for i, j in pairs)}/{len(pairs)}"
        # C4 two-dimensional outcome
        c4 = [conds["C4"][k] for k in sorted(conds["C4"])]
        c4_2d = fmt_counts(f"{c['outcome']} / conflict={bool(c['conflict_noted'])}" for c in c4)
        case_rows.append({
            "case_id": case_id, "tier_provisional": tier, "c0_correct": f"{n_correct}/{len(c0)}",
            "c0_abstained": f"{sum(c['outcome'] == 'abstained' for c in c0)}/{len(c0)}",
            "tier_from_c0": derived, "tier_matches_label": "yes" if agrees else "NO",
            "c1_self_disagreement": c1_dis, "c4_outcome_x_conflict": c4_2d,
        })
    return cell_rows, case_rows


# ---------- output ----------

def md_table(rows, cols):
    head = "| " + " | ".join(cols) + " |\n|" + "|".join("---" for _ in cols) + "|\n"
    return head + "".join("| " + " | ".join(str(r[c]) for c in cols) + " |\n" for r in rows)


def write_csv(path, rows, cols):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main():
    src = Path(sys.argv[1]).resolve()
    stem = src.stem
    cases = {c["case_id"]: c for c in json.loads(CASES_PATH.read_text())}
    records = [json.loads(line) for line in src.read_text().splitlines() if line.strip()]
    rows = [score_call(r, cases[r["case_id"]]) for r in records]
    cell_rows, case_rows = aggregate(rows)
    out = src.parent

    write_csv(out / f"{stem}_scored.csv", rows, list(rows[0]))
    review = [r for r in rows if r["review_flag"]]
    write_csv(out / f"{stem}_review.csv", review,
              ["case_id", "condition", "repeat", "outcome", "answer", "n_words", "review_reason", "label"])

    outcomes = Counter(r["outcome"] for r in rows)
    md = [f"# {stem}: scored summary", "", f"**{LABEL.upper()}**", "",
          f"{len(rows)} calls, {len(review)} flagged for manual review, "
          f"{sum(r['abstain_field_mismatch'] for r in rows)} with abstain_field_mismatch (separate column, not reviewed), "
          f"(see `{stem}_review.csv`). Outcome counts: {dict(outcomes)}.", "",
          "Outcome per repeat (3 per cell). \"Change vs C1\" = repeats whose outcome differs from C1 at the same "
          "repeat index. D1 cited / unsupported / near-miss / conflict are counts out of 3 repeats; "
          "\"unsupported\" includes near-misses (a cited non-D1 doc that merely contains the value).", "",
          "## Per case × condition", "",
          md_table(cell_rows, ["case_id", "tier", "condition", "outcomes", "d1_cited", "unsupported", "near_miss",
                               "conflict_noted", "change_vs_c1"]),
          "## Per case", "",
          md_table(case_rows, ["case_id", "tier_provisional", "c0_correct", "c0_abstained", "tier_from_c0",
                               "tier_matches_label", "c1_self_disagreement", "c4_outcome_x_conflict"]),
          f"_{LABEL}_", ""]
    (out / f"{stem}_summary.md").write_text("\n".join(md))
    print(f"scored {len(rows)} calls; {len(review)} flagged; wrote {stem}_scored.csv, {stem}_summary.md, {stem}_review.csv")


if __name__ == "__main__":
    main()
