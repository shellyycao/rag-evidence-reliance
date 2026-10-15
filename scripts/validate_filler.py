"""Validate data/filler_docs.json against data/pilot_cases.json. No API calls. Exits 1 on any failure.

Checks: unique ids, expected type counts, no case answer/accepted/counterfactual value in any filler doc,
hard negatives name a real case and share a content word with it, sane length, no near-duplicate of a case
document, and no filler doc that contains a case's D1 target sentence.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from evaluate import norm  # same normalization as scoring

MIN_HARD, MIN_GENERAL = 60, 40
MIN_WORDS, MAX_WORDS = 6, 40
STOP = set("""a an the of to in on at for and or is are was were be been it its this that these those with as by from
what who whom which when where why how did do does has have had not no yes can could will would about into over
after before between during than then there their they them he she his her you your we our i my me also each other
such more most some any many much very just only first known""".split())


def stem(w):
    return w[:-1] if len(w) > 3 and w.endswith("s") else w


def content_words(text):
    return {stem(w) for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP and len(w) > 2}


def main():
    cases = {c["case_id"]: c for c in json.loads((ROOT / "data" / "pilot_cases.json").read_text())}
    docs = json.loads((ROOT / "data" / "filler_docs.json").read_text())
    failures = []

    def fail(doc_id, msg):
        failures.append((doc_id, msg))

    ids = [d["id"] for d in docs]
    if len(ids) != len(set(ids)):
        fail("*", f"duplicate ids: {sorted({i for i in ids if ids.count(i) > 1})}")
    n_hard = sum(d["type"] == "hard_negative" for d in docs)
    n_gen = sum(d["type"] == "general" for d in docs)
    if n_hard < MIN_HARD or n_gen < MIN_GENERAL:
        fail("*", f"counts: {n_hard} hard negatives (min {MIN_HARD}), {n_gen} general (min {MIN_GENERAL})")

    # forbidden values: every case's answer forms and counterfactual, normalized
    forbidden = {}
    for cid, c in cases.items():
        for form in {c["answer"], *c["accepted_answers"], c["counterfactual_value"]}:
            if norm(form):
                forbidden[norm(form)] = cid
    case_docs = {norm(" ".join(c["d1"])) for c in cases.values()} | {norm(c[k]) for c in cases.values() for k in ("d2", "d3")}
    targets = {cid: norm(c["d1"][c["target_index"]]) for cid, c in cases.items()}

    per_case = {cid: 0 for cid in cases}
    for d in docs:
        text, n = d["text"], norm(d["text"])
        words = len(text.split())
        if not (MIN_WORDS <= words <= MAX_WORDS):
            fail(d["id"], f"{words} words (allowed {MIN_WORDS}-{MAX_WORDS})")
        for value, cid in forbidden.items():
            if value in n:
                fail(d["id"], f"contains forbidden value {value!r} (case {cid})")
        if n in case_docs:
            fail(d["id"], "duplicates a case document")
        for cid, t in targets.items():
            if t in n:
                fail(d["id"], f"contains the D1 target sentence of {cid}")
        if d["type"] == "hard_negative":
            cid = d.get("case_id")
            if cid not in cases:
                fail(d["id"], f"unknown case_id {cid!r}")
                continue
            per_case[cid] += 1
            c = cases[cid]
            case_words = content_words(" ".join([c["question"], *c["d1"], c["d2"], c["d3"]]))
            if not content_words(text) & case_words:
                fail(d["id"], f"shares no content word with case {cid}")
        elif d["type"] != "general":
            fail(d["id"], f"unknown type {d['type']!r}")

    print(f"{len(docs)} filler docs: {n_hard} hard negatives, {n_gen} general")
    print("hard negatives per case:", per_case)
    for doc_id, msg in failures:
        print(f"  FAIL  {doc_id}: {msg}")
    print(f"\n{len(failures)} failed checks")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
