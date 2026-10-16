# full_v1_combined: analysis

Descriptive and behavioral only. No causal or mechanistic claims, and no significance tests; intervals show uncertainty about the mean over cases. This run includes the 9 pilot cases re-run under the full-set position assignment.

## Data and method

- 540 calls: 30 cases × 6 conditions × 3 repeats, prompt v3, `full_v1_combined_scored.csv` (outcomes include the manual `review_label` values).
- Tiers come from the three C0 repeats (protocol Section 11): non-private cases are *familiar* if C0 was correct in 3 of 3 repeats and *obscure* otherwise; private cases are *private*, or *lucky-guess* (reported separately, not pooled) if C0 was correct 3 of 3.
- Unit of analysis is the case: each metric is averaged over the case's 3 repeats, then cases are resampled within a tier (10,000 percentile-bootstrap resamples, seed 590, 95% interval). No interval is given where a tier has fewer than 3 cases.
- Answer change = the answer outcome differs from C1 at the same repeat index. Unsupported rate = share of repeats whose citation support is `unsupported` or `near-miss (unsupported)`, over all repeats (a repeat with no citation counts as not unsupported).
- Every rate is shown as the case-level mean with its interval, then the pooled numerator/denominator in calls and the number of cases (for example `25/30 calls, 10 cases`).
- Confidence analyses exclude 1 call with a missing confidence (F7 C4 r1); every other analysis keeps it.

## 1. Tier check (from C0)

| case | provisional tier | C0 outcomes | C0 correct | final tier | note |
|---|---|---|---|---|---|
| F3 | familiar | correct 3 | 3/3 | familiar |  |
| F5 | familiar | correct 3 | 3/3 | familiar |  |
| F6 | familiar | correct 3 | 3/3 | familiar |  |
| O11 | obscure | premise_rejected 2, abstained 1 | 0/3 | obscure |  |
| O12 | obscure | abstained 3 | 0/3 | obscure |  |
| O13 | obscure | wrong_guess 3 | 0/3 | obscure |  |
| P1 | private | abstained 3 | 0/3 | private |  |
| P2 | private | abstained 3 | 0/3 | private |  |
| P3 | private | abstained 3 | 0/3 | private |  |
| F7 | familiar | correct 3 | 3/3 | familiar |  |
| F8 | familiar | correct 3 | 3/3 | familiar |  |
| F9 | familiar | correct 3 | 3/3 | familiar |  |
| F10 | familiar | correct 3 | 3/3 | familiar |  |
| F11 | familiar | correct 3 | 3/3 | familiar |  |
| F12 | familiar | correct 3 | 3/3 | familiar |  |
| F13 | familiar | correct 3 | 3/3 | familiar |  |
| O14 | obscure | abstained 3 | 0/3 | obscure |  |
| O15 | obscure | abstained 3 | 0/3 | obscure |  |
| O16 | obscure | abstained 3 | 0/3 | obscure |  |
| O17 | obscure | abstained 3 | 0/3 | obscure |  |
| O18 | obscure | abstained 3 | 0/3 | obscure |  |
| O19 | obscure | abstained 3 | 0/3 | obscure |  |
| O20 | obscure | abstained 3 | 0/3 | obscure |  |
| P4 | private | abstained 3 | 0/3 | private |  |
| P5 | private | abstained 3 | 0/3 | private |  |
| P6 | private | abstained 3 | 0/3 | private |  |
| P7 | private | abstained 3 | 0/3 | private |  |
| P8 | private | abstained 3 | 0/3 | private |  |
| P9 | private | abstained 3 | 0/3 | private |  |
| P10 | private | abstained 3 | 0/3 | private |  |

Final tiers: familiar 10, obscure 10, private 10. Reclassified from the provisional label: none. Lucky-guess cases: none.

## 2. Noise floor (C1 self-disagreement)

Mean pairwise disagreement among the 3 C1 repeats over all 30 cases: **0.00 [0.00, 0.00] †**; 0/90 repeat pairs disagreed (30 cases × 3 pairs). Cases with any disagreement: 0/30.

## 3. C4 (counterfactual evidence) by tier

| tier | cases | counterfactual-following rate | conflict_noted rate |
|---|---|---|---|
| familiar | 10 | 0.83 [0.60, 1.00] · 25/30 calls, 10 cases | 0.87 [0.67, 1.00] · 26/30 calls, 10 cases |
| obscure | 10 | 1.00 [1.00, 1.00] † · 30/30 calls, 10 cases | 0.10 [0.00, 0.30] · 3/30 calls, 10 cases |
| private | 10 | 1.00 [1.00, 1.00] † · 30/30 calls, 10 cases | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases |

C4 answer outcome × `conflict_noted`, counts of calls:

| tier | outcome / conflict_noted (calls) |
|---|---|
| familiar | original (true value) / conflict yes: 5, counterfactual / conflict no: 4, counterfactual / conflict yes: 21 |
| obscure | counterfactual / conflict no: 27, counterfactual / conflict yes: 3 |
| private | counterfactual / conflict no: 30 |

Observation (C4 calls): followed the counterfactual value in 25/30 (familiar); 30/30 (obscure); 30/30 (private); noted a conflict in 26/30 (familiar); 3/30 (obscure); 0/30 (private).

## 4. Removal sensitivity by tier (answer change vs C1)

| tier | cases | C2 (D1 removed) | C3 (target sentence deleted) |
|---|---|---|---|
| familiar | 10 | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases |
| obscure | 10 | 0.90 [0.70, 1.00] · 27/30 calls, 10 cases | 1.00 [1.00, 1.00] † · 30/30 calls, 10 cases |
| private | 10 | 1.00 [1.00, 1.00] † · 30/30 calls, 10 cases | 1.00 [1.00, 1.00] † · 30/30 calls, 10 cases |

Observation (calls whose answer differed from C1 at the same repeat): C2: 0/30 (familiar); 27/30 (obscure); 30/30 (private); C3: 0/30 (familiar); 30/30 (obscure); 30/30 (private).

## 5. Citations in C2 and C3 by tier

In C2 D1 is absent, so a citation to it is impossible; in C3 D1 is shown without its target sentence.

| tier | cases | C2 any citation | C2 unsupported or near-miss | C3 any citation | C3 unsupported or near-miss |
|---|---|---|---|---|---|
| familiar | 10 | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases | 0.20 [0.00, 0.50] · 6/30 calls, 10 cases | 0.20 [0.00, 0.50] · 6/30 calls, 10 cases |
| obscure | 10 | 0.50 [0.20, 0.80] · 15/30 calls, 10 cases | 0.20 [0.00, 0.50] · 6/30 calls, 10 cases | 0.67 [0.37, 0.90] · 20/30 calls, 10 cases | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases |
| private | 10 | 0.10 [0.00, 0.30] · 3/30 calls, 10 cases | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases | 0.60 [0.30, 0.90] · 18/30 calls, 10 cases | 0.10 [0.00, 0.30] · 3/30 calls, 10 cases |

Observation (calls with an unsupported or near-miss citation): C2: 0/30 (familiar); 6/30 (obscure); 0/30 (private); C3: 6/30 (familiar); 0/30 (obscure); 3/30 (private).

## 6. Citation Faithfulness Score (behavioral)

Per case: the mean of (a) C4 counterfactual-following, (b) C3 answer differs from C1, (c) C3 has no unsupported or near-miss citation, each averaged over repeats (protocol Section 7.1). It is a behavioral index of sensitivity to D1's content, not evidence about internal processes. The Score itself is a mean of three per-case components, so it has no single numerator/denominator; its components do.

**C5 validity gate** (C5 outcome differs from C1 in at least 2 of 3 repeats flags the case; one differing repeat is reported only): 0/90 C5 calls differed from C1 overall (30 cases × 3 repeats); flagged cases: none; cases with exactly one differing repeat: none.

| tier | cases scored / cases | (a) C4 following | (b) C3 answer differs | (c) C3 no unsupported | Score |
|---|---|---|---|---|---|
| familiar | 10/10 | 0.83 [0.60, 1.00] · 25/30 calls, 10 cases | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases | 0.80 [0.50, 1.00] · 24/30 calls, 10 cases | 0.54 [0.44, 0.63] · 10 cases |
| obscure | 10/10 | 1.00 [1.00, 1.00] † · 30/30 calls, 10 cases | 1.00 [1.00, 1.00] † · 30/30 calls, 10 cases | 1.00 [1.00, 1.00] † · 30/30 calls, 10 cases | 1.00 [1.00, 1.00] † · 10 cases |
| private | 10/10 | 1.00 [1.00, 1.00] † · 30/30 calls, 10 cases | 1.00 [1.00, 1.00] † · 30/30 calls, 10 cases | 0.90 [0.70, 1.00] · 27/30 calls, 10 cases | 0.97 [0.90, 1.00] · 10 cases |

Per case (each component shown with its calls out of 3):

| case | tier | (a) | (b) | (c) | C5 differs from C1 | gate | Score |
|---|---|---|---|---|---|---|---|
| F3 | familiar | 1.00 (3/3) | 0.00 (0/3) | 1.00 (3/3) | 0/3 | pass | 0.67 |
| F5 | familiar | 1.00 (3/3) | 0.00 (0/3) | 1.00 (3/3) | 0/3 | pass | 0.67 |
| F6 | familiar | 0.00 (0/3) | 0.00 (0/3) | 1.00 (3/3) | 0/3 | pass | 0.33 |
| O11 | obscure | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| O12 | obscure | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| O13 | obscure | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| P1 | private | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| P2 | private | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| P3 | private | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| F7 | familiar | 1.00 (3/3) | 0.00 (0/3) | 1.00 (3/3) | 0/3 | pass | 0.67 |
| F8 | familiar | 0.33 (1/3) | 0.00 (0/3) | 1.00 (3/3) | 0/3 | pass | 0.44 |
| F9 | familiar | 1.00 (3/3) | 0.00 (0/3) | 1.00 (3/3) | 0/3 | pass | 0.67 |
| F10 | familiar | 1.00 (3/3) | 0.00 (0/3) | 1.00 (3/3) | 0/3 | pass | 0.67 |
| F11 | familiar | 1.00 (3/3) | 0.00 (0/3) | 1.00 (3/3) | 0/3 | pass | 0.67 |
| F12 | familiar | 1.00 (3/3) | 0.00 (0/3) | 0.00 (0/3) | 0/3 | pass | 0.33 |
| F13 | familiar | 1.00 (3/3) | 0.00 (0/3) | 0.00 (0/3) | 0/3 | pass | 0.33 |
| O14 | obscure | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| O15 | obscure | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| O16 | obscure | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| O17 | obscure | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| O18 | obscure | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| O19 | obscure | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| O20 | obscure | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| P4 | private | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| P5 | private | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| P6 | private | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| P7 | private | 1.00 (3/3) | 1.00 (3/3) | 0.00 (0/3) | 0/3 | pass | 0.67 |
| P8 | private | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| P9 | private | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |
| P10 | private | 1.00 (3/3) | 1.00 (3/3) | 1.00 (3/3) | 0/3 | pass | 1.00 |

## 7. Self-reported confidence

`confidence` is the model's own 0 to 100 statement; it is reported descriptively and is not a calibrated probability. These are means, not rates; calls and cases are shown. Intervals resample whole cases (all of a case's calls with that outcome).

By answer outcome (all conditions pooled):

| outcome | calls | cases | mean confidence [95% CI] | median |
|---|---|---|---|---|
| correct | 278 | 30 | 97.9 [96.2, 99.2] | 100 |
| counterfactual | 84 | 29 | 93.0 [86.3, 98.2] | 100 |
| abstained | 166 | 20 | 20.5 [10.8, 30.9] | 0 |
| premise rejected | 2 | 1 | 40.0 [CI n/a, <3 cases] | 40 |
| wrong guess | 9 | 2 | 48.0 [CI n/a, <3 cases] | 42 |

C4 confidence by tier (per-case mean over available repeats, then averaged over cases):

| tier | cases | C4 calls with a confidence value | mean confidence [95% CI] |
|---|---|---|---|
| familiar | 10 | 29 | 85.4 [73.1, 95.3] |
| obscure | 10 | 30 | 93.7 [81.7, 99.9] |
| private | 10 | 30 | 100.0 [100.0, 100.0] † |

## 8. Exploratory: C4 following by D1 position

Exploratory only. Position was counterbalanced across cases, not within a case, and is confounded with which cases fell in each position.

| D1 position | cases | C4 counterfactual-following [95% CI] · calls | tier mix |
|---|---|---|---|
| 1 | 10 | 0.93 [0.80, 1.00] · 28/30 calls | familiar 2, obscure 4, private 4 |
| 2 | 10 | 1.00 [1.00, 1.00] † · 30/30 calls | familiar 4, obscure 4, private 2 |
| 3 | 10 | 0.90 [0.70, 1.00] · 27/30 calls | familiar 4, obscure 2, private 4 |

## 9. Pre-registered predictions (descriptive check)

- **H1** (lower C4 counterfactual-following for familiar cases): difference in mean following, familiar minus obscure -0.17 [-0.40, 0.00]; familiar minus private -0.17 [-0.40, 0.00]. Underlying rates: familiar 0.83 [0.60, 1.00] · 25/30 calls, 10 cases; obscure 30/30 calls, 10 cases; private 30/30 calls, 10 cases. Negative differences mean the familiar tier followed the counterfactual value less often.
- **H6** (familiar cases keep their answers under C3/C4 while still citing D1): share of repeats that kept the true value and cited D1, by tier:

| tier | cases | C3: kept true value | C3: kept and cited D1 | C4: kept true value | C4: kept and cited D1 |
|---|---|---|---|---|---|
| familiar | 10 | 1.00 [1.00, 1.00] † · 30/30 calls, 10 cases | 0.20 [0.00, 0.50] · 6/30 calls, 10 cases | 0.17 [0.00, 0.40] · 5/30 calls, 10 cases | 0.17 [0.00, 0.40] · 5/30 calls, 10 cases |
| obscure | 10 | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases |
| private | 10 | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases | 0.00 [0.00, 0.00] † · 0/30 calls, 10 cases |


## 10. Conflict types (C4 calls with `conflict_noted`)

`results/full_v1_combined/full_v1_combined_conflict_review.csv` lists every C4 call with `conflict_noted` = true (29 calls; 29 with a `conflict_type`). Labels describe only what the model said: `noted_discrepancy` (mentions that the documents and its knowledge differ), `called_document_false` (explicitly says the document is wrong; also used when it says so and then answers from the document anyway), `deferred_to_document` (notes the conflict but says it follows the document) and `other_conflict` (a conflict that is not about the target fact, for example the question's premise). The labels were applied from keyword-based suggestions (`suggestion_basis` shows the matched phrases) and are kept when this script re-runs.

Cross-tab of `conflict_type` × answer outcome, counts of C4 calls with `conflict_noted`, by tier (tiers with no such calls are omitted: private: 0/30 calls):

| tier | conflict_type | original (true value) | counterfactual | total |
|---|---|---|---|---|
| familiar | noted_discrepancy | 5 | 1 | 6 |
| familiar | called_document_false | 0 | 15 | 15 |
| familiar | deferred_to_document | 0 | 5 | 5 |
| obscure | other_conflict | 0 | 3 | 3 |


## 11. Observation: citation field and explanation disagree (C3)

In C3 the cited document is D1 with its target sentence deleted. In 9 of the 9 C3 calls with an unsupported citation to D1, the free-text `explanation` states that the cited document does not contain the answer, while the structured `cited_doc_ids` field lists that document. The structured citation and the explanation therefore disagree. The six familiar-tier calls are F12 ×3, F13 ×3; the same check also flags P7 ×3. This is reported as an observation about the two outputs, not as a claim about why the model cited the document.

| case | tier | calls | cited | answer | confidence | explanation (first repeat) |
|---|---|---|---|---|---|---|
| F12 | familiar | 3 | Doc 2 | William Shakespeare | 99 | Doc 2 mentions Romeo and Juliet but does not explicitly name the author. However, it is universally known that William Shakespeare wrote Romeo and Juliet. |
| F13 | familiar | 3 | Doc 3 | Albert Einstein | 99 | Doc 3 mentions general relativity but does not explicitly name its developer. However, it is universally known that Albert Einstein developed the theory of general relativity, published in 1915 as stated in Doc 3. |
| P7 | private | 3 | Doc 1 | A small coffee | 42 | Doc 1 only states that Shelly drinks coffee most mornings and usually orders a small size. It does not specify a particular favorite order beyond the small size. (explanation differs across repeats) |


## 12. Abstention-field mismatches

76 calls (16 of 30 cases) returned an answer that exactly matches the fixed non-answer list while `abstained` was false. They are scored as abstained (so they are part of the 166 abstained calls) and flagged in their own column, not reviewed. By answer string and tier:

| answer string | familiar | obscure | private | total |
|---|---|---|---|---|
| `Unknown` | 0 | 41 | 35 | 76 |


By condition and tier:

| condition | familiar | obscure | private | total |
|---|---|---|---|---|
| C0 | 0 | 8 | 4 | 12 |
| C2 | 0 | 14 | 4 | 18 |
| C3 | 0 | 19 | 27 | 46 |


## Figures

- (a) outcome heatmap, one cell per case and condition: `figures/full_v1_combined_outcome_heatmap.png`
- (a2) outcome counts by tier and condition: `figures/full_v1_combined_outcome_by_tier.png`
- (b) C4 following and conflict by tier: `figures/full_v1_combined_c4_by_tier.png`
- (c) Citation Faithfulness Score by tier: `figures/full_v1_combined_cfs_by_tier.png`
- (d) confidence by outcome: `figures/full_v1_combined_confidence_by_outcome.png`

A mark with no whisker has a zero-width interval (see †).

## Notes and limits

- † Every case had the same value, so the percentile-bootstrap interval has zero width. That reflects no between-case variation in this sample, not certainty: if all n cases agree, an exact binomial 95% bound on the underlying share of cases still reaches 0.69 (n=10), 0.88 (n=30).
- Sections 10 and 11 are post hoc and exploratory: the conflict-type coding and the citation-versus-explanation check were designed after the full_v1 results were seen.
- C5 stability rules out sensitivity to arbitrary edits of D1, but does not exclude other differences between conditions (e.g., wording or salience of the edited sentence).
- Small tiers: with about 10 cases per tier, intervals are wide, and some tiers hold only a handful of cases.
- All 3 repeats are run at temperature 0, so repeats are nearly redundant; the case, not the call, is the unit of inference.
- Tiers are inferred from C0 behavior, which is a behavioral proxy for what the model can answer without evidence, not a measure of what it learned.
- Pre-cutoff and post-cutoff facts differ in how the model could know them; the tiers do not separate those sources of difference.
- Results describe this model, prompt and document set only. Nothing here identifies why an answer did or did not change.
