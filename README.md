# Computational Phenotyping of Real-World Orthopaedic Records

This repository is the reproducible research workspace for developing and validating computational phenotypes derived from real-world orthopaedic records.

## Current phase

The project is entering a **validation-first** phase. The repository is structured so that validation criteria are specified before inspecting validation outcomes, reducing post-hoc tuning and making the evidence chain auditable.

## Validation philosophy

A publishable computational-phenotyping result should demonstrate more than model fit. The primary claims should survive tests of:

- phenotype definition reproducibility;
- cohort and coding perturbations;
- temporal and patient-level separation;
- missing-data and documentation-process sensitivity;
- internal resampling and held-out validation;
- subgroup and distribution-shift checks;
- calibration and decision-level utility where prediction is involved;
- negative controls and leakage checks;
- reproducibility from frozen inputs and configurations.

The detailed preregistered validation matrix is developed on the `validation-v0.1` branch.
