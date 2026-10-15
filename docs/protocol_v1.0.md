# XAI Project 1: Experimental Protocol

**Working Title:** Can We Trust LLM Citations? Evaluating Evidence Reliance in Retrieval-Augmented Generation

**Project Type:** Explainable AI / Responsible AI Research

**Status:** Initial Experimental Protocol (Version 1.0)

## 1. Research Question

**To what extent do LLMs actually rely on retrieved evidence when generating answers?**

Retrieval-Augmented Generation (RAG) allows LLMs to incorporate external information into generated answers and provide citations to supporting documents. However, a correct citation does not necessarily mean the model relied on the cited evidence when producing its answer.

This project investigates whether citations faithfully reflect evidence reliance or merely support answers that the model could generate independently.

The study builds on Wallat et al. (2025), *Correctness is not Faithfulness in Retrieval Augmented Generation Attributions*, and extends the investigation through controlled evidence interventions using synthetic documents.

## 2. Research Hypotheses

### H1 — Pretrained Knowledge vs. Retrieved Evidence

LLMs rely more heavily on their pretrained knowledge than on retrieved evidence when generating answers, shifting toward retrieved evidence when their pretrained knowledge is insufficient.

For this project, the model's ability to answer questions without RAG will serve as an observable indicator of available knowledge, rather than direct proof of what it learned during training.

### H6 — Post-Hoc Citation of Pretrained Knowledge

When LLMs possess relevant pretrained knowledge, they generate answers primarily based on that knowledge rather than retrieved evidence, but still cite retrieved sources to support their answers and make them appear more credible.

We will investigate this hypothesis by testing whether cited documents measurably influence generated answers, rather than assuming that citations reflect the model's actual information use.

## 3. Key XAI Concepts

### 3.1 Answer Correctness

Whether the model's answer is factually correct according to an independently established ground truth.

An answer can be correct regardless of whether the model used retrieved evidence.

### 3.2 Citation Correctness

Whether the document cited by the model actually supports the generated statement.

For example:

- Generated answer: "Marie Curie received her second Nobel Prize in 1911."
- Cited document: "Marie Curie received the Nobel Prize in Chemistry in 1911."

The citation is correct because the document supports the answer.

Citation correctness does not establish whether the document influenced the generation.

### 3.3 Citation Faithfulness

Whether the cited document had a genuine causal influence on the generation of the supported claim.

Following Wallat et al. (2025), a faithful citation must both support the generated claim and have causally contributed to that claim.

Because we cannot directly inspect the internal reasoning of a closed-weight LLM, we will investigate behavioral indicators of causal reliance using controlled evidence interventions.

### 3.4 Post-Hoc Citation

A potential failure mode in which an LLM generates an answer primarily from existing knowledge and then cites retrieved evidence that supports the answer without having meaningfully relied on that evidence.

Post-hoc citation will be treated as a hypothesis to investigate, not something that can be conclusively established merely because an answer remains unchanged after evidence removal.

## 4. Experimental Setup

### Model

One existing pretrained LLM accessed through AWS Bedrock.

The exact model and version will be selected before experimentation. No fine-tuning is planned.

### Dataset

A synthetic benchmark consisting of factual questions, supporting documents, and distractor documents.

The dataset will include multiple knowledge domains, such as science, history, technology, and environmental topics.

Questions will vary in familiarity, assessed initially through no-RAG model performance.

**Proposed initial scope:**

- Pilot: 6–10 factual cases.
- Full experiment: Approximately 30 factual cases.
- Each case will include one target fact and controlled document variants.

### RAG Setup

A fixed set of retrieved documents will be supplied to the LLM for each experimental condition.

Retrieval will initially be controlled rather than fully automated to ensure that the same evidence is available across comparable conditions.

The model will be instructed to provide a concise answer and cite supporting document IDs.

## 5. Experimental Conditions

| Condition | Description | Purpose |
|---|---|---|
| C0 — No RAG | Ask the question without supporting documents | Establish baseline model behavior |
| C1 — Original Evidence | Provide the original supporting document and distractors | Measure normal answer and citation behavior |
| C2 — Evidence Removal | Remove the target supporting document | Examine dependence on the document |
| C3 — Evidence Masking | Hide the critical factual information in the supporting document | Examine dependence on the specific fact |
| C4 — Evidence Replacement | Replace the target fact with a different value | Measure counterfactual evidence sensitivity |
| C5 — Negative Control | Modify an irrelevant passage while preserving the target fact | Check whether changes reflect relevant evidence rather than arbitrary document modifications |

All conditions will use the same underlying question.

Prompts, document formatting, and inference settings will remain consistent wherever possible. Document removal necessarily changes context length; masking and replacement provide complementary tests with more similar contexts.

## 6. Example Experiment

**Question:** What year did Marie Curie receive her second Nobel Prize?

**C0 — No RAG**

No supporting documents are provided.

The model's response establishes a baseline for answering independently.

**C1 — Original Evidence**

Document D1: "Marie Curie received her second Nobel Prize in 1911."

Observe the answer and citation.

**C2 — Evidence Removal**

Remove D1 while preserving unrelated documents.

Observe whether the answer or citation changes.

**C3 — Evidence Masking**

Document D1: "Marie Curie received her second Nobel Prize in [MASKED]."

Observe whether the model still provides 1911.

**C4 — Evidence Replacement**

Document D1: "Marie Curie received her second Nobel Prize in 1913."

Observe whether the model retains 1911, follows the modified evidence, abstains, or acknowledges a conflict.

**C5 — Negative Control**

Modify unrelated document content while leaving D1's factual statement unchanged.

Observe whether the answer remains stable.

The replacement condition is a counterfactual intervention designed to test evidence sensitivity, not an assertion that the historical fact has changed.

## 7. Measurements and Evaluation

### Primary Measurements

| Metric | Operational Definition |
|---|---|
| Answer accuracy | Proportion of responses matching verified ground truth |
| Citation correctness | Proportion of cited claims supported by their referenced documents |
| Answer-change rate | Proportion of matched experimental pairs in which the substantive answer changes |
| Counterfactual following rate | Proportion of eligible cases where the answer changes to match the replacement fact |
| Evidence-removal sensitivity | Proportion of cases where removing relevant evidence changes the answer |
| Negative-control sensitivity | Proportion of cases where changing irrelevant evidence changes the answer |
| Citation-change rate | Proportion of matched pairs where cited document IDs change |

### Citation Faithfulness Assessment

We will compare responses across original and modified evidence conditions.

Particular attention will be given to cases where:

1. The model produces a correct answer and a supporting citation.
2. The model gives the same answer when the cited evidence is removed or masked.
3. The model follows a deliberately changed fact in the cited document.
4. The model changes citations without changing its answer.
5. The model cites evidence even when experiments indicate limited sensitivity to that evidence.

These patterns will help evaluate citation faithfulness, but no single intervention outcome will be considered definitive proof of a model's internal information source.

We will report observed behavioral evidence of reliance separately from stronger claims about causal mechanisms.

## 8. Analysis Plan

Results will be compared across evidence conditions and question categories.

The analysis will include:

- Answer accuracy and citation correctness by condition.
- Matched answer changes following document interventions.
- Comparison of relevant-evidence interventions with negative controls.
- Differences in evidence sensitivity between questions answered correctly and incorrectly without RAG.
- Case studies of potentially unfaithful citations.

For the initial experiment, descriptive statistics and visualizations will be emphasized.

If the sample size permits, we will calculate bootstrap confidence intervals by resampling independent factual cases rather than treating every intervention response as independent.

Ambiguous answers and citation judgments will be manually reviewed using documented evaluation criteria.

## 9. Expected XAI Contribution

This project aims to contribute a reproducible experimental framework for studying evidence reliance and citation faithfulness in RAG.

Its proposed contribution includes:

1. A controlled synthetic benchmark with reproducible evidence interventions.
2. A systematic comparison between citation correctness and behavioral evidence reliance.
3. An investigation of how baseline model knowledge relates to citation behavior.
4. An interactive visualization demonstrating how retrieved-document modifications influence generated answers and citations.

The project is intended to evaluate the trustworthiness of model-generated citations rather than develop a new explanation algorithm.

## 10. Limitations and Responsible AI Considerations

**Unobservable pretrained knowledge:** No-RAG performance cannot conclusively establish which facts a model learned during pretraining.

**Black-box interpretability:** The experiment evaluates observable model behavior, not internal neural mechanisms.

**Causal attribution limitations:** An unchanged answer does not prove that retrieved evidence was ignored. Multiple information sources may influence the same response.

**Synthetic data limitations:** Controlled documents improve experimental validity but may not capture the complexity of real-world retrieval environments.

**Model sensitivity:** Findings may depend on the selected model, prompt wording, decoding settings, and document presentation.

**Citation risks:** Citations can increase users' confidence in AI-generated answers even when they do not accurately reflect evidence reliance. This is particularly important for research, education, and AI-assisted decision-making.

## 11. Reproducibility Requirements

The final repository will include:

- Synthetic dataset and ground-truth metadata
- Document intervention scripts
- AWS Bedrock inference code
- Model identifier, version, Region, and generation settings
- Saved prompts, outputs, citations, and token usage
- Evaluation scripts and scoring criteria
- Dependency requirements and setup instructions
- Statistical analysis and visualizations
- Limitations and relevant future work

API credentials will not be included in the repository.

## 12. Future Work — Project 2

Project 2 will extend the same experimental framework to investigate:

- Conflicts between pretrained knowledge and retrieved evidence (H2).
- Prioritization of prompt information, pretrained knowledge, and RAG (H3).
- Differences in behavior across multiple LLMs (H4).
- Reliance on incorrect retrieved information under limited baseline knowledge (H5).

A longer-term extension will investigate how retrieved evidence influences LLM recommendations and whether the model's explanations faithfully represent the factors that affected those decisions.

## Reference

Wallat, J., Heuss, M., de Rijke, M., & Anand, A. (2025). *Correctness is not Faithfulness in Retrieval Augmented Generation Attributions*. Proceedings of ICTIR 2025, 22–32. https://doi.org/10.1145/3731120.3744592