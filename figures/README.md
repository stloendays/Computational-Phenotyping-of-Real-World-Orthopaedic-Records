# Manuscript figures

This directory contains publication-oriented vector figures generated from versioned repository outputs.

## Pre-gold assets

The following main-text figures are supported entirely by source-architecture and deterministic audit evidence and therefore do not depend on physician reference-standard results:

1. [`pre_gold/Figure1_validation_first_framework.svg`](pre_gold/Figure1_validation_first_framework.svg) — validation-first computational phenotyping architecture and public/private data boundary.
2. [`pre_gold/Figure2_cohort_reconstruction.svg`](pre_gold/Figure2_cohort_reconstruction.svg) — raw-row inflation, candidate-to-strict reconstruction, scaphoid 68/13/7 anatomy audit, and the 72→68 rule transition.
3. [`pre_gold/Figure3_procedure_attribution.svg`](pre_gold/Figure3_procedure_attribution.svg) — procedure-attribution leakage, 114→113 / 31→28 / 18→18 relevance audit, and hierarchical evaluation design.

Corresponding manuscript wording is frozen in [`docs/FIGURE_CAPTIONS_V0_1.md`](../docs/FIGURE_CAPTIONS_V0_1.md).

Table 1 is available as both CSV and Markdown under `results/tables/`.

## Reproducibility

`src/ortho_pheno/build_manuscript_assets_v0_1.py` regenerates Figure 1–3 and Table 1 using only privacy-preserving aggregate CSVs already committed to the repository. The generator never reads raw EHR exports, patient-level rows, study IDs, free text, or physician gold labels.

`tests/test_manuscript_assets.py` regenerates the assets in a temporary directory during CI and checks the current frozen audit counts. A future data-version change must therefore be explicit rather than silently changing a manuscript graphic.

## Style

Current pre-gold figures use a grayscale vector style suitable for manuscript review and lossless SVG/PDF conversion. Final typography and panel sizing may be adapted to the target journal without changing the underlying data mapping.
