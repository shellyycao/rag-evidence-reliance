"""Score the RAG-generation run and put it beside the primary (fixed-evidence) experiment. No API calls.

Per-call scoring is evaluate.score_call, unchanged. Writes, next to the RAG results file:
<stem>_scored.csv (one row per call), <stem>_review.csv (flagged rows; review_label is kept on re-run),
<stem>_summary.md (RAG vs primary tables).

Usage: .venv/bin/python src/rag_evaluate.py results/rag_gen_v1/rag_gen_v1.jsonl
Secondary analysis: descriptive, case-level bootstrap CIs, no significance claims.
"""
import argparse
import csv
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

import evaluate as ev
from analyze import CONFLICT_TYPES, suggest_conflict_type  # same conflict-type rules as the primary analysis

ROOT = Path(__file__).resolve().parent.parent
CASES_PATH = ROOT / "data" / "cases_full.json"
PILOT_CASES_PATH = ROOT / "data" / "pilot_cases.json"
PRIMARY_CONFLICT_PATH = ROOT / "results" / "full_v1_combined" / "full_v1_combined_conflict_review.csv"
PRIMARY_PATH = ROOT / "results" / "full_v1_combined" / "full_v1_combined.jsonl"
CONDITIONS = ["C1", "C2", "C3", "C4", "C5"]
TIERS = ["familiar", "obscure", "private"]
LABEL = "RAG-generation mode: secondary analysis, descriptive (TF-IDF top-3, one repeat per cell)"
PILOT_LABEL = "RAG-generation PILOT: pipeline test, not findings"
SEED, N_BOOT = 590, 2000
# Citations that make a support judgment meaningful: the model cited something and did not abstain.
NOT_JUDGED = {"no citation", "n/a (abstained)", "n/a (premise rejected)", "n/a (invalid)"}


def answer_type(outcome):
    return {"correct": "true value", "counterfactual": "false value", "abstained": "abstained"}.get(outcome, "other")


def load_records(path):
    """Last record per (case, condition, repeat): a retry after an error replaces the errored line."""
    latest = {}
    for line in Path(path).read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            latest[(r["case_id"], r["condition"], r["repeat"])] = r
    return list(latest.values())


def score_all(records, cases, labels):
    rows = []
    for r in records:
        row = ev.score_call(r, cases[r["case_id"]], labels)
        row["answer_type"] = answer_type(row["outcome"])
        row["question"] = r.get("question") or cases[r["case_id"]]["question"]
        row["explanation"] = (r["parsed"] or {}).get("explanation") or ""
        cited = [c for c in row["cited_internal"].split(";") if c]
        row["filler_cited"] = sum(c.startswith("filler:") for c in cited)
        # another case's document: an internal id "<CASE>:d<n>" with a different case prefix
        row["other_case_cited"] = sum(bool(re.match(r"^\w+:d[123]$", c)) and not c.startswith(r["case_id"] + ":")
                                      for c in cited)
        row["tier"] = row["tier_provisional"]
        row["input_tokens"], row["output_tokens"] = r.get("input_tokens"), r.get("output_tokens")
        row["cost_usd"] = r.get("estimated_cost_usd")
        if r.get("mode") == "rag_generation":
            row["retrieved"] = "; ".join(f"{x['doc_id']} (rank {x['rank']}, {x['score']})" for x in r["retrieved"])
            row["display_order"] = "; ".join(r["display_order"])
            row["d1_in_top3"], row["d1_rank"] = r["d1_in_top3"], r["d1_rank"]
        rows.append(row)
    return rows


# ---------- metrics ----------

def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else None


def per_case(rows, pred, value):
    """{case_id: mean of value(row) over that case's rows satisfying pred}; cases with no such row are dropped."""
    by = defaultdict(list)
    for r in rows:
        if pred(r):
            by[r["case_id"]].append(value(r))
    return {c: mean(v) for c, v in by.items()}


def rate_ci(case_values):
    """Mean over cases with a percentile bootstrap CI resampled at the case level."""
    vals = list(case_values.values())
    if not vals:
        return "n/a (0 cases)"
    rng = random.Random(SEED)
    boots = sorted(mean(rng.choices(vals, k=len(vals))) for _ in range(N_BOOT))
    lo, hi = boots[int(0.025 * N_BOOT)], boots[int(0.975 * N_BOOT) - 1]
    return f"{mean(vals):.2f} [{lo:.2f}, {hi:.2f}] (n={len(vals)})"


def md_table(rows, cols):
    return ("| " + " | ".join(cols) + " |\n|" + "|".join("---" for _ in cols) + "|\n"
            + "".join("| " + " | ".join(str(r[c]) for c in cols) + " |\n" for r in rows))


def frac(k, n):
    return f"{k}/{n}" if n else "n/a"


def pilot_ids():
    return {c["case_id"] for c in json.loads(PILOT_CASES_PATH.read_text())}


def summarize(stem, label, rag, primary, ctypes):
    hard = pilot_ids()
    out = [f"# {stem}: RAG-generation vs primary experiment", "", f"**{label}**", "",
           f"RAG: {len(rag)} calls (top-3 TF-IDF documents, 1 repeat per cell). Primary: {len(primary)} calls from "
           "`full_v1_combined`, same cases and conditions C1-C5, fixed D1/D2/D3, 3 repeats per cell. Per-call scoring is "
           "`evaluate.score_call`. Rates over cases are means of per-case rates, with case-level bootstrap 95% CIs "
           f"({N_BOOT} resamples, seed {SEED}); with few cases per tier these are descriptive only. "
           "Reported for all cases, then separately for the 9 pilot-topic cases (which have same-topic hard negatives "
           "in the frozen filler) and the 21 new cases (which have none, so D1 retrieval is expected to look easier).", ""]
    groups = [("All cases", lambda r: True),
              ("The 9 cases with same-topic hard negatives", lambda r: r["case_id"] in hard),
              ("The 21 new cases without hard negatives", lambda r: r["case_id"] not in hard)]
    for name, keep in groups:
        g_rag, g_prim = [r for r in rag if keep(r)], [r for r in primary if keep(r)]
        if not g_rag:
            continue
        n_cases = len({r["case_id"] for r in g_rag})
        out += [f"# {name} ({n_cases} cases)", ""]
        out += [line.replace("## ", "### ", 1) if line.startswith("## ") else line
                for line in sections(stem, label, g_rag, g_prim, ctypes)]
    return "\n".join(out)


def sections(stem, label, rag, primary, ctypes):
    modes = [("RAG", rag), ("Primary", primary)]
    out = []

    # 1. retrieval
    out += ["## 1. Was D1 retrieved? (RAG only)", "",
            "D1 in top-3 means the case's own D1, or its modified version in C3-C5, was among the 3 documents sent. "
            "In C2 D1 is removed, so this is undefined. If the modified D1 is not retrieved the model never saw the "
            "intervention, so the RAG rows of the later tables are also given conditional on retrieval.", ""]
    rows = []
    for cond in CONDITIONS:
        rs = [r for r in rag if r["condition"] == cond]
        k = sum(bool(r["d1_in_top3"]) for r in rs)
        rank = mean(r["d1_rank"] for r in rs if r["d1_rank"])
        rows.append({"condition": cond, "D1 in top-3": "n/a (removed)" if cond == "C2" else frac(k, len(rs)),
                     "D1 cited": frac(sum(r["d1_cited"] for r in rs), len(rs)),
                     "mean D1 rank": "n/a" if rank is None else f"{rank:.1f}"})
    out += [md_table(rows, ["condition", "D1 in top-3", "D1 cited", "mean D1 rank"])]

    # 2. answer type
    out += ["## 2. Answer type by condition", "",
            "true value = accepted original answer; false value = the C4 counterfactual; abstained; other = both values, "
            "neither value, premise rejected, wrong guess or invalid. Counts out of calls.", ""]
    rows = []
    for cond in CONDITIONS:
        row = {"condition": cond}
        for name, rs in modes:
            rs = [r for r in rs if r["condition"] == cond]
            c = Counter(r["answer_type"] for r in rs)
            row[name] = f"true {c['true value']}, false {c['false value']}, abstained {c['abstained']}, " \
                        f"other {c['other']} (of {len(rs)})"
        rows.append(row)
    out += [md_table(rows, ["condition", "RAG", "Primary"])]

    # 3. C4 following by tier
    out += ["## 3. C4 counterfactual-following by tier", "",
            "Share of C4 calls whose answer is the counterfactual value, per tier. "
            "'RAG, modified D1 retrieved' keeps only RAG C4 calls where the modified D1 was in the top-3. "
            "H1 predicts lower following on familiar cases; the 'private' tier holds facts the model does not know.", ""]
    rows = []
    for tier in TIERS + ["all"]:
        in_tier = lambda r: r["condition"] == "C4" and (tier == "all" or r["tier"] == tier)
        follow = lambda r: r["outcome"] == "counterfactual"
        rows.append({
            "tier": tier,
            "Primary": rate_ci(per_case(primary, in_tier, follow)),
            "RAG (all C4 calls)": rate_ci(per_case(rag, in_tier, follow)),
            "RAG, modified D1 retrieved": rate_ci(per_case(rag, lambda r: in_tier(r) and r["d1_in_top3"], follow)),
        })
    out += [md_table(rows, ["tier", "Primary", "RAG (all C4 calls)", "RAG, modified D1 retrieved"])]
    out += ["C4 two-dimensional outcome (answer type × conflict_noted), pooled calls:", ""]
    rows = []
    for name, rs in modes:
        c = Counter(f"{r['answer_type']} / conflict={bool(r['conflict_noted'])}" for r in rs if r["condition"] == "C4")
        rows.append({"mode": name, "C4 outcomes": ", ".join(f"{k}×{v}" for k, v in sorted(c.items()))})
    out += [md_table(rows, ["mode", "C4 outcomes"])]

    # 4. unsupported citations
    out += ["## 4. Unsupported-citation rate", "",
            "Among calls that cited at least one document and did not abstain: the share whose citation is "
            "'unsupported' or a 'near-miss (unsupported)' (observed, not a claim about faithfulness). "
            "'No citation' calls are counted separately.", ""]
    rows = []
    for cond in CONDITIONS:
        row = {"condition": cond}
        for name, rs in modes:
            rs = [r for r in rs if r["condition"] == cond]
            judged = [r for r in rs if r["citation_support"] not in NOT_JUDGED]
            row[name] = (f"{frac(sum(r['citation_support'] in ev.UNSUPPORTED for r in judged), len(judged))} unsupported; "
                         f"{sum(r['citation_support'] == 'no citation' for r in rs)} no citation")
        rows.append(row)
    out += [md_table(rows, ["condition", "RAG", "Primary"])]

    # 5. filler / other-case documents cited
    out += ["## 5. Filler and other-case documents cited (RAG only)", "",
            "A filler document is one of the 100 frozen filler documents; an other-case document is a D1/D2/D3 of a "
            "different case. The primary experiment cannot cite either.", ""]
    rows = []
    for cond in CONDITIONS:
        rs = [r for r in rag if r["condition"] == cond]
        rows.append({"condition": cond, "calls": len(rs),
                     "filler docs cited (total)": sum(r["filler_cited"] for r in rs),
                     "calls citing a filler": sum(r["filler_cited"] > 0 for r in rs),
                     "other-case docs cited (total)": sum(r["other_case_cited"] for r in rs)})
    rows.append({"condition": "all", "calls": len(rag), "filler docs cited (total)": sum(r["filler_cited"] for r in rag),
                 "calls citing a filler": sum(r["filler_cited"] > 0 for r in rag),
                 "other-case docs cited (total)": sum(r["other_case_cited"] for r in rag)})
    out += [md_table(rows, ["condition", "calls", "filler docs cited (total)", "calls citing a filler",
                            "other-case docs cited (total)"])]

    # 5b. D1 not retrieved
    out += ["## 5b. When D1 was not retrieved (RAG only)", "",
            "RAG calls whose top-3 did not contain D1 (all of C2, where D1 is removed, plus any C3-C5 call where it "
            "dropped out). The model then answers from other documents or from its own knowledge. "
            "'Primary' is the same condition in the fixed-evidence experiment (C2/C3: D1 removed or its target "
            "sentence deleted, D2/D3 still shown).", ""]
    rows = []
    for cond in CONDITIONS:
        rs = [r for r in rag if r["condition"] == cond and not r["d1_in_top3"]]
        if not rs:
            continue
        c = Counter(r["answer_type"] for r in rs)
        sup = Counter(r["citation_support"] for r in rs)
        pc = Counter(r["answer_type"] for r in primary if r["condition"] == cond)
        rows.append({"condition": cond, "RAG calls without D1": len(rs),
                     "answer type": f"true {c['true value']}, false {c['false value']}, abstained {c['abstained']}, other {c['other']}",
                     "citations": ", ".join(f"{k}×{v}" for k, v in sorted(sup.items())),
                     "filler / other-case cited": f"{sum(r['filler_cited'] for r in rs)} / {sum(r['other_case_cited'] for r in rs)}",
                     "Primary (same condition)": f"true {pc['true value']}, false {pc['false value']}, abstained {pc['abstained']}, other {pc['other']}"})
    out += [md_table(rows, ["condition", "RAG calls without D1", "answer type", "citations", "filler / other-case cited",
                            "Primary (same condition)"]) if rows else "No such calls.\n"]
    rows = []
    for tier in TIERS:
        rs = [r for r in rag if r["tier"] == tier and not r["d1_in_top3"]]
        c = Counter(r["answer_type"] for r in rs)
        rows.append({"tier": tier, "calls": len(rs),
                     "answer type": f"true {c['true value']}, false {c['false value']}, abstained {c['abstained']}, other {c['other']}"})
    out += ["By tier (RAG calls without D1):", "", md_table(rows, ["tier", "calls", "answer type"])]

    # 5c. conflict
    out += ["## 5c. Conflict noted", "",
            "`conflict_noted` is the field the model reported, exactly as in the primary experiment; the explanation is not "
            "used for the count. Conflict types (exploratory, post hoc) apply to C4 calls with `conflict_noted` true; "
            "an empty `conflict_type` cell falls back to the keyword suggestion (the same rules as the primary analysis).", ""]
    rows = []
    for cond in CONDITIONS:
        row = {"condition": cond}
        for name, rs in modes:
            rs = [r for r in rs if r["condition"] == cond]
            row[name] = frac(sum(bool(r["conflict_noted"]) for r in rs), len(rs))
        rows.append(row)
    out += ["conflict_noted, calls with the field true:", "", md_table(rows, ["condition", "RAG", "Primary"])]
    rows = []
    for tier in TIERS:
        row = {"tier": tier}
        for name, rs in modes:
            c4 = [r for r in rs if r["condition"] == "C4" and r["tier"] == tier]
            c = Counter(f"{r['answer_type']} / conflict={bool(r['conflict_noted'])}" for r in c4)
            row[name] = ", ".join(f"{k}×{v}" for k, v in sorted(c.items())) or "-"
        rows.append(row)
    out += ["C4 outcome × conflict_noted by tier:", "", md_table(rows, ["tier", "RAG", "Primary"])]
    rows = []
    for name, rs in modes:
        labs = Counter(ctypes[name].get((r["case_id"], str(r["repeat"])), "unlabeled")
                       for r in rs if r["condition"] == "C4" and r["conflict_noted"])
        rows.append({"mode": name, "conflict_type of C4 calls with conflict_noted": ", ".join(f"{k}×{v}" for k, v in sorted(labs.items())) or "none"})
    out += ["Conflict types:", "", md_table(rows, ["mode", "conflict_type of C4 calls with conflict_noted"])]

    # 6. cost
    cost = sum(r["cost_usd"] or 0 for r in rag)
    n_pending = sum(r["outcome_auto"] == "other" and not r["review_label"] for r in rag)
    out += ["## 6. Cost and review status", "",
            f"RAG run: {len(rag)} calls, estimated ${cost:.3f}. {sum(r['review_flag'] for r in rag)} calls flagged for "
            f"manual review (`{stem}_review.csv`), {n_pending} 'other' rows awaiting a review_label; until they are "
            "labeled they count as 'other'.", "", f"_{label}_", ""]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results", help="RAG-generation results JSONL, e.g. results/rag_gen_v1/rag_gen_v1.jsonl")
    ap.add_argument("--primary", default=str(PRIMARY_PATH), help="primary results JSONL to put alongside")
    args = ap.parse_args()
    src = Path(args.results).resolve()
    stem = src.stem
    label = PILOT_LABEL if "pilot" in stem else LABEL
    ev.LABEL = label
    cases = {c["case_id"]: c for c in json.loads(CASES_PATH.read_text())}

    review_path = src.parent / f"{stem}_review.csv"
    labels = ev.load_review_labels(review_path)  # read before the review file is rewritten
    rag = score_all(load_records(src), cases, labels)

    primary_src = Path(args.primary)
    primary_labels = ev.load_review_labels(primary_src.parent / f"{primary_src.stem}_review.csv")
    ran = {r["case_id"] for r in rag}
    primary = [r for r in score_all(load_records(primary_src), cases, primary_labels)
               if r["case_id"] in ran and r["condition"] in CONDITIONS]

    cols = ["case_id", "tier", "condition", "repeat", "question", "retrieved", "d1_in_top3", "d1_rank", "display_order",
            "answer", "outcome", "answer_type", "cited_doc_ids", "cited_internal", "d1_cited", "citation_support",
            "filler_cited", "other_case_cited", "abstained", "conflict_noted", "confidence", "abstain_field_mismatch",
            "input_tokens", "output_tokens", "cost_usd", "review_flag", "review_reason", "status", "label"]
    ev.write_csv(src.parent / f"{stem}_scored.csv", rag, cols)
    key_of = lambda r: (r["case_id"], r["condition"], str(r["repeat"]))
    review = [dict(r, outcome=r["outcome_auto"], review_label=labels.get(key_of(r), "")) for r in rag if r["review_flag"]]
    for key in sorted(set(labels) - {key_of(r) for r in review}):
        print(f"WARNING: review_label for {key} is lost: that row is no longer flagged for review")
    ev.write_csv(review_path, review, ["case_id", "condition", "repeat", "outcome", "review_label", "answer", "n_words",
                                       "review_reason", "label"])

    # conflict-type review for C4 calls with conflict_noted true; filled labels are kept on re-run
    conflict_path = src.parent / f"{stem}_conflict_review.csv"
    kept = {}
    if conflict_path.exists():
        kept = {(r["case_id"], r["repeat"]): r["conflict_type"].strip() for r in csv.DictReader(open(conflict_path))
                if r.get("conflict_type", "").strip()}
    cr = []
    for r in rag:
        if r["condition"] == "C4" and r["conflict_noted"]:
            sug, basis = suggest_conflict_type(r["explanation"] or r["answer"])
            cr.append({"case_id": r["case_id"], "tier": r["tier"], "repeat": r["repeat"], "outcome": r["outcome"],
                       "confidence": r["confidence"], "answer": r["answer"], "explanation": r["explanation"],
                       "cited_internal": r["cited_internal"], "suggested_conflict_type": sug, "suggestion_basis": basis,
                       "conflict_type": kept.get((r["case_id"], str(r["repeat"])), "")})
    for row in cr:
        if row["conflict_type"] and row["conflict_type"] not in CONFLICT_TYPES:
            print(f"WARNING: {row['case_id']} has conflict_type {row['conflict_type']!r}, not one of {CONFLICT_TYPES}")
    ev.write_csv(conflict_path, cr, ["case_id", "tier", "repeat", "outcome", "confidence", "answer", "explanation",
                                     "cited_internal", "suggested_conflict_type", "suggestion_basis", "conflict_type"])
    prim_c = {(r["case_id"], r["repeat"]): (r.get("conflict_type") or r["suggested_conflict_type"])
              for r in csv.DictReader(open(PRIMARY_CONFLICT_PATH))} if PRIMARY_CONFLICT_PATH.exists() else {}
    ctypes = {"RAG": {(r["case_id"], str(r["repeat"])): r["conflict_type"] or r["suggested_conflict_type"] for r in cr},
              "Primary": prim_c}
    (src.parent / f"{stem}_summary.md").write_text(summarize(stem, label, rag, primary, ctypes))
    print(f"scored {len(rag)} RAG calls ({len(primary)} primary calls alongside); {len(review)} flagged; "
          f"wrote {stem}_scored.csv, {stem}_review.csv, {stem}_conflict_review.csv, {stem}_summary.md")


if __name__ == "__main__":
    main()
