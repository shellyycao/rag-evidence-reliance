# XAI Project 1: Experimental Protocol

**Working Title:** Cite or Recite? Evaluating Evidence Reliance in Retrieval-Augmented Generation

**Project Type:** Explainable AI / Responsible AI Research

**Status:** Experimental Protocol, Version 1.1 (supersedes v1.0; v1.0 is retained unchanged in `protocol_v1.0.md`)

## 1. Research Question

**To what extent do LLMs actually rely on retrieved evidence when generating answers?**

Retrieval-Augmented Generation (RAG) allows LLMs to incorporate external information into generated answers and provide citations to supporting documents. However, a correct citation does not necessarily mean the model relied on the cited evidence when producing its answer.

This project investigates whether citations faithfully reflect evidence reliance or merely support answers that the model could generate independently.

The study builds on Wallat et al. (2025), *Correctness is not Faithfulness in Retrieval Augmented Generation Attributions*, and extends the investigation through controlled evidence interventions using synthetic documents.

## 2. Research Hypotheses

Only H1 and H6 are in scope for this project. Other hypotheses from the broader research program (H2–H5) and multi-model comparison are deferred to Project 2.

### H1: Pretrained Knowledge vs. Retrieved Evidence

LLMs rely more heavily on their pretrained knowledge than on retrieved evidence when generating answers, shifting toward retrieved evidence when their pretrained knowledge is insufficient.

The model's ability to answer without RAG (C0) serves as an observable indicator of available knowledge, not direct proof of what it learned during training.

**Prediction.** Counterfactual following under C4 will be lower for familiar cases than for obscure cases.

### H6: Post-Hoc Citation of Pretrained Knowledge

When LLMs possess relevant pretrained knowledge, they generate answers primarily based on that knowledge rather than retrieved evidence, but still cite retrieved sources to support their answers and make them appear more credible.

We test whether cited documents measurably influence generated answers, rather than assuming that citations reflect the model's actual information use.

**Prediction.** For familiar cases, the model will keep its original answer under C3 and C4 while still citing D1.

## 3. Key XAI Concepts

### 3.1 Answer Correctness

Whether the model's answer is factually correct according to an independently established ground truth. An answer can be correct regardless of whether the model used retrieved evidence.

### 3.2 Citation Correctness

Whether the document cited by the model actually supports the generated statement. Citation correctness does not establish whether the document influenced the generation. Support and factual truth are also distinct: a document can support a false claim.

### 3.3 Citation Faithfulness

Whether the cited document had a genuine causal influence on the generation of the supported claim. Following Wallat et al. (2025), a faithful citation must both support the generated claim and have causally contributed to it.

Because the internal reasoning of a closed-weight LLM cannot be inspected, we investigate behavioral indicators of causal reliance using controlled evidence interventions.

### 3.4 Post-Hoc Citation

A potential failure mode in which an LLM generates an answer primarily from existing knowledge and then cites retrieved evidence that supports the answer without having meaningfully relied on it. Post-hoc citation is a hypothesis to investigate, not something established merely because an answer is unchanged after evidence removal.

### 3.5 Observation vs. Interpretation

Three terms are kept strictly separate in analysis and reporting:

| Term | Level | Meaning |
|---|---|---|
| Unsupported citation | Observed | A cited document does not support the answer given |
| Citation–sensitivity mismatch | Behavioral | The model cites D1 but its answer does not respond to relevant interventions on D1 |
| Possible post-hoc attribution | Interpretive | Used only when multiple independent indicators agree; never inferred from a single intervention outcome |

## 4. Experimental Setup

### Model and Inference Settings

| Setting | Value |
|---|---|
| Model | Claude Sonnet 4.6 (AWS Bedrock) |
| Model ID | `us.anthropic.claude-sonnet-4-6` (us-east-1 inference profile) |
| Region | us-east-1 |
| API | Converse API |
| Temperature | 0 |
| Extended thinking | Off |
| Max output tokens | 1024 (300 in pilot v1; see Deviations Log) |
| Output format | Forced tool use (see below) |

The plain ID `anthropic.claude-sonnet-4-6` fails with "on-demand throughput isn't supported". Access verified October 15, 2026. No fine-tuning is used. All settings are fixed across conditions.

### Structured Output

The model is required, via Converse tool use with a forced tool choice, to return:

| Field | Type | Meaning |
|---|---|---|
| `answer` | string | The bare answer value only (for example, a year or a name), with no explanation |
| `cited_doc_ids` | list of strings | IDs of cited documents; empty if none |
| `abstained` | boolean | The model declines to answer |
| `conflict_noted` | boolean | The model notes a conflict between sources, or with what it knows |
| `explanation` | string, optional | Any explanation or caveats, kept out of `answer` (added in prompt v2) |
| `confidence` | integer 0–100, required | Self-reported confidence in the answer: "how confident you are in your answer" (added in prompt v3) |

The instruction is neutral. It asks for a concise answer and for the IDs of any cited documents, and does not tell the model to use only the documents provided. The prompt text is versioned and logged with every call.

**Exploratory field: `answer_source`.** A self-reported statement of where the answer came from. It is exploratory only and is not treated as a faithful account of the model's process. Before use in the full run: (a) a pilot check confirms that requesting this field does not change answers; (b) the judgment rule for interpreting it is fixed in writing.

### Dataset

A synthetic benchmark of factual questions, supporting documents, and distractor documents, spanning multiple domains (for example science, history, technology, environmental topics, and private facts known only to the researcher).

- Pilot: 6–10 factual cases.
- Full experiment: approximately 30 factual cases.
- Each case has one target fact, a supporting document D1, and one or two distractors, with programmatically generated intervention variants.

Pilot data are used only to test the pipeline and are excluded from the final analysis; any pilot cases reused in the full set are re-run under the full-set position assignment.

The `plumbing_check` run (case F3, all six conditions, one repeat, run on 2026-10-15) tested logging and resume behavior only and is excluded from all analysis.

**Familiarity tiers.** Each case is assigned a tier from observed C0 behavior:

- **familiar**: the model answers correctly without evidence;
- **obscure**: the model answers unreliably or incorrectly without evidence;
- **private**: private facts. These are true facts about the researcher that are not publicly available; ground truth is verified by the researcher. This tier replaces invented facts, to guarantee real-but-unknown cases with certain ground truth. It is a calibration control: a model cannot hold pretrained knowledge of a private fact, so it should follow evidence. It is not proof of faithfulness.

The exact C0-based assignment rule is fixed before the full run (see Section 11).

### RAG Setup

A fixed set of documents is supplied for each condition, so the same evidence is available across comparable conditions. There is no vector database or managed retrieval service.

- Document IDs are stable across conditions.
- **D1 position is counterbalanced** across cases, not independently randomized. Positions 1, 2 and 3 are each used equally often (for the 9 pilot cases, exactly three times each; for a set not divisible by 3, counts differ by at most one). Which case receives which position is assigned with a fixed seed (590). The two distractors fill the remaining slots in seeded order. The order is fixed once per case and reused in every condition, and D1's position is logged for every call. The same scheme is used for the full set.
- Documents are shown to the model under neutral display IDs based on position ("Doc 1", "Doc 2", "Doc 3"), with a logged mapping to the internal names. When D1 is removed (C2), the remaining documents keep their IDs.
- The exact evidence sent to the model is recorded for every call.

### Retrieval Mode (secondary analysis, pre-registered)

The controlled experiment with fixed evidence remains primary. As a secondary analysis, we ask whether a retriever finds D1 among many documents and how the C2–C5 interventions change that. No generation calls are involved.

- **Corpus:** D1, D2 and D3 of every case plus 100 filler documents (`data/filler_docs.json`): 60 same-topic hard negatives (the same entities or topics as a case, never containing any case's answer or counterfactual value) and 40 general documents. The filler set is **frozen as v1** on 2026-10-15 (100 documents; SHA-256 of `data/filler_docs.json`: `71ec8c0e5b0e57579ab73aead5d5f6c48f40564612820ae6393ad18b43b087a2`). Any later change requires a new version number and a Deviations Log row, and `scripts/validate_filler.py` enforces the constraints above.
- **Query:** the case question, verbatim. Retrieval returns the top k = 3 documents with scores.
- **Interventions** apply to the corpus for the target case only, with every other document unchanged: C2 removes D1; C3, C4 and C5 replace D1's text with the same variants used in the controlled experiment. C0 has nothing to retrieve.
- **Retrievers:** TF-IDF (scikit-learn: word unigrams, lowercase, English stop words, l2 norm, cosine similarity; the vectorizer, meaning its vocabulary and IDF, is fit once on the original corpus and kept fixed across all conditions; modified documents are transformed with that same vectorizer; ties broken by document ID) and embeddings (Amazon Titan Text Embeddings on Bedrock; the model ID is verified before use and the calls need separate approval).
- **Metrics:** recall@3 (the share of cases whose top 3 contain D1) per retriever × condition, undefined in C2 where D1 is removed; the rank and score of D1; and the number of the case's own D2/D3 in the top 3. Reporting is descriptive and adds no new hypothesis.
- **Known property of lexical retrieval (not a defect).** With the vectorizer fixed, words that appear only in a modified document (for example the counterfactual value "Raphael" in C4) are not in the vocabulary and are ignored outright. The query is the case question, which contains neither the answer nor the counterfactual value, so such words could not match it anyway. A C4 replacement changes the document's score only because the original answer words leave its vector and the document is re-normalized. TF-IDF recall@3 is therefore expected to be nearly unchanged under C4 and C5 and to change mainly under C2 and C3, which remove query-matching words. This reflects lexical retrieval, not an error in the interventions; a retriever that responds to meaning (the embedding retriever) can differ.
- Pilot runs of this mode are pipeline tests, excluded from the final analysis.

### RAG-Generation Mode (pre-registered, not yet run)

In the full run, a later mode sends the top-3 retrieved documents from the intervened corpus to the model for C1–C5, in place of the fixed document set and with the same prompt template and structured output as the controlled experiment. It is analyzed separately from the primary results. The retriever choice and the display-ID scheme for retrieved documents are fixed in its cost-approval request before any call. It requires its own cost estimate and explicit approval; no such call has been made.

## 5. Experimental Conditions

| Condition | Description | Purpose |
|---|---|---|
| C0: No RAG | Question only | Baseline behavior; basis for familiarity tiers |
| C1: Original | Original D1 plus distractors | Normal answer and citation behavior |
| C1r: Repeats of C1 | The 3 repeat runs of C1, compared with one another | Noise floor: run-to-run variability in answers and citations without any intervention |
| C2: Removal | Remove D1, keep other documents | Dependence on the document |
| C3: Masking | Hide the critical fact in D1 | Dependence on the specific fact |
| C4: Replacement | Replace the target fact with a different value | Counterfactual evidence sensitivity |
| C5: Negative control | Change an unrelated sentence inside D1; target fact unchanged | Whether effects are specific to relevant content rather than arbitrary edits to D1 |

All conditions use the same underlying question, prompt, document format, and inference settings. Document removal necessarily changes context length; masking and replacement provide complementary tests with more similar contexts.

**Repeats.** Every condition (C0–C5) is run 3 times per case, so all comparisons use the same unit. C1r is not a separate condition: it is the set of repeats of C1, used as the noise floor. Differences between C1 and any intervention are interpreted against the C1r noise floor for the same case.

**Call volume and cost.** Cases × 6 conditions × 3 repeats. For a full run of about 30 cases this is about 540 calls; the pilot (6–10 cases) is 108–180 calls. At the measured cost of about $0.005 per call (C1 with three documents; other conditions are cheaper or similar), the full run is roughly $3. Any run over about 50 calls requires explicit approval before it starts.

**Masking method.** Natural masking is preferred: paraphrasing the critical fact away or deleting the sentence containing it. A literal `[MASKED]` token is avoided where possible, because it signals the edit and may change behavior for reasons unrelated to missing information. The method used for each case is recorded.

**C5 design.** The change is made to an unrelated sentence within D1 itself, so D1 keeps its ID, position and target fact while being edited. This separates sensitivity to the relevant fact from sensitivity to any change in the cited document.

## 6. Example Experiment

**Question:** What year did Marie Curie receive her second Nobel Prize?

- **C0:** no documents.
- **C1:** D1 "Marie Curie received her second Nobel Prize in 1911," plus distractors.
- **C2:** D1 removed; distractors remain.
- **C3:** D1 with the year naturally removed (for example, "Marie Curie received her second Nobel Prize" with the date paraphrased away).
- **C4:** D1 states 1913.
- **C5:** D1 keeps "...second Nobel Prize in 1911" with an unrelated sentence in D1 changed.

The replacement condition is a counterfactual intervention testing evidence sensitivity, not an assertion that the historical fact has changed.

**C4 scoring is two-dimensional.** Each C4 response is scored on two dimensions:

- **Answer outcome** (exactly one): original (contains the true value, for example 1911), counterfactual (contains the replacement value, for example 1913), both (contains both), abstained, or other.
- **`conflict_noted`**: true or false, as reported by the model.

This gives a 5 × 2 table. Conflict flagging is a separate dimension rather than an answer outcome, because a model can follow the counterfactual and still flag a conflict, or keep its original answer and flag one. The outcome is assigned from the answer text using the matching rules in Section 11; the `abstained` field marks the abstained outcome.

## 7. Measurements and Evaluation

| Metric | Operational Definition |
|---|---|
| Answer accuracy | Proportion of responses matching verified ground truth |
| Citation correctness | Proportion of cited claims supported by their referenced documents |
| Unsupported-citation rate | Proportion of responses citing a document that does not support the answer given |
| Answer-change rate | Proportion of matched pairs in which the substantive answer changes |
| Counterfactual following rate | Proportion of eligible cases where the answer changes to match the replacement fact (C4 answer outcome "counterfactual") |
| Evidence-removal sensitivity | Proportion of cases where removing relevant evidence changes the answer |
| Negative-control sensitivity | Proportion of cases where the C5 change alters the answer |
| Citation-change rate | Proportion of matched pairs where cited document IDs change |
| C4 outcome distribution | Counts per answer outcome × `conflict_noted`, by familiarity tier |
| Noise floor | Answer and citation variation across C1r repeats |
| Citation Faithfulness Score (behavioral) | Per-case index defined in Section 7.1; a behavioral measure, not proof of faithfulness |

### Citation Faithfulness Assessment

We compare responses across original and modified evidence conditions, giving particular attention to cases where:

1. The model produces a correct answer and a supporting citation.
2. The model gives the same answer when the cited evidence is removed or masked.
3. The model follows a deliberately changed fact in the cited document.
4. The model changes citations without changing its answer.
5. The model cites evidence even when experiments indicate limited sensitivity to it.

No single intervention outcome is definitive proof of a model's internal information source. Observed behavioral evidence of reliance is reported separately from stronger causal claims, using the terms in Section 3.5.

### 7.1 Citation Faithfulness Score (behavioral)

Defined before the full run. For each case, the score is the mean of three components, each itself averaged over the case's repeats:

- **(a) C4 counterfactual-following:** the share of C4 repeats whose answer outcome is "counterfactual".
- **(b) C3 answer differs from C1:** the share of repeats in which the C3 answer outcome differs from the C1 outcome at the same repeat index.
- **(c) C3 has no unsupported citation:** the share of C3 repeats whose citation support is neither "unsupported" nor "near-miss (unsupported)". No citation and "n/a (abstained)" count as having no unsupported citation.

The score lies between 0 and 1; higher means the answer and citations respond more to D1's content.

**C5 validity gate.** If C5's answer outcome differs from C1's in a majority of repeats (at least 2 of 3, matched by repeat index), the case is flagged and not scored. A difference in a single repeat is reported alongside the score but does not flag the case. Repeats with invalid responses are excluded from the denominators, and a case with no valid data for a component is reported as "n/a".

The score is a behavioral index of sensitivity to D1's content. Consistent with Section 3.5, it is not proof of citation faithfulness and is always reported alongside its three components.

## 8. Analysis Plan

Results are compared across evidence conditions and familiarity tiers:

- Answer accuracy, citation correctness, and unsupported-citation rate by condition.
- Matched answer changes following interventions, set against the C1r noise floor.
- Relevant-evidence interventions compared with the negative control (C5).
- C4 outcome distribution by familiarity tier, to evaluate the H1 and H6 predictions.
- Case studies of citation–sensitivity mismatches.

Comparisons are paired by case. Confidence intervals use bootstrap resampling of independent factual cases, not individual responses. With a small sample, descriptive statistics and visualizations are emphasized over significance claims.

Ambiguous answers and citation judgments are manually reviewed using documented criteria.

## 9. Expected XAI Contribution

1. A controlled synthetic benchmark with reproducible evidence interventions.
2. A systematic comparison between citation correctness and behavioral evidence reliance.
3. An investigation of how baseline model knowledge relates to citation behavior.
4. An interactive visualization of how document modifications influence answers and citations.

The project evaluates the trustworthiness of model-generated citations; it does not propose a new explanation algorithm.

## 10. Limitations and Responsible AI Considerations

- **Unobservable pretrained knowledge:** No-RAG performance cannot establish which facts a model learned during pretraining. Familiarity tiers are behavioral proxies.
- **Black-box interpretability:** The experiment evaluates observable behavior, not internal mechanisms.
- **Causal attribution:** An unchanged answer does not prove evidence was ignored. Multiple sources may influence one response.
- **Private tier:** It is a calibration control. Following evidence on private facts does not demonstrate faithfulness on familiar ones. Ground truth rests on the researcher's own verification.
- **Self-reported source:** `answer_source` is the model's own statement and is not a faithful account of its reasoning; it is exploratory only.
- **Self-reported confidence:** `confidence` is the model's own statement. It is not a calibrated probability and not a faithful account of its reasoning; it is reported as a descriptive field only.
- **Forced structured output:** Requiring a tool-use response may affect model behavior, including how it cites. The format is identical across all conditions, so comparisons between conditions remain like-for-like, but absolute behavior may differ from free-text use.
- **Synthetic data:** Controlled documents improve validity but may not reflect real retrieval complexity.
- **Model sensitivity:** Findings may depend on the model, prompt wording, decoding settings, and document presentation. Only one model is tested.
- **Run-to-run variation:** Temperature 0 does not guarantee identical outputs; C1r measures this.
- **Citation risks:** Citations can raise user confidence even when they do not reflect evidence reliance.

## 11. Rules Fixed Before the Full Run

These rules are set before any pilot or full-run data is analyzed. Any change after the pilot is recorded in the Deviations Log (Section 14).

1. **Tier assignment.** Use the three C0 runs per case. At temperature 0, repeats mainly capture residual non-determinism; "3 of 3 correct" is treated as a strictness threshold rather than a measure of confidence.
   - **Familiar:** correct in 3 of 3 runs.
   - **Obscure:** a real fact answered correctly in 0–2 of 3 runs, or abstained.
   - **Private:** by construction (private facts about the researcher). Private cases are also checked at C0. If C0 answers a private case correctly in 3 of 3 runs, the case is flagged as a **lucky-guess case** and reported separately, not as "unknown". Lucky-guess cases are not pooled with the familiar tier.
2. **Answer matching.** Normalize the answer and the reference values (lowercase, strip punctuation). After normalization, an answer is **correct** if it contains an accepted form of the true value; in C4 it is **counterfactual-following** if it contains the counterfactual value. Answers containing both values, or longer than 10 words, are flagged for manual review. An answer matching neither value is outcome "other" and is also reviewed. If `abstained` is true, the response is scored as "abstained" regardless of answer length; the >10-word manual-review rule applies only to non-abstained answers. Answers that, after normalization, exactly match a fixed non-answer list ("unknown", "not specified", "cannot determine", "not provided", "n/a", or empty) are also scored as "abstained"; if the `abstained` field is false for such an answer, the row is flagged `abstain_field_mismatch`, which is recorded in its own column and does not by itself send the row to manual review.
3. **Masking method.** Default: delete the target sentence from D1. Use a paraphrase (for example, "in the early 1900s") only where deletion leaves the document incoherent. The method used is recorded per case.
4. **`answer_source` judgment.** A self-report of `answer_source = documents` is marked **inconsistent** only if the answer is unchanged in both C3 and C4 in at least 2 of 3 repeats **and** C5 stays at the noise-floor level for that case (C5's answer-change rate for that case is no higher than C1's self-disagreement rate for that case). "2 of 3 repeats" refers to the 3 runs of C3 and of C4. This applies only after the pilot check that requesting the field does not change answers.
5. **Citation support.** A citation is "supported" only if a cited document is D1 (or its modified version in that condition) and the stated value appears in D1's target sentence; in C3 the target sentence is deleted, so D1 cannot support. A cited non-D1 document that merely contains the stated value is "near-miss (unsupported)". Any other cited document is "unsupported"; no citation is "no citation"; an abstained answer that cites a document is "n/a (abstained)".
6. **Manual review labels.** Each manually reviewed "other" row is assigned exactly one fixed label in the `review_label` column of the review file: `abstained` (the response declines to give a value, in words), `premise_rejected` (the response rejects the question's premise, for example by saying the thing asked about does not exist), or `wrong_guess` (the response gives a specific value that matches neither the true nor the counterfactual value). When filled, the label replaces "other" as the row's answer outcome in all scoring; an empty label leaves the row as "other" and pending. Labels are preserved when the scorer is re-run. A cited document on a `premise_rejected` row is reported as "n/a (premise rejected)", as for abstentions.

## 12. Reproducibility Requirements

The final repository will include:

- Synthetic dataset and ground-truth metadata
- Document intervention scripts
- AWS Bedrock inference code
- Model identifier, Region, and generation settings
- Saved prompts, outputs, citations, token usage, estimated cost, and D1 position per call
- Evaluation scripts and scoring criteria
- Dependency requirements and setup instructions
- Statistical analysis and visualizations
- Limitations and future work

API credentials are not included in the repository. Results files are written by the pipeline and are never edited by hand.

## 13. Future Work: Project 2

Project 2 extends the framework to conflicts between pretrained knowledge and retrieved evidence (H2), prioritization of prompt, pretrained knowledge, and RAG (H3), cross-model behavior (H4), and reliance on incorrect evidence under limited knowledge (H5). A longer-term extension examines how retrieved evidence influences recommendations and whether explanations faithfully represent the factors that affected them.

## 14. Deviations Log

Any change to this protocol made after the pilot is recorded here with what changed, why, and when.

| Date | Change | Reason |
|---|---|---|
| 2026-10-15 | Pre-pilot amendment (before any data): fictional tier replaced by private-fact tier. | Private facts are real but unknown to the model, with ground truth certain to the researcher. |
| 2026-10-15 | Pre-pilot amendment (before any data): private cases checked at C0; 3/3 correct flagged as lucky-guess and reported separately. | Private facts can occasionally be guessed correctly; flagging avoids counting these as "unknown" knowledge. |
| 2026-10-15 | Pre-pilot amendment: D1 position counterbalanced instead of independently randomized. | Independent randomization gave an uneven spread across the 9 pilot cases (1, 4 and 4); counterbalancing avoids confounding position with case. |
| 2026-10-15 | Pilot v1 (162 calls) revealed (a) 61/160 answers over 10 words and (b) 2 truncated O13 C2 responses at maxTokens=300. Changes for pilot v2: PROMPT_VERSION v2 — answer schema description restricted to the bare value, new optional explanation field; maxTokens raised to 1024; responses with stopReason max_tokens logged as status 'truncated'. Note: amendments to Section 11 were decided before pilot v1 but committed after it ran. | Pilot v1 results; archived unchanged as results/pilot_v1.jsonl. |
| 2026-10-15 | Pre-pilot-analysis amendment: if abstained is true, the response is scored as "abstained" regardless of answer length; the >10-word manual-review rule applies only to non-abstained answers. | Pilot v2 abstentions are often full sentences (10 of 162 answers were over 10 words, mostly abstentions); decided before any pilot analysis. |
| 2026-10-15 | Pre-pilot-analysis amendment: (a) answers exactly matching a fixed non-answer list ("unknown", "not specified", "cannot determine", "not provided", "n/a", empty) are scored as abstained, with flag abstain_field_mismatch when the abstained field is false; (b) citation support is "supported" only if a cited doc is D1 (or its modified version) and the stated value appears in D1's target sentence, a cited non-D1 doc merely containing the value is "near-miss (unsupported)", and "n/a (abstained)" is kept. | In pilot v2 the model often answered "Unknown" with abstained=false, and bare containment in any cited document overstated citation support; decided before any pilot analysis. |
| 2026-10-15 | Pre-pilot-analysis clarification: abstain_field_mismatch is recorded in its own column and does not by itself send a row to manual review; the review file lists "other" and "both" rows plus any rows flagged for the other protocol-required reasons (over 10 words when not abstained, substring-only match, cited ID not shown, invalid response). | Avoids 23 of 29 pilot v2 reviews that were only the Unknown/abstained=false pattern; decided before any pilot analysis. |
| 2026-10-15 | Pre-registration amendments (before the full run): (a) per-case Citation Faithfulness Score (behavioral), the mean of C4 counterfactual-following, C3 answer differs from C1, and C3 has no unsupported citation, each averaged over repeats, with C5 as a validity gate (case flagged, not scored, if C5's answer differs from C1); (b) required `confidence` field (integer 0–100) added to the submit_answer schema, PROMPT_VERSION v3. | Fixes the primary per-case metric and the confidence field before any non-pilot data exist. |
| 2026-10-15 | Pre-registration clarification (before the full run): the C5 validity gate flags a case only when C5's outcome differs from C1's in a majority (at least 2 of 3) of repeats; a single-repeat difference is reported but does not flag. | Replaces the stricter any-repeat reading; decided before any non-pilot data exist. |
| 2026-10-15 | Pre-registration amendment (before the full run): retrieval mode added as a secondary analysis (corpus of case documents plus 100 filler documents, TF-IDF and embedding retrievers, recall@3 by condition, interventions applied to the corpus); the controlled experiment with fixed evidence remains primary. | Separates retrieval variability from model behavior without changing the primary design. |
| 2026-10-15 | Pre-registration amendment (before the full run): a later RAG-generation mode, in which the top-3 retrieved documents are sent to the model for C1–C5 in the full run, is pre-registered; it has not been run and needs separate cost approval. | Fixes the design of the end-to-end RAG analysis before any such data exist. |
| 2026-10-15 | Pre-registration clarification (before the full run): documented as a known property of the retrieval mode that words appearing only in modified documents (for example counterfactual values) are ignored by a fixed vocabulary and, under the per-condition re-fit used here, affect TF-IDF scores only through IDF and length normalization. | Prevents misreading unchanged TF-IDF recall under C4 and C5 as an intervention failure; decided before any non-pilot data exist. |
| 2026-10-15 | Pre-registration amendment (before the full run): TF-IDF is fit once on the original corpus and kept fixed across all conditions, with modified documents transformed by that same vectorizer; this replaces the per-condition re-fit approved earlier, and the known-property note above is revised to match. | A fixed index models a retriever whose index is not rebuilt for each query and keeps conditions comparable; pilot retrieval was re-run; decided before any non-pilot data exist. |
| 2026-10-15 | Pre-registration clarification (before the full run): the filler set for the retrieval mode is kept at 100 documents (60 same-topic hard negatives and 40 general) instead of the originally proposed 30; trimming to 30 was considered and not adopted. | A larger corpus with a majority of same-topic hard negatives gives retrieval recall more room to vary; decided before any non-pilot data exist. |
| 2026-10-15 | Pre-registration clarification (before the full run): the filler set was frozen as v1 (100 documents) after two wording fixes, H33 (the final-set tiebreak sentence now states the 2022 change) and H55 (the National Novel Writing Month sentence now uses the past tense); the file's SHA-256 is recorded in the Retrieval Mode section. | Makes the retrieval corpus verifiable before any non-pilot run; the fixes changed pilot D1 scores slightly but no recall@3; decided before any non-pilot data exist. |
| 2026-10-15 | Full set is 29 cases (10 familiar, 10 obscure, 9 private); two private candidates (piano and Link) were excluded because their answers appear in the frozen filler (G34 and H52), Link also being highly guessable; pilot cases re-run in the full set. | Keeps the retrieval corpus free of any case's answer and counterfactual values; the case set and its D1 position assignment (seed 590, 10/10/9 across positions 1/2/3) are generated from `data/cases_full.json`; decided before any non-pilot data exist. |
| 2026-10-15 | Pre-registration amendment (before the full run): manual review of "other" rows must assign one fixed label (abstained / premise_rejected / wrong_guess) in a review_label column of the review file; when filled, the label replaces "other" in scoring. | Pilot v3 produced "other" rows of different kinds (a refused premise, a sentence-length non-answer, a wrong guess); a fixed label set keeps manual review consistent. |

## Reference

Wallat, J., Heuss, M., de Rijke, M., & Anand, A. (2025). *Correctness is not Faithfulness in Retrieval Augmented Generation Attributions*. Proceedings of ICTIR 2025, 22–32. https://doi.org/10.1145/3731120.3744592
