# Data release policy

This directory contains **privacy-preserving aggregate artifacts only**.

The fixed source archive contains 18 hospital exports covering hallux valgus, first CMC osteoarthritis, and scaphoid-fracture candidate cohorts:

- demographics and diagnoses;
- complaint and specialist physical examination;
- surgery name / detailed operative-note exports;
- examination/imaging reports;
- laboratory exports.

The raw files contain direct identifiers and protected clinical text and are therefore **not stored in this public repository**.

## What is included

### Source/schema artifacts

- `schema/source_inventory.csv` - source-file structure, sheets, row/column counts and linkage-key coverage;
- `schema/field_map.csv` - canonical research fields and release policy.

### Cohort/anatomy artifacts

- `aggregate/cohort_overview.csv` - current strict-cohort sizes and aggregate data availability;
- `aggregate/year_distribution.csv` - year distribution with public small-cell suppression;
- `aggregate/scaphoid_anatomy_audit.csv` - v0.3 partition of 88 scaphoid candidates into wrist/foot/ambiguous;
- `aggregate/scaphoid_rule_version_transition.csv` - transition from the superseded 72-case heuristic to v0.3;
- `aggregate/scaphoid_phenotype_groups.csv` - 23 established chronic/nonunion vs 45 other wrist-scaphoid episodes;
- `aggregate/source_duplication_audit.csv` and `aggregate/era_module_coverage.csv` - pseudoreplication and documentation-era audits.

### Procedure-context artifacts

Two families are intentionally retained.

**Historical/full-note keyword baselines** show what happens if all detailed operative-note text is searched without target-disease attribution. These files are retained for auditability.

**Current disease-concordant outputs** require the detailed note to be attributable to the target disease/anatomical site before procedure components contribute to clinical prevalence or treatment-pattern analysis:

- `aggregate/procedure_note_relevance_audit.csv`;
- `aggregate/procedure_phenotype_counts_concordant.csv`;
- `aggregate/hallux_procedure_combinations_concordant.csv`;
- `aggregate/hallux_treatment_pattern_contrasts_concordant.csv`;
- `aggregate/scaphoid_procedure_by_group_concordant.csv`.

Current module-available vs disease-concordant procedure admissions are:

| Domain | Detailed-note module | Disease-concordant |
|---|---:|---:|
| Hallux valgus | 114 | **113** |
| Wrist scaphoid | 31 | **28** |
| First-CMC OA | 18 | **18** |

The module count remains a documentation-availability metric. The disease-concordant count is the current pre-validation denominator for target-disease procedure prevalence.

### Validation workload

- `aggregate/annotation_workload_summary.csv` - public aggregate workload for the local-only physician reference standard.

The procedure annotation workload deliberately uses all **163 module-available admissions**, including unrelated operations, because these are clinically meaningful hard negatives for procedure-attribution evaluation.

## Current deterministic cohort definitions

Phenotype v0.3 recovers:

- hallux valgus: **193 / 200** candidate admissions;
- strict first-CMC osteoarthritis: **28 / 79** candidate admissions;
- high-specificity wrist-scaphoid phenotype: **68 / 88** candidate admissions.

The 88 scaphoid candidates are partitioned into:

- **68 wrist-scaphoid**;
- **13 foot-navicular**;
- **7 ambiguous** records reserved for physician adjudication.

The earlier 72-case wrist-scaphoid count is superseded. All 68 current wrist-scaphoid episodes were retained from the earlier set, while the four removed episodes are explicitly foot-navicular under v0.3. No new wrist episodes were added to increase sample size.

## Reproducibility

- `src/ortho_pheno/build_safe_release.py` - privacy-preserving source/cohort aggregate builder;
- `src/ortho_pheno/scaphoid_anatomy_audit.py` - independent 68/13/7 anatomy audit;
- `src/ortho_pheno/analysis_v0_2.py` - current phenotype-v0.3 aggregate-analysis entrypoint;
- `src/ortho_pheno/procedure_rules.py` - canonical anatomy-aware procedure taxonomy and relevance rules;
- `src/ortho_pheno/procedure_context_audit.py` - regenerates disease-concordant procedure summaries;
- `src/ortho_pheno/legacy_xls.py` - read-only access to legacy binary Excel files.

## Privacy boundary

The public repository must never contain:

- names;
- admission numbers / chart numbers;
- phone numbers;
- patient-level dates;
- raw complaint or examination text;
- raw operation names or operative notes;
- raw imaging reports;
- patient-level laboratory rows;
- pseudonymized row-level clinical data;
- physician annotation rows or pseudonymous study IDs.

Public non-zero cells below five are suppressed as `<5`; inferential statistics are also suppressed when they could reveal a small cell. The code may be public; raw and row-level derived clinical data remain local.
