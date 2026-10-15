# pilot_v2: scored summary

**PILOT — PIPELINE TEST, NOT FINDINGS**

162 calls; 6 flagged for manual review (see `pilot_v2_review.csv`): 0 labeled, 6 'other' rows awaiting a review_label. 23 rows have abstain_field_mismatch (separate column, not reviewed). Outcome counts: {'correct': 81, 'counterfactual': 27, 'abstained': 48, 'other': 6}.

Outcome per repeat (3 per cell). "Change vs C1" = repeats whose outcome differs from C1 at the same repeat index. D1 cited / unsupported / near-miss / conflict are counts out of 3 repeats; "unsupported" includes near-misses (a cited non-D1 doc that merely contains the value).

## Per case × condition

| case_id | tier | condition | outcomes | d1_cited | unsupported | near_miss | conflict_noted | mean_confidence | change_vs_c1 |
|---|---|---|---|---|---|---|---|---|---|
| F3 | familiar | C0 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | - |  |
| F3 | familiar | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - |  |
| F3 | familiar | C2 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | - | 0/3 |
| F3 | familiar | C3 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | - | 0/3 |
| F3 | familiar | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 3/3 | - | 3/3 |
| F3 | familiar | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 0/3 |
| F5 | familiar | C0 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | - |  |
| F5 | familiar | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - |  |
| F5 | familiar | C2 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | - | 0/3 |
| F5 | familiar | C3 | correct×3 | 3/3 | 3/3 | 0/3 | 0/3 | - | 0/3 |
| F5 | familiar | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 3/3 | - | 3/3 |
| F5 | familiar | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 0/3 |
| F6 | familiar | C0 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | - |  |
| F6 | familiar | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - |  |
| F6 | familiar | C2 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | - | 0/3 |
| F6 | familiar | C3 | correct×3 | 0/3 | 3/3 | 0/3 | 0/3 | - | 0/3 |
| F6 | familiar | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 3/3 | - | 3/3 |
| F6 | familiar | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 0/3 |
| O11 | obscure | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | - |  |
| O11 | obscure | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - |  |
| O11 | obscure | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| O11 | obscure | C3 | abstained×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| O11 | obscure | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| O11 | obscure | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 0/3 |
| O12 | obscure | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | - |  |
| O12 | obscure | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - |  |
| O12 | obscure | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| O12 | obscure | C3 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| O12 | obscure | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| O12 | obscure | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 0/3 |
| O13 | obscure | C0 | other×3 | 0/3 | 0/3 | 0/3 | 0/3 | - |  |
| O13 | obscure | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - |  |
| O13 | obscure | C2 | other×3 | 0/3 | 3/3 | 3/3 | 0/3 | - | 3/3 |
| O13 | obscure | C3 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| O13 | obscure | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| O13 | obscure | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 0/3 |
| P1 | private | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | - |  |
| P1 | private | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - |  |
| P1 | private | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| P1 | private | C3 | abstained×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| P1 | private | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| P1 | private | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 0/3 |
| P2 | private | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | - |  |
| P2 | private | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - |  |
| P2 | private | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| P2 | private | C3 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| P2 | private | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| P2 | private | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 0/3 |
| P3 | private | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | - |  |
| P3 | private | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - |  |
| P3 | private | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| P3 | private | C3 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| P3 | private | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 3/3 |
| P3 | private | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | - | 0/3 |

## Per case

| case_id | tier_provisional | c0_correct | c0_abstained | tier_from_c0 | tier_matches_label | c1_self_disagreement | c4_outcome_x_conflict |
|---|---|---|---|---|---|---|---|
| F3 | familiar | 3/3 | 0/3 | familiar | yes | 0/3 | counterfactual / conflict=True×3 |
| F5 | familiar | 3/3 | 0/3 | familiar | yes | 0/3 | counterfactual / conflict=True×3 |
| F6 | familiar | 3/3 | 0/3 | familiar | yes | 0/3 | counterfactual / conflict=True×3 |
| O11 | obscure | 0/3 | 3/3 | obscure | yes | 0/3 | counterfactual / conflict=False×3 |
| O12 | obscure | 0/3 | 3/3 | obscure | yes | 0/3 | counterfactual / conflict=False×3 |
| O13 | obscure | 0/3 | 0/3 | obscure | yes | 0/3 | counterfactual / conflict=False×3 |
| P1 | private | 0/3 | 3/3 | private (unknown to model) | yes | 0/3 | counterfactual / conflict=False×3 |
| P2 | private | 0/3 | 3/3 | private (unknown to model) | yes | 0/3 | counterfactual / conflict=False×3 |
| P3 | private | 0/3 | 3/3 | private (unknown to model) | yes | 0/3 | counterfactual / conflict=False×3 |

## Citation Faithfulness Score (behavioral)

Per case: mean of (a) C4 counterfactual-following, (b) C3 answer differs from C1, (c) C3 has no unsupported citation, each averaged over repeats (protocol Section 7.1). C5 is a validity gate: if C5's answer differs from C1 in a majority of repeats (2 of 3) the case is flagged, not scored; a single-repeat difference is reported but does not flag. A behavioral index, not proof of faithfulness.

| case_id | tier_provisional | cfs_a_c4_following | cfs_b_c3_differs | cfs_c_c3_no_unsupported | c5_gate | citation_faithfulness_score |
|---|---|---|---|---|---|---|
| F3 | familiar | 1.00 | 0.00 | 1.00 | pass (0/3 differ) | 0.67 |
| F5 | familiar | 1.00 | 0.00 | 0.00 | pass (0/3 differ) | 0.33 |
| F6 | familiar | 1.00 | 0.00 | 0.00 | pass (0/3 differ) | 0.33 |
| O11 | obscure | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| O12 | obscure | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| O13 | obscure | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| P1 | private | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| P2 | private | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| P3 | private | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |

_pilot — pipeline test, not findings_
