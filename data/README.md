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
- `aggregate/scaphoid_phenotype_groups.csv`: aggregate text-defined scaphoid chronic/nonunion phenotype groups.

## Current deterministic cohort definitions

The current rule-based baseline recovers:

- hallux valgus: **193 / 200** candidate admissions;
- strict first-CMC osteoarthritis: **28 / 79** candidate admissions;
- wrist-scaphoid phenotype: **72 / 88** candidate admissions.

These are versioned computational phenotype counts, not hand-entered sample sizes. They should be regenerated whenever phenotype rules change.

## Reproducibility

`src/ortho_pheno/build_safe_release.py` reads the local raw exports and writes aggregate artifacts only. The legacy `.xls` reader is implemented in `src/ortho_pheno/legacy_xls.py` so the old examination/laboratory workbooks can be incorporated without converting the originals.

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
