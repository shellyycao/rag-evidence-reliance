# rag_gen_v1: RAG-generation vs primary experiment

**RAG-generation mode: secondary analysis, descriptive (TF-IDF top-3, one repeat per cell)**

RAG: 150 calls (top-3 TF-IDF documents, 1 repeat per cell). Primary: 450 calls from `full_v1_combined`, same cases and conditions C1-C5, fixed D1/D2/D3, 3 repeats per cell. Per-call scoring is `evaluate.score_call`. Rates over cases are means of per-case rates, with case-level bootstrap 95% CIs (2000 resamples, seed 590); with few cases per tier these are descriptive only. Reported for all cases, then separately for the 9 pilot-topic cases (which have same-topic hard negatives in the frozen filler) and the 21 new cases (which have none, so D1 retrieval is expected to look easier).

# All cases (30 cases)

### 1. Was D1 retrieved? (RAG only)

D1 in top-3 means the case's own D1, or its modified version in C3-C5, was among the 3 documents sent. In C2 D1 is removed, so this is undefined. If the modified D1 is not retrieved the model never saw the intervention, so the RAG rows of the later tables are also given conditional on retrieval.

| condition | D1 in top-3 | D1 cited | mean D1 rank |
|---|---|---|---|
| C1 | 30/30 | 30/30 | 1.2 |
| C2 | n/a (removed) | 0/30 | n/a |
| C3 | 23/30 | 11/30 | 3.3 |
| C4 | 30/30 | 30/30 | 1.2 |
| C5 | 30/30 | 30/30 | 1.2 |

### 2. Answer type by condition

true value = accepted original answer; false value = the C4 counterfactual; abstained; other = both values, neither value, premise rejected, wrong guess or invalid. Counts out of calls.

| condition | RAG | Primary |
|---|---|---|
| C1 | true 30, false 0, abstained 0, other 0 (of 30) | true 90, false 0, abstained 0, other 0 (of 90) |
| C2 | true 11, false 0, abstained 18, other 1 (of 30) | true 33, false 0, abstained 54, other 3 (of 90) |
| C3 | true 10, false 0, abstained 18, other 2 (of 30) | true 30, false 0, abstained 57, other 3 (of 90) |
| C4 | true 2, false 28, abstained 0, other 0 (of 30) | true 5, false 85, abstained 0, other 0 (of 90) |
| C5 | true 30, false 0, abstained 0, other 0 (of 30) | true 90, false 0, abstained 0, other 0 (of 90) |

### 3. C4 counterfactual-following by tier

Share of C4 calls whose answer is the counterfactual value, per tier. 'RAG, modified D1 retrieved' keeps only RAG C4 calls where the modified D1 was in the top-3. H1 predicts lower following on familiar cases; the 'private' tier holds facts the model does not know.

| tier | Primary | RAG (all C4 calls) | RAG, modified D1 retrieved |
|---|---|---|---|
| familiar | 0.83 [0.60, 1.00] (n=10) | 0.80 [0.50, 1.00] (n=10) | 0.80 [0.50, 1.00] (n=10) |
| obscure | 1.00 [1.00, 1.00] (n=10) | 1.00 [1.00, 1.00] (n=10) | 1.00 [1.00, 1.00] (n=10) |
| private | 1.00 [1.00, 1.00] (n=10) | 1.00 [1.00, 1.00] (n=10) | 1.00 [1.00, 1.00] (n=10) |
| all | 0.94 [0.86, 1.00] (n=30) | 0.93 [0.83, 1.00] (n=30) | 0.93 [0.83, 1.00] (n=30) |

C4 two-dimensional outcome (answer type × conflict_noted), pooled calls:

| mode | C4 outcomes |
|---|---|
| RAG | false value / conflict=False×20, false value / conflict=True×8, true value / conflict=True×2 |
| Primary | false value / conflict=False×61, false value / conflict=True×24, true value / conflict=True×5 |

### 4. Unsupported-citation rate

Among calls that cited at least one document and did not abstain: the share whose citation is 'unsupported' or a 'near-miss (unsupported)' (observed, not a claim about faithfulness). 'No citation' calls are counted separately.

| condition | RAG | Primary |
|---|---|---|
| C1 | 0/30 unsupported; 0 no citation | 0/90 unsupported; 0 no citation |
| C2 | 2/2 unsupported; 25 no citation | 6/6 unsupported; 72 no citation |
| C3 | 4/4 unsupported; 15 no citation | 9/9 unsupported; 46 no citation |
| C4 | 2/30 unsupported; 0 no citation | 5/90 unsupported; 0 no citation |
| C5 | 0/30 unsupported; 0 no citation | 0/90 unsupported; 0 no citation |

### 5. Filler and other-case documents cited (RAG only)

A filler document is one of the 100 frozen filler documents; an other-case document is a D1/D2/D3 of a different case. The primary experiment cannot cite either.

| condition | calls | filler docs cited (total) | calls citing a filler | other-case docs cited (total) |
|---|---|---|---|---|
| C1 | 30 | 0 | 0 | 1 |
| C2 | 30 | 0 | 0 | 1 |
| C3 | 30 | 0 | 0 | 1 |
| C4 | 30 | 0 | 0 | 1 |
| C5 | 30 | 0 | 0 | 1 |
| all | 150 | 0 | 0 | 5 |

### 5b. When D1 was not retrieved (RAG only)

RAG calls whose top-3 did not contain D1 (all of C2, where D1 is removed, plus any C3-C5 call where it dropped out). The model then answers from other documents or from its own knowledge. 'Primary' is the same condition in the fixed-evidence experiment (C2/C3: D1 removed or its target sentence deleted, D2/D3 still shown).

| condition | RAG calls without D1 | answer type | citations | filler / other-case cited | Primary (same condition) |
|---|---|---|---|---|---|
| C2 | 30 | true 11, false 0, abstained 18, other 1 | n/a (abstained)×3, near-miss (unsupported)×1, no citation×25, unsupported×1 | 0 / 1 | true 33, false 0, abstained 54, other 3 |
| C3 | 7 | true 2, false 0, abstained 5, other 0 | n/a (abstained)×2, no citation×5 | 0 / 0 | true 30, false 0, abstained 57, other 3 |

By tier (RAG calls without D1):

| tier | calls | answer type |
|---|---|---|
| familiar | 12 | true 12, false 0, abstained 0, other 0 |
| obscure | 11 | true 1, false 0, abstained 9, other 1 |
| private | 14 | true 0, false 0, abstained 14, other 0 |

### 5c. Conflict noted

`conflict_noted` is the field the model reported, exactly as in the primary experiment; the explanation is not used for the count. Conflict types (exploratory, post hoc) apply to C4 calls with `conflict_noted` true; an empty `conflict_type` cell falls back to the keyword suggestion (the same rules as the primary analysis).

conflict_noted, calls with the field true:

| condition | RAG | Primary |
|---|---|---|
| C1 | 1/30 | 3/90 |
| C2 | 0/30 | 0/90 |
| C3 | 0/30 | 0/90 |
| C4 | 10/30 | 29/90 |
| C5 | 2/30 | 6/90 |

C4 outcome × conflict_noted by tier:

| tier | RAG | Primary |
|---|---|---|
| familiar | false value / conflict=False×1, false value / conflict=True×7, true value / conflict=True×2 | false value / conflict=False×4, false value / conflict=True×21, true value / conflict=True×5 |
| obscure | false value / conflict=False×9, false value / conflict=True×1 | false value / conflict=False×27, false value / conflict=True×3 |
| private | false value / conflict=False×10 | false value / conflict=False×30 |

Conflict types:

| mode | conflict_type of C4 calls with conflict_noted |
|---|---|
| RAG | called_document_false×6, noted_discrepancy×3, other_conflict×1 |
| Primary | called_document_false×15, deferred_to_document×5, noted_discrepancy×6, other_conflict×3 |

### 6. Cost and review status

RAG run: 150 calls, estimated $0.877. 9 calls flagged for manual review (`rag_gen_v1_review.csv`), 0 'other' rows awaiting a review_label; until they are labeled they count as 'other'.

_RAG-generation mode: secondary analysis, descriptive (TF-IDF top-3, one repeat per cell)_

# The 9 cases with same-topic hard negatives (9 cases)

### 1. Was D1 retrieved? (RAG only)

D1 in top-3 means the case's own D1, or its modified version in C3-C5, was among the 3 documents sent. In C2 D1 is removed, so this is undefined. If the modified D1 is not retrieved the model never saw the intervention, so the RAG rows of the later tables are also given conditional on retrieval.

| condition | D1 in top-3 | D1 cited | mean D1 rank |
|---|---|---|---|
| C1 | 9/9 | 9/9 | 1.2 |
| C2 | n/a (removed) | 0/9 | n/a |
| C3 | 6/9 | 2/9 | 5.3 |
| C4 | 9/9 | 9/9 | 1.1 |
| C5 | 9/9 | 9/9 | 1.2 |

### 2. Answer type by condition

true value = accepted original answer; false value = the C4 counterfactual; abstained; other = both values, neither value, premise rejected, wrong guess or invalid. Counts out of calls.

| condition | RAG | Primary |
|---|---|---|
| C1 | true 9, false 0, abstained 0, other 0 (of 9) | true 27, false 0, abstained 0, other 0 (of 27) |
| C2 | true 3, false 0, abstained 6, other 0 (of 9) | true 9, false 0, abstained 15, other 3 (of 27) |
| C3 | true 3, false 0, abstained 6, other 0 (of 9) | true 9, false 0, abstained 18, other 0 (of 27) |
| C4 | true 1, false 8, abstained 0, other 0 (of 9) | true 3, false 24, abstained 0, other 0 (of 27) |
| C5 | true 9, false 0, abstained 0, other 0 (of 9) | true 27, false 0, abstained 0, other 0 (of 27) |

### 3. C4 counterfactual-following by tier

Share of C4 calls whose answer is the counterfactual value, per tier. 'RAG, modified D1 retrieved' keeps only RAG C4 calls where the modified D1 was in the top-3. H1 predicts lower following on familiar cases; the 'private' tier holds facts the model does not know.

| tier | Primary | RAG (all C4 calls) | RAG, modified D1 retrieved |
|---|---|---|---|
| familiar | 0.67 [0.00, 1.00] (n=3) | 0.67 [0.00, 1.00] (n=3) | 0.67 [0.00, 1.00] (n=3) |
| obscure | 1.00 [1.00, 1.00] (n=3) | 1.00 [1.00, 1.00] (n=3) | 1.00 [1.00, 1.00] (n=3) |
| private | 1.00 [1.00, 1.00] (n=3) | 1.00 [1.00, 1.00] (n=3) | 1.00 [1.00, 1.00] (n=3) |
| all | 0.89 [0.67, 1.00] (n=9) | 0.89 [0.67, 1.00] (n=9) | 0.89 [0.67, 1.00] (n=9) |

C4 two-dimensional outcome (answer type × conflict_noted), pooled calls:

| mode | C4 outcomes |
|---|---|
| RAG | false value / conflict=False×6, false value / conflict=True×2, true value / conflict=True×1 |
| Primary | false value / conflict=False×18, false value / conflict=True×6, true value / conflict=True×3 |

### 4. Unsupported-citation rate

Among calls that cited at least one document and did not abstain: the share whose citation is 'unsupported' or a 'near-miss (unsupported)' (observed, not a claim about faithfulness). 'No citation' calls are counted separately.

| condition | RAG | Primary |
|---|---|---|
| C1 | 0/9 unsupported; 0 no citation | 0/27 unsupported; 0 no citation |
| C2 | n/a unsupported; 8 no citation | 3/3 unsupported; 18 no citation |
| C3 | n/a unsupported; 5 no citation | n/a unsupported; 19 no citation |
| C4 | 1/9 unsupported; 0 no citation | 3/27 unsupported; 0 no citation |
| C5 | 0/9 unsupported; 0 no citation | 0/27 unsupported; 0 no citation |

### 5. Filler and other-case documents cited (RAG only)

A filler document is one of the 100 frozen filler documents; an other-case document is a D1/D2/D3 of a different case. The primary experiment cannot cite either.

| condition | calls | filler docs cited (total) | calls citing a filler | other-case docs cited (total) |
|---|---|---|---|---|
| C1 | 9 | 0 | 0 | 0 |
| C2 | 9 | 0 | 0 | 0 |
| C3 | 9 | 0 | 0 | 0 |
| C4 | 9 | 0 | 0 | 0 |
| C5 | 9 | 0 | 0 | 0 |
| all | 45 | 0 | 0 | 0 |

### 5b. When D1 was not retrieved (RAG only)

RAG calls whose top-3 did not contain D1 (all of C2, where D1 is removed, plus any C3-C5 call where it dropped out). The model then answers from other documents or from its own knowledge. 'Primary' is the same condition in the fixed-evidence experiment (C2/C3: D1 removed or its target sentence deleted, D2/D3 still shown).

| condition | RAG calls without D1 | answer type | citations | filler / other-case cited | Primary (same condition) |
|---|---|---|---|---|---|
| C2 | 9 | true 3, false 0, abstained 6, other 0 | n/a (abstained)×1, no citation×8 | 0 / 0 | true 9, false 0, abstained 15, other 3 |
| C3 | 3 | true 1, false 0, abstained 2, other 0 | n/a (abstained)×2, no citation×1 | 0 / 0 | true 9, false 0, abstained 18, other 0 |

By tier (RAG calls without D1):

| tier | calls | answer type |
|---|---|---|
| familiar | 4 | true 4, false 0, abstained 0, other 0 |
| obscure | 4 | true 0, false 0, abstained 4, other 0 |
| private | 4 | true 0, false 0, abstained 4, other 0 |

### 5c. Conflict noted

`conflict_noted` is the field the model reported, exactly as in the primary experiment; the explanation is not used for the count. Conflict types (exploratory, post hoc) apply to C4 calls with `conflict_noted` true; an empty `conflict_type` cell falls back to the keyword suggestion (the same rules as the primary analysis).

conflict_noted, calls with the field true:

| condition | RAG | Primary |
|---|---|---|
| C1 | 0/9 | 0/27 |
| C2 | 0/9 | 0/27 |
| C3 | 0/9 | 0/27 |
| C4 | 3/9 | 9/27 |
| C5 | 1/9 | 0/27 |

C4 outcome × conflict_noted by tier:

| tier | RAG | Primary |
|---|---|---|
| familiar | false value / conflict=False×1, false value / conflict=True×1, true value / conflict=True×1 | false value / conflict=False×3, false value / conflict=True×3, true value / conflict=True×3 |
| obscure | false value / conflict=False×2, false value / conflict=True×1 | false value / conflict=False×6, false value / conflict=True×3 |
| private | false value / conflict=False×3 | false value / conflict=False×9 |

Conflict types:

| mode | conflict_type of C4 calls with conflict_noted |
|---|---|
| RAG | called_document_false×2, other_conflict×1 |
| Primary | called_document_false×3, noted_discrepancy×3, other_conflict×3 |

### 6. Cost and review status

RAG run: 45 calls, estimated $0.268. 1 calls flagged for manual review (`rag_gen_v1_review.csv`), 0 'other' rows awaiting a review_label; until they are labeled they count as 'other'.

_RAG-generation mode: secondary analysis, descriptive (TF-IDF top-3, one repeat per cell)_

# The 21 new cases without hard negatives (21 cases)

### 1. Was D1 retrieved? (RAG only)

D1 in top-3 means the case's own D1, or its modified version in C3-C5, was among the 3 documents sent. In C2 D1 is removed, so this is undefined. If the modified D1 is not retrieved the model never saw the intervention, so the RAG rows of the later tables are also given conditional on retrieval.

| condition | D1 in top-3 | D1 cited | mean D1 rank |
|---|---|---|---|
| C1 | 21/21 | 21/21 | 1.2 |
| C2 | n/a (removed) | 0/21 | n/a |
| C3 | 17/21 | 9/21 | 2.4 |
| C4 | 21/21 | 21/21 | 1.2 |
| C5 | 21/21 | 21/21 | 1.2 |

### 2. Answer type by condition

true value = accepted original answer; false value = the C4 counterfactual; abstained; other = both values, neither value, premise rejected, wrong guess or invalid. Counts out of calls.

| condition | RAG | Primary |
|---|---|---|
| C1 | true 21, false 0, abstained 0, other 0 (of 21) | true 63, false 0, abstained 0, other 0 (of 63) |
| C2 | true 8, false 0, abstained 12, other 1 (of 21) | true 24, false 0, abstained 39, other 0 (of 63) |
| C3 | true 7, false 0, abstained 12, other 2 (of 21) | true 21, false 0, abstained 39, other 3 (of 63) |
| C4 | true 1, false 20, abstained 0, other 0 (of 21) | true 2, false 61, abstained 0, other 0 (of 63) |
| C5 | true 21, false 0, abstained 0, other 0 (of 21) | true 63, false 0, abstained 0, other 0 (of 63) |

### 3. C4 counterfactual-following by tier

Share of C4 calls whose answer is the counterfactual value, per tier. 'RAG, modified D1 retrieved' keeps only RAG C4 calls where the modified D1 was in the top-3. H1 predicts lower following on familiar cases; the 'private' tier holds facts the model does not know.

| tier | Primary | RAG (all C4 calls) | RAG, modified D1 retrieved |
|---|---|---|---|
| familiar | 0.90 [0.71, 1.00] (n=7) | 0.86 [0.57, 1.00] (n=7) | 0.86 [0.57, 1.00] (n=7) |
| obscure | 1.00 [1.00, 1.00] (n=7) | 1.00 [1.00, 1.00] (n=7) | 1.00 [1.00, 1.00] (n=7) |
| private | 1.00 [1.00, 1.00] (n=7) | 1.00 [1.00, 1.00] (n=7) | 1.00 [1.00, 1.00] (n=7) |
| all | 0.97 [0.90, 1.00] (n=21) | 0.95 [0.86, 1.00] (n=21) | 0.95 [0.86, 1.00] (n=21) |

C4 two-dimensional outcome (answer type × conflict_noted), pooled calls:

| mode | C4 outcomes |
|---|---|
| RAG | false value / conflict=False×14, false value / conflict=True×6, true value / conflict=True×1 |
| Primary | false value / conflict=False×43, false value / conflict=True×18, true value / conflict=True×2 |

### 4. Unsupported-citation rate

Among calls that cited at least one document and did not abstain: the share whose citation is 'unsupported' or a 'near-miss (unsupported)' (observed, not a claim about faithfulness). 'No citation' calls are counted separately.

| condition | RAG | Primary |
|---|---|---|
| C1 | 0/21 unsupported; 0 no citation | 0/63 unsupported; 0 no citation |
| C2 | 2/2 unsupported; 17 no citation | 3/3 unsupported; 54 no citation |
| C3 | 4/4 unsupported; 10 no citation | 9/9 unsupported; 27 no citation |
| C4 | 1/21 unsupported; 0 no citation | 2/63 unsupported; 0 no citation |
| C5 | 0/21 unsupported; 0 no citation | 0/63 unsupported; 0 no citation |

### 5. Filler and other-case documents cited (RAG only)

A filler document is one of the 100 frozen filler documents; an other-case document is a D1/D2/D3 of a different case. The primary experiment cannot cite either.

| condition | calls | filler docs cited (total) | calls citing a filler | other-case docs cited (total) |
|---|---|---|---|---|
| C1 | 21 | 0 | 0 | 1 |
| C2 | 21 | 0 | 0 | 1 |
| C3 | 21 | 0 | 0 | 1 |
| C4 | 21 | 0 | 0 | 1 |
| C5 | 21 | 0 | 0 | 1 |
| all | 105 | 0 | 0 | 5 |

### 5b. When D1 was not retrieved (RAG only)

RAG calls whose top-3 did not contain D1 (all of C2, where D1 is removed, plus any C3-C5 call where it dropped out). The model then answers from other documents or from its own knowledge. 'Primary' is the same condition in the fixed-evidence experiment (C2/C3: D1 removed or its target sentence deleted, D2/D3 still shown).

| condition | RAG calls without D1 | answer type | citations | filler / other-case cited | Primary (same condition) |
|---|---|---|---|---|---|
| C2 | 21 | true 8, false 0, abstained 12, other 1 | n/a (abstained)×2, near-miss (unsupported)×1, no citation×17, unsupported×1 | 0 / 1 | true 24, false 0, abstained 39, other 0 |
| C3 | 4 | true 1, false 0, abstained 3, other 0 | no citation×4 | 0 / 0 | true 21, false 0, abstained 39, other 3 |

By tier (RAG calls without D1):

| tier | calls | answer type |
|---|---|---|
| familiar | 8 | true 8, false 0, abstained 0, other 0 |
| obscure | 7 | true 1, false 0, abstained 5, other 1 |
| private | 10 | true 0, false 0, abstained 10, other 0 |

### 5c. Conflict noted

`conflict_noted` is the field the model reported, exactly as in the primary experiment; the explanation is not used for the count. Conflict types (exploratory, post hoc) apply to C4 calls with `conflict_noted` true; an empty `conflict_type` cell falls back to the keyword suggestion (the same rules as the primary analysis).

conflict_noted, calls with the field true:

| condition | RAG | Primary |
|---|---|---|
| C1 | 1/21 | 3/63 |
| C2 | 0/21 | 0/63 |
| C3 | 0/21 | 0/63 |
| C4 | 7/21 | 20/63 |
| C5 | 1/21 | 6/63 |

C4 outcome × conflict_noted by tier:

| tier | RAG | Primary |
|---|---|---|
| familiar | false value / conflict=True×6, true value / conflict=True×1 | false value / conflict=False×1, false value / conflict=True×18, true value / conflict=True×2 |
| obscure | false value / conflict=False×7 | false value / conflict=False×21 |
| private | false value / conflict=False×7 | false value / conflict=False×21 |

Conflict types:

| mode | conflict_type of C4 calls with conflict_noted |
|---|---|
| RAG | called_document_false×4, noted_discrepancy×3 |
| Primary | called_document_false×12, deferred_to_document×5, noted_discrepancy×3 |

### 6. Cost and review status

RAG run: 105 calls, estimated $0.609. 8 calls flagged for manual review (`rag_gen_v1_review.csv`), 0 'other' rows awaiting a review_label; until they are labeled they count as 'other'.

_RAG-generation mode: secondary analysis, descriptive (TF-IDF top-3, one repeat per cell)_
