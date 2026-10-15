"""Validate a cases file. No API calls. Exits 1 if any check fails.

Usage: python scripts/validate_cases.py [--cases data/cases_full.json]   (default: data/pilot_cases.json)

Per case:
  0. schema: required keys, 3 D1 sentences, target_index 1, known tier, c5 original differs from its replacement
  1. the answer (or an accepted form) appears in the target sentence
  2. replacing it with counterfactual_value changes only the target sentence
  3. c5.original appears exactly once in D1, only in the unrelated sentence
  4. the answer does NOT appear in the case's own d2 or d3
Across cases:
  5. case ids are unique
  6. no case's answer, accepted form or counterfactual appears in any OTHER case's documents
  7. none of them appears in the frozen filler (data/filler_docs.json)
(A case's own D2 may contain its counterfactual value, as a deliberate tricky distractor.)
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from evaluate import norm  # noqa: E402
from interventions import matched_form, replace_ci  # noqa: E402

REQUIRED = ["case_id", "tier", "domain", "question", "answer", "accepted_answers", "source", "counterfactual_value",
            "d1", "target_index", "c5", "d2", "d3", "tricky_distractor", "notes"]
TIERS = {"familiar", "obscure", "private"}


def forms(case):
    return sorted({case["answer"], *case["accepted_answers"]}, key=len, reverse=True)


def values(case):
    """Everything about this case that must not leak into other cases' documents."""
    return {norm(v): v for v in [*forms(case), case["counterfactual_value"]] if norm(v)}


def check_case(case):
    results = {}
    d1, t = case["d1"], case.get("target_index")

    missing = [k for k in REQUIRED if k not in case]
    problems = []
    if missing:
        problems.append(f"missing keys {missing}")
    if not missing:
        if len(d1) != 3:
            problems.append(f"{len(d1)} D1 sentences, expected 3")
        if t != 1:
            problems.append(f"target_index {t}, expected 1")
        if case["tier"] not in TIERS:
            problems.append(f"unknown tier {case['tier']!r}")
        if case["c5"]["original"] == case["c5"]["replacement"]:
            problems.append("c5 replacement equals its original")
    results["0 schema"] = (not problems, "; ".join(problems) or "ok")
    if missing or problems:
        return results

    target = d1[t]
    matched = next((f for f in forms(case) if f.lower() in target.lower()), None)
    results["1 answer in target sentence"] = (matched is not None,
                                               f"matched {matched!r}" if matched else f"none of {forms(case)} in target")

    if matched:
        form = matched_form(case)
        replaced = [replace_ci(s, form, case["counterfactual_value"]) for s in d1]
        changed = [i for i, (a, b) in enumerate(zip(d1, replaced)) if a != b]
        results["2 counterfactual changes only target"] = (changed == [t], f"sentences changed: {changed}, expected [{t}]")
    else:
        results["2 counterfactual changes only target"] = (False, "skipped: no answer match")

    orig = case["c5"]["original"]
    counts = [s.count(orig) for s in d1]
    unrelated = [i for i in range(len(d1)) if i not in (0, t)]
    ok3 = sum(counts) == 1 and all(counts[i] == 0 for i in range(len(d1)) if i not in unrelated)
    results["3 c5 once, only in unrelated sentence"] = (ok3, f"count per sentence {counts}; unrelated sentence index {unrelated}")

    leaks = [(name, f) for name in ("d2", "d3") for f in forms(case) if f.lower() in case[name].lower()]
    results["4 answer absent from own d2/d3"] = (not leaks, f"leaks: {leaks}" if leaks else "clean")
    return results


def check_global(cases, filler):
    failures = []
    ids = [c["case_id"] for c in cases]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        failures.append(("5 unique case ids", f"duplicate id {dup}"))
    for a in cases:
        for value_norm, value in values(a).items():
            for b in cases:
                if b is a:
                    continue
                for name, text in [("d1", " ".join(b["d1"])), ("d2", b["d2"]), ("d3", b["d3"])]:
                    if value_norm in norm(text):
                        failures.append(("6 no leak into other cases", f"{a['case_id']} value {value!r} appears in {b['case_id']} {name}"))
            for doc in filler:
                if value_norm in norm(doc["text"]):
                    failures.append(("7 no leak into frozen filler", f"{a['case_id']} value {value!r} appears in filler {doc['id']}"))
    return failures


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=str(ROOT / "data" / "pilot_cases.json"))
    args = ap.parse_args()
    cases = json.loads(Path(args.cases).read_text())
    filler_path = ROOT / "data" / "filler_docs.json"
    filler = json.loads(filler_path.read_text()) if filler_path.exists() else []

    failures = 0
    for case in cases:
        print(f"{case['case_id']} ({case.get('tier')}, {case.get('domain')})")
        for name, (ok, detail) in check_case(case).items():
            failures += not ok
            if not ok:
                print(f"  FAIL  {name}: {detail}")
    print(f"\nper-case checks on {len(cases)} cases: {failures} failed")

    global_failures = check_global(cases, filler)
    print(f"cross-case and filler checks ({len(filler)} filler docs): {len(global_failures)} failed")
    for name, detail in global_failures:
        print(f"  FAIL  {name}: {detail}")
    total = failures + len(global_failures)
    print(f"\n{len(cases)} cases, {total} failed checks")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
