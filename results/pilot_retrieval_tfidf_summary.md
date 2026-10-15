# Pilot retrieval (tfidf): summary

**PILOT — PIPELINE TEST, NOT FINDINGS**

9 cases, corpus of about 127 documents (case D1/D2/D3 + filler), k=3. The query is the case question. The intervention is applied to the target case's D1 only; the TF-IDF vectorizer is fit once on the original corpus and kept fixed across conditions.

## recall@3 (share of cases whose top 3 contain D1)

| retriever | C1 | C2 | C3 | C4 | C5 |
|---|---|---|---|---|---|
| tfidf | 9/9 | n/a (D1 removed) | 7/9 | 9/9 | 9/9 |

## Mean rank of D1 (1 = best)

| retriever | C1 | C2 | C3 | C4 | C5 |
|---|---|---|---|---|---|
| tfidf | 1.11 | n/a | 3.56 | 1.11 | 1.11 |

## Mean number of the case's own D2/D3 in the top 3

| retriever | C1 | C2 | C3 | C4 | C5 |
|---|---|---|---|---|---|
| tfidf | 0.56 | 0.67 | 0.56 | 0.56 | 0.56 |

## Per case: rank of D1 (cosine score)

| case_id | tier | C1 | C2 | C3 | C4 | C5 |
|---|---|---|---|---|---|---|
| F3 | familiar | rank 1 (0.484) | removed | rank 14 (0.000) | rank 1 (0.504) | rank 1 (0.465) |
| F5 | familiar | rank 1 (0.434) | removed | rank 3 (0.350) | rank 1 (0.502) | rank 1 (0.449) |
| F6 | familiar | rank 1 (0.479) | removed | rank 1 (0.518) | rank 1 (0.497) | rank 1 (0.479) |
| O11 | obscure | rank 2 (0.328) | removed | rank 2 (0.265) | rank 2 (0.358) | rank 2 (0.339) |
| O12 | obscure | rank 1 (0.558) | removed | rank 5 (0.176) | rank 1 (0.558) | rank 1 (0.594) |
| O13 | obscure | rank 1 (0.605) | removed | rank 1 (0.242) | rank 1 (0.634) | rank 1 (0.617) |
| P1 | private | rank 1 (0.526) | removed | rank 3 (0.201) | rank 1 (0.564) | rank 1 (0.526) |
| P2 | private | rank 1 (0.684) | removed | rank 2 (0.265) | rank 1 (0.705) | rank 1 (0.684) |
| P3 | private | rank 1 (0.579) | removed | rank 1 (0.577) | rank 1 (0.609) | rank 1 (0.609) |

_pilot — pipeline test, not findings_
