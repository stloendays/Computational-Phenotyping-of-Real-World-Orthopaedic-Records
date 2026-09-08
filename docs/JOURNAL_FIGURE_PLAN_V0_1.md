# Journal Figure Plan v0.1 — Scaphoid Problem-First Revision

## Main-text principle

Every main figure must answer the scaphoid scientific question directly. Project architecture, repository reproducibility, public/private boundaries and generic NLP benchmarking are not main-text figures.

## Figure 1 — Study population and operative analytic denominator

A compact flow diagram:

- 88 broad scaphoid candidates;
- 68 high-specificity wrist-scaphoid admissions;
- 23 established chronic/nonunion vs 45 comparison phenotypes;
- 18 vs 13 detailed-note module admissions;
- 15 vs 13 disease-concordant detailed operative records.

The figure should make clear that the final operative analysis contains 28 records and that all 28 occur in 2023-2025.

## Figure 2 — Treatment composition by phenotype group

Primary clinical figure.

Panel A: internal fixation proportion.  
Panel B: bone-graft augmentation proportion.  
Panel C: effect estimates after physician validation.

The visual message is the contrast:

- fixation remains common in both groups;
- graft augmentation differs.

Use simple bars/dots and a forest-plot effect estimate. No workflow boxes or decorative icons.

## Figure 3 — Validation of the variables used in the clinical analysis

Only show validation tasks required for the main conclusion:

- wrist-scaphoid anatomy;
- chronic/nonunion state;
- target-disease procedure relevance;
- internal fixation;
- bone graft.

Report physician-reference precision/recall/F1 or sensitivity/specificity as appropriate.

If deterministic rules perform adequately, do not force an LLM comparison into this figure.

## Figure 4 — Robustness and influence

Optional main or supplementary figure.

Potential panels:

- deterministic vs physician-adjudicated effect estimate;
- leave-one-out influence range for the bone-graft association;
- primary bone-graft outcome vs broader augmentation composite;
- exclusion of competing same-admission procedures.

## Supplementary figures

Move the following out of the main text:

- broad multi-disease framework diagram;
- public/private repository architecture;
- full 68/13/7 anatomy audit;
- procedure-attribution leakage schematic;
- full deterministic/LLM/hybrid benchmark across all diseases;
- hallux-valgus exploratory treatment patterns;
- first-CMC disambiguation audit.

## Visual style

- white background;
- black/gray data marks;
- no marketing-style title bands;
- panel letters A/B/C;
- effect sizes and confidence intervals preferred over decorative annotation;
- figure text limited to labels needed to read the data;
- explanation belongs in the legend.
