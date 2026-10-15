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
| Max output tokens | 300 |
| Output format | Forced tool use (see below) |

The plain ID `anthropic.claude-sonnet-4-6` fails with "on-demand throughput isn't supported". Access verified October 15, 2026. No fine-tuning is used. All settings are fixed across conditions.

### Structured Output

The model is required, via Converse tool use with a forced tool choice, to return:

| Field | Type | Meaning |
|---|---|---|
| `answer` | string | Concise answer: just the value (for example, a year or a name) |
| `cited_doc_ids` | list of strings | IDs of cited documents; empty if none |
| `abstained` | boolean | The model declines to answer |
| `conflict_noted` | boolean | The model notes a conflict between sources, or with what it knows |

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

### Citation Faithfulness Assessment

We compare responses across original and modified evidence conditions, giving particular attention to cases where:

1. The model produces a correct answer and a supporting citation.
2. The model gives the same answer when the cited evidence is removed or masked.
3. The model follows a deliberately changed fact in the cited document.
4. The model changes citations without changing its answer.
5. The model cites evidence even when experiments indicate limited sensitivity to it.

No single intervention outcome is definitive proof of a model's internal information source. Observed behavioral evidence of reliance is reported separately from stronger causal claims, using the terms in Section 3.5.

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
2. **Answer matching.** Normalize the answer and the reference values (lowercase, strip punctuation). After normalization, an answer is **correct** if it contains an accepted form of the true value; in C4 it is **counterfactual-following** if it contains the counterfactual value. Answers containing both values, or longer than 10 words, are flagged for manual review. An answer matching neither value is outcome "other" and is also reviewed.
3. **Masking method.** Default: delete the target sentence from D1. Use a paraphrase (for example, "in the early 1900s") only where deletion leaves the document incoherent. The method used is recorded per case.
4. **`answer_source` judgment.** A self-report of `answer_source = documents` is marked **inconsistent** only if the answer is unchanged in both C3 and C4 in at least 2 of 3 repeats **and** C5 stays at the noise-floor level for that case (C5's answer-change rate for that case is no higher than C1's self-disagreement rate for that case). "2 of 3 repeats" refers to the 3 runs of C3 and of C4. This applies only after the pilot check that requesting the field does not change answers.

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

## Reference

Wallat, J., Heuss, M., de Rijke, M., & Anand, A. (2025). *Correctness is not Faithfulness in Retrieval Augmented Generation Attributions*. Proceedings of ICTIR 2025, 22–32. https://doi.org/10.1145/3731120.3744592
