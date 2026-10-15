"""Secondary analysis: can a retriever find D1 in a corpus of case documents plus filler?

Corpus = D1/D2/D3 of every pilot case + data/filler_docs.json. For each (case, condition) the intervention is applied
to that case's D1 only (C2 removes it; C3/C4/C5 replace its text); all other documents stay original. The query is the
case question, verbatim. The TF-IDF vectorizer (vocabulary and IDF) is fit ONCE on the original corpus and kept fixed
across all conditions; modified documents are transformed with that same vectorizer, so words that appear only in a
modified document (for example a counterfactual value) are out of vocabulary and ignored. Only the TF-IDF retriever is run; the embedding retriever is disabled until its model ID is
verified and Bedrock calls are approved. No API calls are made by this script.

Usage: .venv/bin/python src/retrieval.py [--retriever tfidf]
PILOT: pipeline test, not findings.
"""
import argparse
import csv
import json
from pathlib import Path

import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer

from interventions import d1_variants

ROOT = Path(__file__).resolve().parent.parent
CASES_PATH = ROOT / "data" / "pilot_cases.json"
FILLER_PATH = ROOT / "data" / "filler_docs.json"
RESULTS_DIR = ROOT / "results"
LABEL = "pilot — pipeline test, not findings"

K = 3
CONDITIONS = ["C1", "C2", "C3", "C4", "C5"]  # C0 has nothing to retrieve
# Pre-registered TF-IDF settings; fit once on the original corpus and kept fixed across all conditions.
TFIDF_SETTINGS = {"lowercase": True, "stop_words": "english", "ngram_range": (1, 1), "norm": "l2", "sublinear_tf": False}


def load_cases():
    return json.loads(CASES_PATH.read_text())


def load_filler():
    return json.loads(FILLER_PATH.read_text())


def build_corpus(cases, filler, target, condition):
    """{doc_id: text} with the intervention on `target`'s D1. Document order is deterministic."""
    corpus = {}
    for c in cases:
        cid = c["case_id"]
        d1 = " ".join(c["d1"])
        if c is target and condition != "C1":
            d1 = d1_variants(c)[condition][0]  # None for C2: D1 is removed from the corpus
        if d1 is not None:
            corpus[f"{cid}:d1"] = d1
        corpus[f"{cid}:d2"] = c["d2"]
        corpus[f"{cid}:d3"] = c["d3"]
    for d in filler:
        corpus[f"filler:{d['id']}"] = d["text"]
    return corpus


def order(scores_by_id):
    """Full ranking, highest score first; ties broken by doc id."""
    return sorted(scores_by_id.items(), key=lambda kv: (-kv[1], kv[0]))


class TfidfRetriever:
    name = "tfidf"

    def __init__(self, original_corpus):
        """Fit the vectorizer once on the original corpus; it is never re-fitted."""
        self.original = dict(original_corpus)
        self.vectorizer = TfidfVectorizer(**TFIDF_SETTINGS)
        ids = list(self.original)
        matrix = self.vectorizer.fit_transform([self.original[i] for i in ids]).tocsr()  # rows are l2-normalized
        self.rows = {doc_id: matrix[i] for i, doc_id in enumerate(ids)}

    def rank(self, query, corpus):
        """Rank `corpus` (possibly with one document removed or replaced) with the fixed vectorizer."""
        ids = list(corpus)
        rows = [self.rows[i] if corpus[i] == self.original.get(i) else self.vectorizer.transform([corpus[i]])
                for i in ids]  # unchanged docs reuse their original row; modified docs are only transformed
        scores = (sparse.vstack(rows) @ self.vectorizer.transform([query]).T).toarray().ravel()  # cosine similarity
        return order(dict(zip(ids, map(float, scores))))


class TitanEmbeddingRetriever:
    """Amazon Titan Text Embeddings via Bedrock. UNTESTED and DISABLED by default.

    Needs an explicitly verified model ID (none is assumed) and allow_bedrock_calls=True, which requires the user's
    approval of the embedding calls first. Nothing in this module's CLI constructs it.
    """
    name = "titan"

    def __init__(self, model_id, allow_bedrock_calls=False):
        if not allow_bedrock_calls:
            raise RuntimeError("Bedrock embedding calls are not approved; the embedding retriever is disabled.")
        import boto3
        from smoke_test import PROFILE, REGION

        self.model_id = model_id
        self.client = boto3.Session(profile_name=PROFILE, region_name=REGION).client("bedrock-runtime")
        self.cache = {}

    def _embed(self, text):
        if text not in self.cache:
            response = self.client.invoke_model(modelId=self.model_id, body=json.dumps({"inputText": text}))
            vector = np.array(json.loads(response["body"].read())["embedding"], dtype=float)
            self.cache[text] = vector / np.linalg.norm(vector)
        return self.cache[text]

    def rank(self, query, corpus):
        q = self._embed(query)
        return order({doc_id: float(self._embed(text) @ q) for doc_id, text in corpus.items()})


def evaluate(retriever, cases, filler, k=K):
    """One result row per (case, condition)."""
    rows = []
    for case in cases:
        cid = case["case_id"]
        for cond in CONDITIONS:
            corpus = build_corpus(cases, filler, case, cond)
            ranking = retriever.rank(case["question"], corpus)
            top = ranking[:k]
            top_ids = [d for d, _ in top]
            d1_id = f"{cid}:d1"
            position = next((i for i, (d, _) in enumerate(ranking, 1) if d == d1_id), None)
            rows.append({
                "retriever": retriever.name, "case_id": cid, "tier": case["tier"], "condition": cond,
                "corpus_size": len(corpus), "d1_in_corpus": d1_id in corpus,
                "hit_at_k": (d1_id in top_ids) if d1_id in corpus else "",  # undefined when D1 was removed (C2)
                "d1_rank": position if position else "",
                "d1_score": round(dict(ranking)[d1_id], 4) if d1_id in corpus else "",
                "own_d2_d3_in_top_k": sum(d in (f"{cid}:d2", f"{cid}:d3") for d in top_ids),
                "top_k": "; ".join(f"{d} ({s:.3f})" for d, s in top), "label": LABEL,
            })
    return rows


def md_table(rows, cols):
    return ("| " + " | ".join(cols) + " |\n|" + "|".join("---" for _ in cols) + "|\n"
            + "".join("| " + " | ".join(str(r[c]) for c in cols) + " |\n" for r in rows))


def summarize(rows, name, k, n_cases, corpus_size):
    by = lambda cond: [r for r in rows if r["condition"] == cond]
    recall, rank_row, distract = {"retriever": name}, {"retriever": name}, {"retriever": name}
    for cond in CONDITIONS:
        rs = by(cond)
        if cond == "C2":
            recall[cond] = "n/a (D1 removed)"
            rank_row[cond] = "n/a"
        else:
            recall[cond] = f"{sum(r['hit_at_k'] for r in rs)}/{len(rs)}"
            rank_row[cond] = f"{np.mean([r['d1_rank'] for r in rs]):.2f}"
        distract[cond] = f"{np.mean([r['own_d2_d3_in_top_k'] for r in rs]):.2f}"
    detail = []
    for case_id in dict.fromkeys(r["case_id"] for r in rows):
        row = {"case_id": case_id, "tier": next(r["tier"] for r in rows if r["case_id"] == case_id)}
        for cond in CONDITIONS:
            r = next(x for x in rows if x["case_id"] == case_id and x["condition"] == cond)
            row[cond] = "removed" if r["d1_rank"] == "" else f"rank {r['d1_rank']} ({r['d1_score']:.3f})"
        detail.append(row)
    cols = ["retriever", *CONDITIONS]
    return "\n".join([
        f"# Pilot retrieval ({name}): summary", "", f"**{LABEL.upper()}**", "",
        f"{n_cases} cases, corpus of about {corpus_size} documents (case D1/D2/D3 + filler), k={k}. The query is the "
        "case question. The intervention is applied to the target case's D1 only; the TF-IDF vectorizer is fit once on the "
        "original corpus and kept fixed across conditions.", "",
        f"## recall@{k} (share of cases whose top {k} contain D1)", "", md_table([recall], cols),
        "## Mean rank of D1 (1 = best)", "", md_table([rank_row], cols),
        f"## Mean number of the case's own D2/D3 in the top {k}", "", md_table([distract], cols),
        "## Per case: rank of D1 (cosine score)", "", md_table(detail, ["case_id", "tier", *CONDITIONS]),
        f"_{LABEL}_", ""])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--retriever", choices=["tfidf"], default="tfidf",
                    help="only tfidf is enabled; the embedding retriever needs verification and approval")
    ap.add_argument("--k", type=int, default=K)
    args = ap.parse_args()

    cases, filler = load_cases(), load_filler()
    retriever = TfidfRetriever(build_corpus(cases, filler, cases[0], "C1"))  # fit once on the original corpus
    rows = evaluate(retriever, cases, filler, args.k)
    RESULTS_DIR.mkdir(exist_ok=True)
    csv_path = RESULTS_DIR / f"pilot_retrieval_{retriever.name}.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    corpus_size = len(build_corpus(cases, filler, cases[0], "C1"))
    md_path = RESULTS_DIR / f"pilot_retrieval_{retriever.name}_summary.md"
    md_path.write_text(summarize(rows, retriever.name, args.k, len(cases), corpus_size))
    print(f"{len(rows)} (case, condition) rows; wrote {csv_path.name} and {md_path.name}")


if __name__ == "__main__":
    main()
