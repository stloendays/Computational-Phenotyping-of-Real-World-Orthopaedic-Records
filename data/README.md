# Data release policy

This directory contains **privacy-preserving aggregate artifacts only**.

The source archive contains 18 hospital exports covering hallux valgus, first CMC osteoarthritis, and scaphoid-fracture candidate cohorts:

- demographics and diagnoses;
- complaint and specialist physical examination;
- surgery name / operating-note exports;
- examination/imaging reports;
- laboratory exports.

The raw files contain direct identifiers and protected clinical text. They are therefore **not stored in this public repository**.

## What is included

- `schema/source_inventory.csv`: source-file structure, sheet names, row counts, column counts, linkage-key coverage, and release status.
- `schema/field_map.csv`: canonical research fields and their privacy/release policy.
- `aggregate/cohort_overview.csv`: aggregate cohort size, demographics, text/surgery availability, examination coverage, and laboratory coverage.
- `aggregate/year_distribution.csv`: strict-cohort admissions by calendar year, with public small-cell suppression (`<5`).
- `aggregate/procedure_phenotype_counts.csv`: procedure phenotype frequencies among strict cases with detailed operating notes; cells below five are suppressed.
- `aggregate/scaphoid_anatomy_audit.csv`: complete v0.3 anatomy accounting of the 88 scaphoid-retrieval candidates.
- `aggregate/scaphoid_rule_version_transition.csv`: aggregate transition from the superseded heuristic to v0.3 anatomy classes.
- `aggregate/scaphoid_phenotype_groups.csv`: aggregate text-defined scaphoid chronic/nonunion phenotype groups within the high-specificity wrist cohort.
- `aggregate/annotation_workload_summary.csv`: aggregate size of the local-only physician reference-standard workload.

## Current deterministic cohort definitions

The current phenotype-v0.3 baseline recovers:

- hallux valgus: **193 / 200** candidate admissions;
- strict first-CMC osteoarthritis: **28 / 79** candidate admissions;
- high-specificity wrist-scaphoid phenotype: **68 / 88** candidate admissions.

The 88 scaphoid candidates are additionally partitioned into:

- **68 wrist-scaphoid**;
- **13 foot-navicular**;
- **7 ambiguous** records reserved for physician adjudication.

The earlier 72-case wrist-scaphoid count is superseded. Rule-transition auditing shows that all 68 current wrist-scaphoid episodes were retained from the earlier set and the four removed episodes are explicitly classified as foot-navicular under v0.3; no new wrist episodes were added to increase sample size.

These are versioned computational phenotype counts, not hand-entered sample sizes. They must be regenerated whenever phenotype rules change.

## Reproducibility

`src/ortho_pheno/build_safe_release.py` reads the local raw exports and writes aggregate artifacts only. `src/ortho_pheno/scaphoid_anatomy_audit.py` independently regenerates the 68/13/7 anatomy audit. The current inferential entrypoint is `src/ortho_pheno/analysis_v0_2.py`, which applies phenotype-v0.3 cohort logic while retaining the historical analysis implementation for auditability.

The legacy `.xls` reader is implemented in `src/ortho_pheno/legacy_xls.py` so the old examination/laboratory workbooks can be incorporated without converting the originals.

## Privacy boundary

The public repository must never contain:

- names;
- admission numbers / chart numbers;
- phone numbers;
- patient-level dates;
- raw complaint or examination text;
- raw operating notes;
- raw imaging reports;
- patient-level laboratory rows;
- pseudonymized row-level clinical data.

The code may be public; the raw and patient-level derived data remain local.
