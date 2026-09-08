# Manuscript figures

This directory separates **journal main-text figures** from repository/supplementary schematics.

## Important reclassification

The first pre-gold graphics were intentionally useful for repository review and method communication, but they are **too workflow-heavy for the main Results figures of a journal article**.

Accordingly:

- `pre_gold/Figure1_validation_first_framework.svg` is now treated as a **Supplementary / repository overview schematic**, not the preferred main-text Figure 1;
- `pre_gold/Figure2_cohort_reconstruction.svg` contains reusable quantitative content, but the final main-text version should be reformatted according to `docs/JOURNAL_FIGURE_PLAN_V0_1.md`;
- `pre_gold/Figure3_procedure_attribution.svg` similarly remains an auditable prototype; the final main-text version should foreground quantitative attribution error rather than workflow boxes.

No data or audit result has been withdrawn. This is a **manuscript-design correction**, not a change in scientific evidence.

## Journal main-figure principle

A main figure must answer a scientific question using data, denominators, uncertainty or validated performance. Project-management concepts such as public/private zones, freeze governance and repository architecture belong in Methods, Supplementary Information or the README unless they are directly necessary to interpret a quantitative result.

The current preferred main-text hierarchy is:

1. **Study cohort derivation and analytical sample**;
2. **Data-quality distortions corrected during phenotyping**;
3. **Procedure-attribution error in operative records**;
4. **Physician-reference validation benchmark**;
5. **Hallux-valgus clinical/procedure phenotype**;
6. **Scaphoid phenotype and treatment pattern**.

See [`docs/JOURNAL_FIGURE_PLAN_V0_1.md`](../docs/JOURNAL_FIGURE_PLAN_V0_1.md) for panel-level specifications.

## Existing pre-gold assets

The current SVG files remain retained for auditability:

- [`pre_gold/Figure1_validation_first_framework.svg`](pre_gold/Figure1_validation_first_framework.svg);
- [`pre_gold/Figure2_cohort_reconstruction.svg`](pre_gold/Figure2_cohort_reconstruction.svg);
- [`pre_gold/Figure3_procedure_attribution.svg`](pre_gold/Figure3_procedure_attribution.svg).

They should not automatically be interpreted as final journal main figures.

## Reproducibility

`src/ortho_pheno/build_manuscript_assets_v0_1.py` regenerates the original pre-gold assets and Table 1 using only privacy-preserving aggregate CSVs committed to the repository. Those files remain versioned historical outputs.

A journal-oriented v0.2 figure generator will use the same aggregate evidence but reduce explanatory workflow content, remove in-figure promotional headings, and prioritize quantitative panels.

## Visual style for final journal figures

- white background;
- black/dark-grey/light-grey palette;
- no gradients, shadows or decorative icons;
- concise A-D panel labels;
- axes, denominators and confidence intervals where relevant;
- minimal explanatory text inside plotting regions;
- vector output for lossless journal export.
