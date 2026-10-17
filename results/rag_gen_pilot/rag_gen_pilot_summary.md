# rag_gen_pilot: RAG-generation vs primary experiment

**RAG-generation PILOT: pipeline test, not findings**

RAG: 6 calls (top-3 TF-IDF documents, 1 repeat per cell). Primary: 45 calls from `full_v1_combined`, same cases and conditions C1-C5, fixed D1/D2/D3, 3 repeats per cell. Per-call scoring is `evaluate.score_call`. Rates over cases are means of per-case rates, with case-level bootstrap 95% CIs (2000 resamples, seed 590); with few cases per tier these are descriptive only. Reported for all cases, then separately for the 9 pilot-topic cases (which have same-topic hard negatives in the frozen filler) and the 21 new cases (which have none, so D1 retrieval is expected to look easier).

# All cases (3 cases)

### 1. Was D1 retrieved? (RAG only)

D1 in top-3 means the case's own D1, or its modified version in C3-C5, was among the 3 documents sent. In C2 D1 is removed, so this is undefined. If the modified D1 is not retrieved the model never saw the intervention, so the RAG rows of the later tables are also given conditional on retrieval.

| condition | D1 in top-3 | D1 cited | mean D1 rank |
|---|---|---|---|
| C1 | 3/3 | 3/3 | 1.7 |
| C2 | n/a (removed) | n/a | n/a |
| C3 | n/a | n/a | n/a |
| C4 | 3/3 | 3/3 | 1.3 |
| C5 | n/a | n/a | n/a |

### 2. Answer type by condition

true value = accepted original answer; false value = the C4 counterfactual; abstained; other = both values, neither value, premise rejected, wrong guess or invalid. Counts out of calls.

| condition | RAG | Primary |
|---|---|---|
| C1 | true 3, false 0, abstained 0, other 0 (of 3) | true 9, false 0, abstained 0, other 0 (of 9) |
| C2 | true 0, false 0, abstained 0, other 0 (of 0) | true 3, false 0, abstained 6, other 0 (of 9) |
| C3 | true 0, false 0, abstained 0, other 0 (of 0) | true 3, false 0, abstained 6, other 0 (of 9) |
| C4 | true 0, false 3, abstained 0, other 0 (of 3) | true 0, false 9, abstained 0, other 0 (of 9) |
| C5 | true 0, false 0, abstained 0, other 0 (of 0) | true 9, false 0, abstained 0, other 0 (of 9) |

### 3. C4 counterfactual-following by tier

Share of C4 calls whose answer is the counterfactual value, per tier. 'RAG, modified D1 retrieved' keeps only RAG C4 calls where the modified D1 was in the top-3. H1 predicts lower following on familiar cases; the 'private' tier holds facts the model does not know.

| tier | Primary | RAG (all C4 calls) | RAG, modified D1 retrieved |
|---|---|---|---|
| familiar | 1.00 [1.00, 1.00] (n=1) | 1.00 [1.00, 1.00] (n=1) | 1.00 [1.00, 1.00] (n=1) |
| obscure | 1.00 [1.00, 1.00] (n=1) | 1.00 [1.00, 1.00] (n=1) | 1.00 [1.00, 1.00] (n=1) |
| private | 1.00 [1.00, 1.00] (n=1) | 1.00 [1.00, 1.00] (n=1) | 1.00 [1.00, 1.00] (n=1) |
| all | 1.00 [1.00, 1.00] (n=3) | 1.00 [1.00, 1.00] (n=3) | 1.00 [1.00, 1.00] (n=3) |

C4 two-dimensional outcome (answer type × conflict_noted), pooled calls:

| mode | C4 outcomes |
|---|---|
| RAG | false value / conflict=False×3 |
| Primary | false value / conflict=False×9 |

### 4. Unsupported-citation rate

Among calls that cited at least one document and did not abstain: the share whose citation is 'unsupported' or a 'near-miss (unsupported)' (observed, not a claim about faithfulness). 'No citation' calls are counted separately.

| condition | RAG | Primary |
|---|---|---|
| C1 | 0/3 unsupported; 0 no citation | 0/9 unsupported; 0 no citation |
| C2 | n/a unsupported; 0 no citation | n/a unsupported; 6 no citation |
| C3 | n/a unsupported; 0 no citation | n/a unsupported; 4 no citation |
| C4 | 0/3 unsupported; 0 no citation | 0/9 unsupported; 0 no citation |
| C5 | n/a unsupported; 0 no citation | 0/9 unsupported; 0 no citation |

### 5. Filler and other-case documents cited (RAG only)

A filler document is one of the 100 frozen filler documents; an other-case document is a D1/D2/D3 of a different case. The primary experiment cannot cite either.

| condition | calls | filler docs cited (total) | calls citing a filler | other-case docs cited (total) |
|---|---|---|---|---|
| C1 | 3 | 0 | 0 | 0 |
| C2 | 0 | 0 | 0 | 0 |
| C3 | 0 | 0 | 0 | 0 |
| C4 | 3 | 0 | 0 | 0 |
| C5 | 0 | 0 | 0 | 0 |
| all | 6 | 0 | 0 | 0 |

### 6. Cost and review status

RAG run: 6 calls, estimated $0.033. 0 calls flagged for manual review (`rag_gen_pilot_review.csv`), 0 'other' rows awaiting a review_label; until they are labeled they count as 'other'.

_RAG-generation PILOT: pipeline test, not findings_

# The 9 cases with same-topic hard negatives (3 cases)

### 1. Was D1 retrieved? (RAG only)

D1 in top-3 means the case's own D1, or its modified version in C3-C5, was among the 3 documents sent. In C2 D1 is removed, so this is undefined. If the modified D1 is not retrieved the model never saw the intervention, so the RAG rows of the later tables are also given conditional on retrieval.

| condition | D1 in top-3 | D1 cited | mean D1 rank |
|---|---|---|---|
| C1 | 3/3 | 3/3 | 1.7 |
| C2 | n/a (removed) | n/a | n/a |
| C3 | n/a | n/a | n/a |
| C4 | 3/3 | 3/3 | 1.3 |
| C5 | n/a | n/a | n/a |

### 2. Answer type by condition

true value = accepted original answer; false value = the C4 counterfactual; abstained; other = both values, neither value, premise rejected, wrong guess or invalid. Counts out of calls.

| condition | RAG | Primary |
|---|---|---|
| C1 | true 3, false 0, abstained 0, other 0 (of 3) | true 9, false 0, abstained 0, other 0 (of 9) |
| C2 | true 0, false 0, abstained 0, other 0 (of 0) | true 3, false 0, abstained 6, other 0 (of 9) |
| C3 | true 0, false 0, abstained 0, other 0 (of 0) | true 3, false 0, abstained 6, other 0 (of 9) |
| C4 | true 0, false 3, abstained 0, other 0 (of 3) | true 0, false 9, abstained 0, other 0 (of 9) |
| C5 | true 0, false 0, abstained 0, other 0 (of 0) | true 9, false 0, abstained 0, other 0 (of 9) |

### 3. C4 counterfactual-following by tier

Share of C4 calls whose answer is the counterfactual value, per tier. 'RAG, modified D1 retrieved' keeps only RAG C4 calls where the modified D1 was in the top-3. H1 predicts lower following on familiar cases; the 'private' tier holds facts the model does not know.

| tier | Primary | RAG (all C4 calls) | RAG, modified D1 retrieved |
|---|---|---|---|
| familiar | 1.00 [1.00, 1.00] (n=1) | 1.00 [1.00, 1.00] (n=1) | 1.00 [1.00, 1.00] (n=1) |
| obscure | 1.00 [1.00, 1.00] (n=1) | 1.00 [1.00, 1.00] (n=1) | 1.00 [1.00, 1.00] (n=1) |
| private | 1.00 [1.00, 1.00] (n=1) | 1.00 [1.00, 1.00] (n=1) | 1.00 [1.00, 1.00] (n=1) |
| all | 1.00 [1.00, 1.00] (n=3) | 1.00 [1.00, 1.00] (n=3) | 1.00 [1.00, 1.00] (n=3) |

C4 two-dimensional outcome (answer type × conflict_noted), pooled calls:

| mode | C4 outcomes |
|---|---|
| RAG | false value / conflict=False×3 |
| Primary | false value / conflict=False×9 |

### 4. Unsupported-citation rate

Among calls that cited at least one document and did not abstain: the share whose citation is 'unsupported' or a 'near-miss (unsupported)' (observed, not a claim about faithfulness). 'No citation' calls are counted separately.

| condition | RAG | Primary |
|---|---|---|
| C1 | 0/3 unsupported; 0 no citation | 0/9 unsupported; 0 no citation |
| C2 | n/a unsupported; 0 no citation | n/a unsupported; 6 no citation |
| C3 | n/a unsupported; 0 no citation | n/a unsupported; 4 no citation |
| C4 | 0/3 unsupported; 0 no citation | 0/9 unsupported; 0 no citation |
| C5 | n/a unsupported; 0 no citation | 0/9 unsupported; 0 no citation |

### 5. Filler and other-case documents cited (RAG only)

A filler document is one of the 100 frozen filler documents; an other-case document is a D1/D2/D3 of a different case. The primary experiment cannot cite either.

| condition | calls | filler docs cited (total) | calls citing a filler | other-case docs cited (total) |
|---|---|---|---|---|
| C1 | 3 | 0 | 0 | 0 |
| C2 | 0 | 0 | 0 | 0 |
| C3 | 0 | 0 | 0 | 0 |
| C4 | 3 | 0 | 0 | 0 |
| C5 | 0 | 0 | 0 | 0 |
| all | 6 | 0 | 0 | 0 |

### 6. Cost and review status

RAG run: 6 calls, estimated $0.033. 0 calls flagged for manual review (`rag_gen_pilot_review.csv`), 0 'other' rows awaiting a review_label; until they are labeled they count as 'other'.

_RAG-generation PILOT: pipeline test, not findings_
