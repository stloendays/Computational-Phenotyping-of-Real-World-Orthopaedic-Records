# Cohort audit v0.1

This audit is generated from the fixed local dataset. No patient-level data, direct identifiers or free text are written to the public outputs.

## Frozen strict cohorts

- `hallux_valgus`: 193 strict admission episodes from 200 candidate admission episodes.
- `first_cmc_oa`: 28 strict admission episodes from 79 candidate admission episodes.
- `scaphoid_fracture`: 72 strict admission episodes from 88 candidate admission episodes.

## Key design cautions

- Repeated diagnosis rows are not independent observations; the analysis unit is the admission episode.
- The scaphoid chronic/nonunion group is an established text-supported phenotype and is not assumed to represent incident nonunion observed from an acute baseline.
- Documentation availability varies by calendar era and module; temporal analyses must account for this data-generation shift.
- Procedure labels are multi-label text phenotypes and require physician validation before confirmatory clinical interpretation.

## Generated aggregate analyses

- `source_duplication_audit.csv`: raw-row inflation by source module.
- `era_module_coverage.csv`: documentation coverage by era.
- `scaphoid_comparative_table.csv`: exploratory chronic/nonunion vs other wrist-scaphoid comparison.
- `scaphoid_era_distribution.csv`: documentation-era distribution by scaphoid phenotype group.
- `scaphoid_2023_2025_sensitivity.csv`: treatment comparison restricted to the internally consistent 2023-2025 era.
- `scaphoid_procedure_by_group.csv`: procedure phenotype distribution by scaphoid group.
- `hallux_procedure_combinations.csv`: common multi-label hallux procedure combinations.
- `hallux_procedure_cooccurrence.csv`: pairwise procedure co-occurrence.
- `hallux_treatment_pattern_contrasts.csv`: exploratory Chevron/fusion treatment-pattern contrasts.
- `first_cmc_disambiguation_audit.csv`: diagnostic ambiguity audit for first-CMC OA.
