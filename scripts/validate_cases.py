"""Validate data/pilot_cases.json. No API calls. Exits 1 if any check fails."""
import json
import re
import sys
from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "data" / "pilot_cases.json"


def forms(case):
    """Answer plus accepted forms, longest first so the most specific form is matched."""
    return sorted({case["answer"], *case["accepted_answers"]}, key=len, reverse=True)


def replace_ci(text, old, new):
    return re.sub(re.escape(old), lambda _: new, text, flags=re.IGNORECASE)


def check(case):
    d1, t = case["d1"], case["target_index"]
    target = d1[t]
    results = {}

    # 1. an answer form appears in the target sentence
    matched = next((f for f in forms(case) if f.lower() in target.lower()), None)
    results["1 answer in target sentence"] = (
        matched is not None, f"matched {matched!r}" if matched else f"none of {forms(case)} in target")

    # 2. replacing the answer across all of D1 changes only the target sentence
    if matched:
        replaced = [replace_ci(s, matched, case["counterfactual_value"]) for s in d1]
        changed = [i for i, (a, b) in enumerate(zip(d1, replaced)) if a != b]
        results["2 counterfactual changes only target"] = (
            changed == [t], f"sentences changed: {changed}, expected [{t}]")
    else:
        results["2 counterfactual changes only target"] = (False, "skipped: no answer match")

    # 3. c5.original appears exactly once in D1, and only in the unrelated sentence
    orig = case["c5"]["original"]
    counts = [s.count(orig) for s in d1]
    unrelated = [i for i in range(len(d1)) if i != t and i != 0]
    ok3 = sum(counts) == 1 and all(counts[i] == 0 for i in range(len(d1)) if i not in unrelated)
    results["3 c5 once, only in unrelated sentence"] = (
        ok3, f"count per sentence {counts}; unrelated sentence index {unrelated}")

    # 4. no answer form appears in d2 or d3
    leaks = [(name, f) for name in ("d2", "d3") for f in forms(case) if f.lower() in case[name].lower()]
    results["4 answer absent from d2/d3"] = (not leaks, f"leaks: {leaks}" if leaks else "clean")
    return results


def main():
    cases = json.loads(PATH.read_text())
    failures = 0
    for case in cases:
        print(f"{case['case_id']} ({case['tier']}, {case['domain']})")
        for name, (ok, detail) in check(case).items():
            failures += not ok
            print(f"  {'PASS' if ok else 'FAIL'}  {name}: {detail}")
    print(f"\n{len(cases)} cases, {failures} failed checks")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
