# Manuscript figures

The main paper is now **scaphoid problem-first**. Figures are organized around the clinical question rather than the earlier multi-disease computational workflow.

## Current main-text sequence

### Figure 1 — Cohort derivation and operative analytic denominator

Current pre-gold vector figure:

- [`scaphoid/Figure1_cohort_flow_pre_gold.svg`](scaphoid/Figure1_cohort_flow_pre_gold.svg)

It shows:

`88 broad scaphoid candidates`

→ `68 high-specificity wrist scaphoid`

→ `23 established chronic/nonunion | 45 comparison`

→ `15 | 13 disease-concordant detailed operative records`.

All 28 current operative analytic records occur in 2023-2025.

### Figure 2 — Treatment composition by phenotype group

**Final figure waits for physician-adjudicated clinical labels.**

Planned panels:

- internal fixation by phenotype;
- bone-graft augmentation by phenotype;
- odds ratios with 95% confidence intervals.

Exact small-cell treatment counts are not published in an open figure before the privacy/physician-validation gate.

### Figure 3 — Validation of the clinical variables used in the paper

Only the measurements required for the scientific conclusion:

- wrist-scaphoid anatomy;
- chronic/nonunion state;
- target-disease procedure relevance;
- internal fixation;
- bone graft.

Generic multi-disease NLP benchmark panels are not required in the main article.

### Figure 4 — Robustness / influence

Optional main or supplementary figure:

- physician-adjudicated versus deterministic effect estimate;
- physician-confirmed acute-only sensitivity analysis;
- leave-one-out influence analysis;
- primary bone-graft outcome versus broader augmentation composite.

## Historical / supplementary graphics

The original workflow-heavy files remain for auditability and repository documentation:

- `pre_gold/Figure1_validation_first_framework.svg`;
- `pre_gold/Figure2_cohort_reconstruction.svg`;
- `pre_gold/Figure3_procedure_attribution.svg`.

These are **not current main-text figures**. They may be used in Supplementary Methods or repository documentation if useful.

## Visual style

- white background;
- black/dark-gray/light-gray data marks;
- no promotional title bands, decorative icons, shadows or gradients;
- concise panel letters;
- explicit denominators;
- effect estimates and confidence intervals when inferential results are displayed;
- vector output for journal export.

See `docs/JOURNAL_FIGURE_PLAN_V0_1.md` and `docs/MANUSCRIPT_PLAN_SCAPHOID_V0_1.md`.
