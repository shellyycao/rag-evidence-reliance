# XAI Research Project: Understanding How LLMs Rely on Retrieved Evidence

## 1. Project Background and Motivation

I am working on an Explainable AI (XAI) class project. My goal is to develop a deeper understanding of how large language models (LLMs) use information when generating answers, particularly the relationship between their pretrained knowledge and externally retrieved information through Retrieval-Augmented Generation (RAG).

I am interested in whether LLMs genuinely rely on the evidence they cite or whether they sometimes generate answers primarily from pretrained knowledge and subsequently cite supporting documents to make those answers appear more credible.

More broadly, I want to understand how information influences LLM outputs and eventually their recommendations and decisions.

This is an XAI and Responsible AI research project, **not simply a RAG chatbot development project**. The technical pipeline should support controlled experiments investigating citation correctness, citation faithfulness, and evidence reliance.

I plan to divide this research into two class projects, with potential further extensions. Right now, I only want to implement Project 1, but the architecture should be reusable for future experiments.

---

## 2. Main Research Question

**To what extent do LLMs actually rely on retrieved evidence when generating answers?**

The key distinction is between:

**Citation correctness:** Does the cited document actually support the model's generated claim?

**Citation faithfulness:** Did the cited document genuinely influence the generation of that claim?

A citation can be correct without necessarily being faithful. For example, an LLM might already know that Marie Curie received her second Nobel Prize in 1911, generate that answer using pretrained knowledge, and cite a retrieved document that happens to contain the same fact.

I want to investigate this distinction experimentally.

### Foundational Literature

My primary reference is:

Wallat, J., Heuss, M., de Rijke, M., & Anand, A. (2025). *Correctness is not Faithfulness in Retrieval Augmented Generation Attributions.*

[https://arxiv.org/abs/2412.18004](https://arxiv.org/abs/2412.18004)

DOI: [https://doi.org/10.1145/3731120.3744592](https://doi.org/10.1145/3731120.3744592)

I want to understand and adapt relevant methods from this paper, especially evidence manipulation and counterfactual testing.

I am not necessarily reproducing the entire paper. My goal is to build a smaller, controlled experiment that extends or applies its central ideas.

---

## 3. Research Hypotheses

I have developed six working hypotheses across the broader research program.

### Current Project 1 Hypotheses

**H1 — Pretrained Knowledge vs. Retrieved Evidence**

LLMs rely more heavily on their pretrained knowledge than on retrieved evidence when generating answers, shifting toward retrieved evidence when their pretrained knowledge is insufficient.

For Project 1, I will use no-RAG baseline performance as an observable indicator of available knowledge. I understand that this does not directly reveal what the model learned during pretraining.

**H6 — Post-Hoc Citation of Pretrained Knowledge**

When LLMs possess relevant pretrained knowledge, they generate answers primarily based on that knowledge rather than retrieved evidence, but still cite retrieved sources to support their answers and make them appear more credible.

This will be investigated using evidence interventions. I understand that unchanged answers following evidence removal do not, by themselves, prove post-hoc citation.

### Future Hypotheses — Not Part of Project 1

**H2 — Conflicting Information**

LLMs rely more heavily on retrieved evidence when it contradicts their pretrained knowledge.

**H3 — Information Source Prioritization**

LLMs prioritize information sources in the following order:

Prompt input > Pretrained knowledge > RAG evidence.

**H4 — Consistency Across Models**

Different LLMs exhibit similar patterns of information-source prioritization and evidence reliance.

**H5 — Reliance on RAG in the Absence of Pretrained Knowledge**

When LLMs lack relevant pretrained knowledge, they treat retrieved evidence as ground truth when generating answers, even if that information is incorrect.

H5 has been set aside because determining whether an LLM truly lacks pretrained knowledge is methodologically difficult. It may be revised into an operationally testable hypothesis later.

**Important:** Do not expand Project 1 to test all six hypotheses. Its current focus is H1 and H6.

---

## 4. Overall Research Roadmap

### Project 1 — Current XAI Class Project

**Focus: Citation correctness, citation faithfulness, and evidence reliance.**

Use one pretrained LLM to investigate how generated answers and citations respond to controlled modifications of retrieved evidence.

Main activities:

1. Establish no-RAG baseline behavior.
2. Supply retrieved supporting documents.
3. Remove relevant evidence.
4. Mask critical information.
5. Replace factual information with counterfactual values.
6. Modify irrelevant evidence as a negative control.
7. Compare answers and citations across conditions.
8. Evaluate citation correctness and behavioral evidence reliance.

This project must stand alone as a complete, functional XAI research artifact.

### Project 2 — Future Class Project

**Focus: Knowledge conflicts, information-source prioritization, and model comparison.**

Extend Project 1's framework to:

1. Test how LLMs react to deliberately incorrect retrieved information, including obvious contradictions such as "1 + 1 = 3."
2. Compare information supplied in user prompts versus RAG documents versus pretrained knowledge.
3. Investigate which information sources models prioritize when they conflict.
4. Repeat experiments across multiple LLMs, potentially from different model families.
5. Compare citation faithfulness, conflict recognition, and misinformation acceptance.

Project 2 will address H2, H3, H4, and potentially H5.

### Potential Longer-Term Research

**Decision and recommendation traceability.**

I eventually want to investigate how information influences LLM recommendations, not just factual answers.

For example, if an LLM recommends Project A to a student, can we establish which retrieved documents or user-provided facts influenced that recommendation?

Could incorrect retrieved evidence change a recommendation without being mentioned in the explanation?

The progression is:

Evidence reliance → Information-source prioritization → Recommendation influence → Explanation faithfulness.

This is future work and should not expand the current implementation scope.

---

## 5. Technical Decisions

### LLM

I want to use **one existing pretrained LLM through AWS Bedrock**, preferably an Anthropic Claude model available in my AWS account.

I do not want to train or fine-tune a new LLM.

The exact model, model ID, and AWS Region have not yet been finalized.

### Computing and Budget

- I have approximately $100 in AWS credits remaining.
- My available local computing resources are limited.
- I can use Google Colab or local Python for experimentation.
- I prefer Bedrock-hosted inference so I do not need to run a large model locally.
- I want to avoid unnecessary AWS infrastructure costs.
- A working spending target of approximately $25 for Project 1 is reasonable, subject to actual pricing and credit eligibility.

### Preferred Technologies

- Python
- AWS Bedrock
- Boto3
- pandas
- NumPy
- scipy / statsmodels
- matplotlib / seaborn
- JSONL for experiment outputs
- GitHub for version control
- Potentially Streamlit for the final interactive XAI artifact

I already have experience with Python, AWS, data pipelines, and Streamlit, so I want to use this project to strengthen LLM engineering and evaluation skills rather than focus primarily on infrastructure.

### RAG Architecture

For Project 1, I prefer **a lightweight, controlled RAG setup rather than Bedrock Knowledge Bases or OpenSearch**.

The primary experiment should use fixed, predetermined evidence documents so that retrieval variability does not confound the investigation of model behavior.

A simple retriever can be added to demonstrate a functioning RAG workflow, but the causal experiments should control exactly which documents the model sees.

I want the architecture to support adding other models and prompt-based interventions in Project 2 without major refactoring.

---

## 6. Dataset Design

I plan to construct a small synthetic benchmark involving multiple knowledge domains.

Potential domains include:

- Science and astronomy
- History
- Technology and AI
- Wildlife and environmental science
- Fictional entities and invented facts

I prefer multiple domains rather than restricting the entire experiment to one subject.

### Dataset Dimensions

The broader research plan includes two dimensions:

**Knowledge familiarity**

- Highly familiar facts
- Less familiar facts
- Novel or fictional facts

For Project 1, knowledge familiarity should be assessed using the model's baseline performance without RAG, rather than assuming the model knows or doesn't know a particular fact.

**Misinformation difficulty**

- Obvious falsehoods
- Subtle or plausible misinformation

Systematic misinformation difficulty comparisons belong primarily to Project 2. Project 1 can still use factual replacements as a counterfactual testing method.

### Proposed Project 1 Dataset Size

- Pilot: 6–10 independent factual cases.
- Full experiment target: Approximately 30 independent factual cases.
- Each case should include a question, verified ground truth where applicable, and supporting documents.
- Add one or two distractor documents per case.
- Generate intervention variants programmatically.

Each relevant case should support evidence removal, masking, factual replacement, and negative-control modifications.

The dataset must be versioned, documented, and reproducible.

### Example

Question: "What year did Marie Curie receive her second Nobel Prize?"

Original document:

D1: "Marie Curie received her second Nobel Prize in 1911."

Counterfactual document:

D1: "Marie Curie received her second Nobel Prize in 1913."

Masked document:

D1: "Marie Curie received her second Nobel Prize in [MASKED]."

For the removal condition, D1 is omitted.

For the negative-control condition, an unrelated piece of information is modified while the correct answer remains available.

We want to understand whether the model's answer and citation respond to these changes.

---

## 7. Project 1 Experimental Conditions

| ID | Condition            | Description                                                    | Research Purpose                                       |
| -- | -------------------- | -------------------------------------------------------------- | ------------------------------------------------------ |
| C0 | No RAG               | Ask the question without external evidence                     | Establish baseline model behavior                      |
| C1 | Original Evidence    | Provide correct supporting documents                           | Measure normal answers and citations                   |
| C2 | Evidence Removal     | Remove the relevant supporting document                        | Investigate dependence on the evidence                 |
| C3 | Evidence Masking     | Mask the critical factual information                          | Test reliance on specific content                      |
| C4 | Evidence Replacement | Replace the target fact with a different value                 | Evaluate counterfactual evidence sensitivity           |
| C5 | Negative Control     | Change irrelevant information without changing the target fact | Test whether effects are specific to relevant evidence |

The same underlying question should be used across all experimental conditions.

The input structure and generation configuration should remain consistent wherever possible.

### Important Experimental Controls

- Keep model and model version fixed.
- Use consistent prompts and generation settings.
- Keep document IDs stable across conditions where possible.
- Avoid unintentionally changing unrelated information during interventions.
- Record the exact evidence passed to the model.
- Preserve model outputs without manually editing them.
- Record response metadata, token usage, errors, and retry behavior.
- Where feasible, repeat experiments to examine response variability.
- Use negative controls to distinguish relevant-evidence sensitivity from generic sensitivity to document changes.

---

## 8. Evaluation Metrics

### Answer Correctness

Does the generated answer match independently verified ground truth?

### Citation Correctness

Does the document cited by the model support its generated claim?

Important: Citation support and factual truth are different. A document can support a claim that is objectively false.

### Answer-Change Rate

How frequently does the substantive answer change between matched experimental conditions?

### Evidence-Removal Sensitivity

Does removing a relevant cited document affect the answer?

### Counterfactual Following Rate

Does the answer change to match a deliberately modified factual value in the supplied evidence?

### Citation-Change Rate

Does the cited document change between experimental conditions?

### Negative-Control Sensitivity

Does changing unrelated information affect the answer?

### Citation Faithfulness

Citation faithfulness is the central XAI concept.

I want to investigate whether cited evidence has a genuine causal influence on the model's generated answer.

Since a closed-weight Claude model does not expose internal activations or its actual generation mechanism, we will estimate behavioral evidence reliance through counterfactual interventions.

We must avoid overclaiming that an unchanged answer after evidence removal proves the model ignored the evidence.

The evaluation should clearly distinguish:

1. Factual answer correctness.
2. Citation support correctness.
3. Observable sensitivity to relevant evidence interventions.
4. Stronger claims about citation faithfulness that cannot be conclusively established through black-box testing alone.

---

## 9. Statistical Analysis

I want to compare responses across experimental conditions and different levels of baseline knowledge.

Potential analysis includes:

- Overall answer accuracy and citation correctness.
- Comparison of original versus modified evidence conditions.
- Evidence-removal and masking effects.
- Counterfactual following rates.
- Relationships between no-RAG performance and evidence sensitivity.
- Qualitative analysis of unusual or potentially unfaithful citations.

Because multiple conditions are tested on the same underlying questions, the analysis should use paired comparisons.

For confidence intervals, use bootstrap resampling at the independent factual-case level rather than treating every response as an independent observation.

With a small sample size, prioritize clear descriptive analysis and uncertainty over unsupported claims of statistical significance.

---

## 10. Pipeline Requirements

I want Claude to help me design and implement the technical pipeline.

The conceptual architecture is:

**Synthetic Dataset → Controlled Retrieval → Evidence Intervention → AWS Bedrock Inference → Output Logging → Evaluation → Visualization**

The pipeline should include:

### Dataset Module

Stores questions, verified answers, supporting documents, distractors, and intervention metadata.

### Retrieval Module

Selects the documents supplied to the LLM. For the primary experiment, this must support fixed evidence sets.

### Intervention Module

Supports:

- Original evidence
- Evidence removal
- Evidence masking
- Factual replacement
- Irrelevant-document modification

Interventions must be reproducible and preferably programmatically generated.

### Inference Module

Calls the selected Claude model through AWS Bedrock.

It should accept a question and selected evidence documents, construct a consistent prompt, invoke the model, and return the response and metadata.

### Logging Module

Records:

- Case ID
- Experimental condition
- Model ID and configuration
- Full question and evidence provided
- Prompt version
- Raw model output
- Parsed answer
- Parsed citations
- Token usage
- Estimated API cost
- Timestamp
- Execution status or errors

Results should be saved incrementally so experiments can resume after interruptions.

### Evaluation Module

Calculates the experimental metrics and supports manual review of ambiguous citations.

### Visualization Module

Generates aggregate comparison charts and case-level comparisons.

A final Streamlit application is desirable but should not take priority over valid experiments.

---

## 11. Final XAI Artifact

My class project is graded on three categories:

### Project Artifact — 100 points

- Demonstrates XAI or Responsible AI concepts — 15
- Makes a novel contribution — 20
- Is substantially developed and functional — 20
- Follows appropriate best practices — 15
- Includes sufficient documentation — 15
- Is polished as a professional portfolio piece — 15

### Responsible AI Rigor and Evaluation — 75 points

- Relevant literature and course grounding — 15
- Clear research question — 10
- Appropriate experimental evidence — 20
- Limitations, uncertainty, and responsible AI considerations — 15
- Significance and future work — 15

### Creativity and Ambition — 25 points

- Intellectual or technical ambition — 10
- Creativity in approach or contribution — 10
- Engaging communication — 5

**Total: 200 points.**

The project must be academically rigorous, technically functional, reproducible, and professionally presented.

### Planned Deliverables

1. Well-documented Python codebase.
2. Controlled synthetic benchmark.
3. Working AWS Bedrock inference and experiment pipeline.
4. Counterfactual evidence-intervention framework.
5. Quantitative XAI evaluation.
6. Research visualizations.
7. GitHub repository with setup and execution instructions.
8. Research report describing methods, results, limitations, and future work.
9. Potential Streamlit Evidence Reliance Explorer.

### Proposed Streamlit Artifact

The **Evidence Reliance Explorer** would allow someone to:

- Select an experimental question.
- View retrieved documents.
- Switch between original, removed, masked, and counterfactual evidence.
- Compare actual model answers and citations.
- Explore aggregate evidence-reliance metrics.
- Inspect examples where citation correctness and behavioral evidence reliance diverge.

The dashboard should use real saved experiment outputs. Live API querying is optional.

---

## 12. Responsible AI and Research Limitations

The project should explicitly acknowledge:

- We cannot directly observe what a closed-weight model learned during pretraining.
- No-RAG performance is only a behavioral proxy for accessible knowledge.
- Answer stability does not prove that retrieved evidence was ignored.
- Citation correctness is not equivalent to citation faithfulness.
- Synthetic evidence may not reflect real-world retrieval complexity.
- Prompts, model versions, and decoding settings can affect outcomes.
- Model-generated explanations should not automatically be treated as faithful accounts of internal reasoning.
- Misleading or unfaithful citations may cause users to trust generated information more than they should.

The project concerns the reliability and transparency of AI-generated explanations and citations.

---

## 13. Implementation Plan

### 1 — Research Foundation and Bedrock Setup

- Review Wallat et al.'s methodology.
- Select one Claude model.
- Verify Bedrock access and pricing.
- Configure AWS credentials securely.
- Implement a minimal inference function.
- Test document-ID citation generation.

### 2 — Dataset and Interventions

- Create 6–10 pilot cases.
- Build document representations.
- Implement fixed evidence retrieval.
- Implement removal, masking, replacement, and negative controls.
- Validate the generated interventions.

### &#x20;3 — Pilot and Evaluation

- Execute the experimental conditions.
- Save model responses and citations.
- Implement initial evaluation metrics.
- Manually inspect ambiguous cases.
- Revise the experimental protocol if needed.

### 4 — Full Experiments and Analysis

- Expand toward approximately 30 cases.
- Run the experiments.
- Analyze answer and citation changes.
- Calculate summary metrics and uncertainty.
- Identify representative failure cases.

### 5 — Final Artifact

- Build visualizations and the optional Streamlit explorer.
- Write the research report.
- Document all setup and reproduction steps.
- Prepare the presentation.
- Organize the repository as a professional portfolio piece.

---

## 14. Important Instructions for Claude

I want your help primarily with the **technical implementation**, while preserving the research design described above.

Please follow these principles:

1. **Do not expand Project 1 into Project 2.** Only implement H1 and H6 and the current evidence-reliance experiments.
2. **Do not start by building a complex production RAG system.** Start with controlled document inputs and a minimal Bedrock inference pipeline.
3. **Prioritize experimental validity over infrastructure complexity.**
4. **Keep the code modular and reusable** so additional models, prompt interventions, and recommendation experiments can be added later.
5. **Do not assume citations prove evidence reliance.** The distinction between citation correctness and citation faithfulness is central.
6. **Do not interpret model behavior as direct access to its internal reasoning.**
7. **Keep AWS costs low**, avoid unnecessary managed infrastructure, and track token usage.
8. **Use a small working pilot before scaling the dataset.**
9. **Keep the project academically rigorous and portfolio-ready.**
10. **Work with me step by step.** Explain the architecture and implementation choices before introducing unnecessary complexity.

The immediate technical goal is to select and configure one Claude model through AWS Bedrock, implement a minimal reproducible inference pipeline, and test it using a few manually controlled documents.

Do not build the entire system at once. Start with the smallest functional experiment and expand from there.
