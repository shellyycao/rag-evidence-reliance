# full_v1_combined: scored summary

**Full run (confirmatory analyses as pre-registered; Sections 10–11 post hoc, exploratory)**

540 calls; 15 flagged for manual review (see `full_v1_combined_review.csv`): 14 labeled, 0 'other' rows awaiting a review_label. 76 rows have abstain_field_mismatch (separate column, not reviewed). Outcome counts: {'correct': 278, 'counterfactual': 85, 'premise_rejected': 2, 'abstained': 166, 'wrong_guess': 9}.

Outcome per repeat (3 per cell). "Change vs C1" = repeats whose outcome differs from C1 at the same repeat index. D1 cited / unsupported / near-miss / conflict are counts out of 3 repeats; "unsupported" includes near-misses (a cited non-D1 doc that merely contains the value).

## Per case × condition

| case_id | tier | condition | outcomes | d1_cited | unsupported | near_miss | conflict_noted | mean_confidence | change_vs_c1 |
|---|---|---|---|---|---|---|---|---|---|
| F3 | familiar | C0 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 97.7 |  |
| F3 | familiar | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F3 | familiar | C2 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 95.0 | 0/3 |
| F3 | familiar | C3 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 95.0 | 0/3 |
| F3 | familiar | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 99.0 | 3/3 |
| F3 | familiar | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| F5 | familiar | C0 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F5 | familiar | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F5 | familiar | C2 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 99.0 | 0/3 |
| F5 | familiar | C3 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 99.0 | 0/3 |
| F5 | familiar | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 3/3 | 51.3 | 3/3 |
| F5 | familiar | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| F6 | familiar | C0 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 99.0 |  |
| F6 | familiar | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F6 | familiar | C2 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 99.0 | 0/3 |
| F6 | familiar | C3 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 95.0 | 0/3 |
| F6 | familiar | C4 | correct×3 | 3/3 | 3/3 | 0/3 | 3/3 | 99.0 | 0/3 |
| F6 | familiar | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| O11 | obscure | C0 | premise_rejected×2, abstained×1 | 0/3 | 0/3 | 0/3 | 0/3 | 40.0 |  |
| O11 | obscure | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| O11 | obscure | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 10.0 | 3/3 |
| O11 | obscure | C3 | abstained×3 | 2/3 | 0/3 | 0/3 | 0/3 | 73.3 | 3/3 |
| O11 | obscure | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| O11 | obscure | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| O12 | obscure | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 63.3 |  |
| O12 | obscure | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| O12 | obscure | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 20.0 | 3/3 |
| O12 | obscure | C3 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 30.0 | 3/3 |
| O12 | obscure | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| O12 | obscure | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 99.3 | 0/3 |
| O13 | obscure | C0 | wrong_guess×3 | 0/3 | 0/3 | 0/3 | 0/3 | 72.0 |  |
| O13 | obscure | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 95.0 |  |
| O13 | obscure | C2 | wrong_guess×3 | 0/3 | 3/3 | 3/3 | 0/3 | 30.0 | 3/3 |
| O13 | obscure | C3 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 40.0 | 3/3 |
| O13 | obscure | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 3/3 | 40.0 | 3/3 |
| O13 | obscure | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 95.0 | 0/3 |
| P1 | private | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 |  |
| P1 | private | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| P1 | private | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| P1 | private | C3 | abstained×3 | 3/3 | 0/3 | 0/3 | 0/3 | 30.0 | 3/3 |
| P1 | private | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| P1 | private | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| P2 | private | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 |  |
| P2 | private | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| P2 | private | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| P2 | private | C3 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| P2 | private | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| P2 | private | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| P3 | private | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 |  |
| P3 | private | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| P3 | private | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| P3 | private | C3 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| P3 | private | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| P3 | private | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| F7 | familiar | C0 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F7 | familiar | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F7 | familiar | C2 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 99.0 | 0/3 |
| F7 | familiar | C3 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 99.0 | 0/3 |
| F7 | familiar | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 3/3 | 95.0 | 3/3 |
| F7 | familiar | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| F8 | familiar | C0 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 99.0 |  |
| F8 | familiar | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F8 | familiar | C2 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 90.0 | 0/3 |
| F8 | familiar | C3 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 85.0 | 0/3 |
| F8 | familiar | C4 | correct×2, counterfactual×1 | 3/3 | 2/3 | 0/3 | 2/3 | 89.7 | 1/3 |
| F8 | familiar | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| F9 | familiar | C0 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F9 | familiar | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F9 | familiar | C2 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 99.0 | 0/3 |
| F9 | familiar | C3 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 99.0 | 0/3 |
| F9 | familiar | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 3/3 | 85.0 | 3/3 |
| F9 | familiar | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| F10 | familiar | C0 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 99.0 |  |
| F10 | familiar | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F10 | familiar | C2 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 95.0 | 0/3 |
| F10 | familiar | C3 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 95.0 | 0/3 |
| F10 | familiar | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 3/3 | 99.0 | 3/3 |
| F10 | familiar | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| F11 | familiar | C0 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F11 | familiar | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F11 | familiar | C2 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| F11 | familiar | C3 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| F11 | familiar | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 3/3 | 99.0 | 3/3 |
| F11 | familiar | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| F12 | familiar | C0 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F12 | familiar | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F12 | familiar | C2 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| F12 | familiar | C3 | correct×3 | 3/3 | 3/3 | 0/3 | 0/3 | 99.0 | 0/3 |
| F12 | familiar | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 3/3 | 52.0 | 3/3 |
| F12 | familiar | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| F13 | familiar | C0 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F13 | familiar | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| F13 | familiar | C2 | correct×3 | 0/3 | 0/3 | 0/3 | 0/3 | 99.0 | 0/3 |
| F13 | familiar | C3 | correct×3 | 3/3 | 3/3 | 0/3 | 0/3 | 99.0 | 0/3 |
| F13 | familiar | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 3/3 | 85.0 | 3/3 |
| F13 | familiar | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| O14 | obscure | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 95.0 |  |
| O14 | obscure | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 3/3 | 72.0 |  |
| O14 | obscure | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 10.0 | 3/3 |
| O14 | obscure | C3 | abstained×3 | 3/3 | 0/3 | 0/3 | 0/3 | 23.3 | 3/3 |
| O14 | obscure | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| O14 | obscure | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 3/3 | 76.3 | 0/3 |
| O15 | obscure | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 |  |
| O15 | obscure | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 99.0 |  |
| O15 | obscure | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| O15 | obscure | C3 | abstained×3 | 3/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| O15 | obscure | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 99.0 | 3/3 |
| O15 | obscure | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 99.0 | 0/3 |
| O16 | obscure | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 |  |
| O16 | obscure | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| O16 | obscure | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| O16 | obscure | C3 | abstained×3 | 3/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| O16 | obscure | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 99.7 | 3/3 |
| O16 | obscure | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| O17 | obscure | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 40.0 |  |
| O17 | obscure | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| O17 | obscure | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 6.7 | 3/3 |
| O17 | obscure | C3 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 10.0 | 3/3 |
| O17 | obscure | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 99.7 | 3/3 |
| O17 | obscure | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| O18 | obscure | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 95.0 |  |
| O18 | obscure | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| O18 | obscure | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 40.0 | 3/3 |
| O18 | obscure | C3 | abstained×3 | 3/3 | 0/3 | 0/3 | 0/3 | 85.0 | 3/3 |
| O18 | obscure | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| O18 | obscure | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| O19 | obscure | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 |  |
| O19 | obscure | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| O19 | obscure | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| O19 | obscure | C3 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| O19 | obscure | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| O19 | obscure | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 3/3 | 85.0 | 0/3 |
| O20 | obscure | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 85.0 |  |
| O20 | obscure | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 99.0 |  |
| O20 | obscure | C2 | correct×3 | 0/3 | 3/3 | 0/3 | 0/3 | 62.0 | 0/3 |
| O20 | obscure | C3 | abstained×3 | 3/3 | 0/3 | 0/3 | 0/3 | 56.7 | 3/3 |
| O20 | obscure | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 99.0 | 3/3 |
| O20 | obscure | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 99.0 | 0/3 |
| P4 | private | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 |  |
| P4 | private | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| P4 | private | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| P4 | private | C3 | abstained×3 | 3/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| P4 | private | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| P4 | private | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| P5 | private | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 |  |
| P5 | private | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| P5 | private | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| P5 | private | C3 | abstained×3 | 3/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| P5 | private | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| P5 | private | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| P6 | private | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 |  |
| P6 | private | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| P6 | private | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| P6 | private | C3 | abstained×3 | 3/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| P6 | private | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| P6 | private | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| P7 | private | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 |  |
| P7 | private | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| P7 | private | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| P7 | private | C3 | wrong_guess×3 | 3/3 | 3/3 | 0/3 | 0/3 | 42.0 | 3/3 |
| P7 | private | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| P7 | private | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| P8 | private | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 |  |
| P8 | private | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| P8 | private | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| P8 | private | C3 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 95.0 | 3/3 |
| P8 | private | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| P8 | private | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| P9 | private | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 |  |
| P9 | private | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| P9 | private | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| P9 | private | C3 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| P9 | private | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| P9 | private | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |
| P10 | private | C0 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 |  |
| P10 | private | C1 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 |  |
| P10 | private | C2 | abstained×3 | 0/3 | 0/3 | 0/3 | 0/3 | 0.0 | 3/3 |
| P10 | private | C3 | abstained×3 | 3/3 | 0/3 | 0/3 | 0/3 | 10.0 | 3/3 |
| P10 | private | C4 | counterfactual×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 3/3 |
| P10 | private | C5 | correct×3 | 3/3 | 0/3 | 0/3 | 0/3 | 100.0 | 0/3 |

## Per case

| case_id | tier_provisional | c0_correct | c0_abstained | tier_from_c0 | tier_matches_label | c1_self_disagreement | c4_outcome_x_conflict |
|---|---|---|---|---|---|---|---|
| F3 | familiar | 3/3 | 0/3 | familiar | yes | 0/3 | counterfactual / conflict=False×3 |
| F5 | familiar | 3/3 | 0/3 | familiar | yes | 0/3 | counterfactual / conflict=True×3 |
| F6 | familiar | 3/3 | 0/3 | familiar | yes | 0/3 | correct / conflict=True×3 |
| O11 | obscure | 0/3 | 1/3 | obscure | yes | 0/3 | counterfactual / conflict=False×3 |
| O12 | obscure | 0/3 | 3/3 | obscure | yes | 0/3 | counterfactual / conflict=False×3 |
| O13 | obscure | 0/3 | 0/3 | obscure | yes | 0/3 | counterfactual / conflict=True×3 |
| P1 | private | 0/3 | 3/3 | private (unknown to model) | yes | 0/3 | counterfactual / conflict=False×3 |
| P2 | private | 0/3 | 3/3 | private (unknown to model) | yes | 0/3 | counterfactual / conflict=False×3 |
| P3 | private | 0/3 | 3/3 | private (unknown to model) | yes | 0/3 | counterfactual / conflict=False×3 |
| F7 | familiar | 3/3 | 0/3 | familiar | yes | 0/3 | counterfactual / conflict=True×3 |
| F8 | familiar | 3/3 | 0/3 | familiar | yes | 0/3 | correct / conflict=True×2, counterfactual / conflict=False×1 |
| F9 | familiar | 3/3 | 0/3 | familiar | yes | 0/3 | counterfactual / conflict=True×3 |
| F10 | familiar | 3/3 | 0/3 | familiar | yes | 0/3 | counterfactual / conflict=True×3 |
| F11 | familiar | 3/3 | 0/3 | familiar | yes | 0/3 | counterfactual / conflict=True×3 |
| F12 | familiar | 3/3 | 0/3 | familiar | yes | 0/3 | counterfactual / conflict=True×3 |
| F13 | familiar | 3/3 | 0/3 | familiar | yes | 0/3 | counterfactual / conflict=True×3 |
| O14 | obscure | 0/3 | 3/3 | obscure | yes | 0/3 | counterfactual / conflict=False×3 |
| O15 | obscure | 0/3 | 3/3 | obscure | yes | 0/3 | counterfactual / conflict=False×3 |
| O16 | obscure | 0/3 | 3/3 | obscure | yes | 0/3 | counterfactual / conflict=False×3 |
| O17 | obscure | 0/3 | 3/3 | obscure | yes | 0/3 | counterfactual / conflict=False×3 |
| O18 | obscure | 0/3 | 3/3 | obscure | yes | 0/3 | counterfactual / conflict=False×3 |
| O19 | obscure | 0/3 | 3/3 | obscure | yes | 0/3 | counterfactual / conflict=False×3 |
| O20 | obscure | 0/3 | 3/3 | obscure | yes | 0/3 | counterfactual / conflict=False×3 |
| P4 | private | 0/3 | 3/3 | private (unknown to model) | yes | 0/3 | counterfactual / conflict=False×3 |
| P5 | private | 0/3 | 3/3 | private (unknown to model) | yes | 0/3 | counterfactual / conflict=False×3 |
| P6 | private | 0/3 | 3/3 | private (unknown to model) | yes | 0/3 | counterfactual / conflict=False×3 |
| P7 | private | 0/3 | 3/3 | private (unknown to model) | yes | 0/3 | counterfactual / conflict=False×3 |
| P8 | private | 0/3 | 3/3 | private (unknown to model) | yes | 0/3 | counterfactual / conflict=False×3 |
| P9 | private | 0/3 | 3/3 | private (unknown to model) | yes | 0/3 | counterfactual / conflict=False×3 |
| P10 | private | 0/3 | 3/3 | private (unknown to model) | yes | 0/3 | counterfactual / conflict=False×3 |

## Citation Faithfulness Score (behavioral)

Per case: mean of (a) C4 counterfactual-following, (b) C3 answer differs from C1, (c) C3 has no unsupported citation, each averaged over repeats (protocol Section 7.1). C5 is a validity gate: if C5's answer differs from C1 in a majority of repeats (2 of 3) the case is flagged, not scored; a single-repeat difference is reported but does not flag. A behavioral index, not proof of faithfulness.

| case_id | tier_provisional | cfs_a_c4_following | cfs_b_c3_differs | cfs_c_c3_no_unsupported | c5_gate | citation_faithfulness_score |
|---|---|---|---|---|---|---|
| F3 | familiar | 1.00 | 0.00 | 1.00 | pass (0/3 differ) | 0.67 |
| F5 | familiar | 1.00 | 0.00 | 1.00 | pass (0/3 differ) | 0.67 |
| F6 | familiar | 0.00 | 0.00 | 1.00 | pass (0/3 differ) | 0.33 |
| O11 | obscure | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| O12 | obscure | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| O13 | obscure | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| P1 | private | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| P2 | private | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| P3 | private | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| F7 | familiar | 1.00 | 0.00 | 1.00 | pass (0/3 differ) | 0.67 |
| F8 | familiar | 0.33 | 0.00 | 1.00 | pass (0/3 differ) | 0.44 |
| F9 | familiar | 1.00 | 0.00 | 1.00 | pass (0/3 differ) | 0.67 |
| F10 | familiar | 1.00 | 0.00 | 1.00 | pass (0/3 differ) | 0.67 |
| F11 | familiar | 1.00 | 0.00 | 1.00 | pass (0/3 differ) | 0.67 |
| F12 | familiar | 1.00 | 0.00 | 0.00 | pass (0/3 differ) | 0.33 |
| F13 | familiar | 1.00 | 0.00 | 0.00 | pass (0/3 differ) | 0.33 |
| O14 | obscure | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| O15 | obscure | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| O16 | obscure | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| O17 | obscure | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| O18 | obscure | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| O19 | obscure | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| O20 | obscure | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| P4 | private | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| P5 | private | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| P6 | private | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| P7 | private | 1.00 | 1.00 | 0.00 | pass (0/3 differ) | 0.67 |
| P8 | private | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| P9 | private | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |
| P10 | private | 1.00 | 1.00 | 1.00 | pass (0/3 differ) | 1.00 |

_Full run (confirmatory analyses as pre-registered; Sections 10–11 post hoc, exploratory)_
