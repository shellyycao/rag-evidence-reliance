"""RAG-generation mode (secondary analysis, pre-registered): the model answers from the top-3 documents a retriever
finds, instead of the fixed D1/D2/D3 set. Everything else is identical to the controlled experiment: prompt v3,
structured output, model ID, inference settings.

For each (case, condition C1-C5): the intervention is applied to the case's D1 inside the corpus (retrieval.build_corpus),
the case question (verbatim) is the query, and the TF-IDF top-3 are sent to the model as "Doc 1".."Doc 3". The vectorizer is
fit once on the original corpus (cases in scope + frozen filler v1) and never re-fit. The display order of the 3 retrieved
documents is shuffled with the fixed seed (590): each document gets a seeded pseudo-random key from (case, document), so a
document keeps the same relative order in every condition. C0 is not run (nothing to retrieve).

--dry-run builds everything and makes zero API calls. Real calls need --confirm and explicit user approval first.

Usage:
  .venv/bin/python src/rag_generation.py --dry-run [--pilot] [--scope all|pilot9]
  .venv/bin/python src/rag_generation.py --confirm [--pilot]
"""
import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

import retrieval
from interventions import SEED
from logging_utils import call_key, load_done, log_path
from prompts import INFERENCE_CONFIG, PROMPT_VERSION
from run_experiment import estimate, jobs, real_run
from smoke_test import MODEL_ID, PRICE_IN_PER_M, PRICE_OUT_PER_M

ROOT = Path(__file__).resolve().parent.parent
CASES_PATH = ROOT / "data" / "cases_full.json"
PILOT_CASES_PATH = ROOT / "data" / "pilot_cases.json"
FILLER_SHA_PREFIX = "71ec8c0e5b0e"  # frozen filler v1
CONDITIONS = ["C1", "C2", "C3", "C4", "C5"]
PILOT_CONDITIONS = ["C1", "C4"]


def load_scope(scope):
    """'all' = every case in cases_full.json (what was requested); 'pilot9' = the 9 cases the protocol pre-registered."""
    cases = json.loads(CASES_PATH.read_text())
    if scope == "pilot9":
        keep = {c["case_id"] for c in json.loads(PILOT_CASES_PATH.read_text())}
        cases = [c for c in cases if c["case_id"] in keep]
    return cases


def check_filler_frozen():
    sha = hashlib.sha256(retrieval.FILLER_PATH.read_bytes()).hexdigest()
    if not sha.startswith(FILLER_SHA_PREFIX):
        sys.exit(f"filler_docs.json is not the frozen v1 (sha256 {sha[:12]}…, expected {FILLER_SHA_PREFIX}…)")


def display_order(case_id, doc_ids):
    """Seeded shuffle of the retrieved documents; a document's key does not depend on the condition."""
    return sorted(doc_ids, key=lambda d: (random.Random(f"{SEED}:rag_order:{case_id}:{d}").random(), d))


def pilot_cases(cases):
    """--pilot: the first case of each tier, in file order."""
    seen, picked = set(), []
    for c in cases:
        if c["tier"] not in seen:
            seen.add(c["tier"])
            picked.append(c["case_id"])
    return picked


def build_lines(cases, filler, emit_ids, conditions):
    """One condition line per (case, condition), in the format run_experiment.jobs / logging_utils.make_record expect."""
    original = retrieval.build_corpus(cases, filler, cases[0], "C1")
    retriever = retrieval.TfidfRetriever(original)  # fit once, never re-fitted
    lines = []
    for case in cases:
        if case["case_id"] not in emit_ids:
            continue
        cid, d1_id = case["case_id"], f"{case['case_id']}:d1"
        for cond in conditions:
            corpus = retrieval.build_corpus(cases, filler, case, cond)
            ranking = retriever.rank(case["question"], corpus)
            top = ranking[:retrieval.K]
            order = display_order(cid, [d for d, _ in top])
            rank_of = {d: i for i, (d, _) in enumerate(ranking, 1)}
            score_of = dict(ranking)
            internal = lambda d: "d1" if d == d1_id else d  # evaluate.score_call recognizes the case's own D1 as "d1"
            lines.append({
                "case_id": cid, "condition": cond, "tier": case["tier"], "question": case["question"], "seed": SEED,
                "order": [internal(d) for d in order],
                "d1_position": order.index(d1_id) + 1 if d1_id in order else None,
                "docs": [{"display_id": f"Doc {i}", "internal": internal(d), "text": corpus[d]}
                         for i, d in enumerate(order, 1)],
                "extra": {
                    "mode": "rag_generation", "retriever": "tfidf", "question": case["question"],
                    "corpus_size": len(corpus), "d1_id": d1_id,
                    "d1_in_corpus": d1_id in corpus, "d1_in_top3": d1_id in [d for d, _ in top],
                    "d1_rank": rank_of.get(d1_id), "d1_score": round(score_of[d1_id], 4) if d1_id in score_of else None,
                    "retrieved": [{"doc_id": d, "rank": rank_of[d], "score": round(s, 4)} for d, s in top],
                    "display_order": order, "filler_sha256_prefix": FILLER_SHA_PREFIX,
                },
            })
    return lines


def dry_run(lines, all_jobs, path, scope):
    done = load_done(path)
    todo = [j for j in all_jobs if call_key(j[1]["case_id"], j[1]["condition"], j[0]) not in done]
    print(f"mode: RAG-generation | scope: {scope} ({len({l['case_id'] for l in lines})} cases) | retriever: tfidf (k=3)")
    print(f"prompt version: {PROMPT_VERSION} | model: {MODEL_ID} | settings: {INFERENCE_CONFIG}")
    for want in ("C1", "C4"):
        r, c, prompt = next(j for j in all_jobs if j[1]["condition"] == want)
        ex = c["extra"]
        print(f"\n===== EXAMPLE: case {c['case_id']} {want} | D1 in top-3: {ex['d1_in_top3']} (D1 rank {ex['d1_rank']}) "
              f"| retrieved { [(x['doc_id'], x['rank']) for x in ex['retrieved']] } "
              f"| map { {d['display_id']: d['internal'] for d in c['docs']} } =====")
        print(prompt)
    print("\n===== D1 in top-3 (retrieval is local; no API calls) =====")
    for cond in sorted({l["condition"] for l in lines}):
        ls = [l for l in lines if l["condition"] == cond]
        label = "n/a (D1 removed)" if cond == "C2" else f"{sum(l['extra']['d1_in_top3'] for l in ls)}/{len(ls)}"
        print(f"{cond}: {label}")
    est = [estimate(p) for _, _, p in todo]
    print("\n===== DRY RUN SUMMARY (no API calls made) =====")
    print(f"calls in plan: {len(all_jobs)}  |  already logged (skipped): {len(all_jobs) - len(todo)}  |  to run: {len(todo)}")
    print(f"estimated tokens: in~{sum(e[0] for e in est):,.0f}, out~{sum(e[1] for e in est):,.0f}")
    print(f"estimated cost: ${sum(e[2] for e in est):.2f} at ${PRICE_IN_PER_M}/${PRICE_OUT_PER_M} per M tokens")
    print("real run requires --confirm")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", choices=["all", "pilot9"], default="all",
                    help="all = every case in cases_full.json (default, as requested); pilot9 = the 9 pre-registered cases")
    ap.add_argument("--pilot", action="store_true",
                    help="3 cases (first of each tier) x C1 and C4 = 6 calls at one repeat")
    ap.add_argument("--run-name", default=None, help="default rag_gen_v1, or rag_gen_pilot with --pilot")
    ap.add_argument("--limit-case", nargs="+", metavar="CASE_ID", help="only these case IDs")
    ap.add_argument("--repeats", type=int, default=1, help="repeats per (case, condition); 1 (see Deviations Log)")
    ap.add_argument("--dry-run", action="store_true", help="build prompts and estimate cost; no API calls")
    ap.add_argument("--confirm", action="store_true", help="required to make real API calls")
    args = ap.parse_args()

    check_filler_frozen()
    cases, filler = load_scope(args.scope), retrieval.load_filler()
    emit = set(pilot_cases(cases)) if args.pilot else {c["case_id"] for c in cases}
    if args.limit_case:
        unknown = set(args.limit_case) - emit
        if unknown:
            sys.exit(f"case ID(s) not in this scope/selection: {sorted(unknown)}")
        emit = set(args.limit_case)
    conditions = PILOT_CONDITIONS if args.pilot else CONDITIONS
    run_name = args.run_name or ("rag_gen_pilot" if args.pilot else "rag_gen_v1")

    lines = build_lines(cases, filler, emit, conditions)
    all_jobs = jobs(lines, args.repeats)
    path = log_path(run_name)
    if args.dry_run:
        dry_run(lines, all_jobs, path, args.scope)
    elif not args.confirm:
        sys.exit(f"refusing to start {len(all_jobs)} API calls without --confirm. Run with --dry-run first.")
    else:
        real_run(all_jobs, path, run_name)


if __name__ == "__main__":
    main()
