# Computational Phenotyping of Real-World Orthopaedic Records

A reproducible clinical-informatics study for reconstructing admission-level orthopaedic phenotypes from heterogeneous Chinese EHR exports and analysing real-world disease and treatment patterns.

## Current status

The project is in a **validation-first, fixed-data** phase. No additional local clinical data are assumed to become available.

Completed:

- full 18-file source inventory;
- admission-level reconstruction and deduplication;
- phenotype rule audit through **v0.3**;
- cohort audit v0.2;
- calendar-era sensitivity analysis;
- exploratory scaphoid and hallux treatment-pattern analyses;
- synthetic regression tests and CI;
- local-only physician annotation packet generator and annotation schema.

Current locked milestone: **physician reference-standard annotation before any LLM-assisted extraction comparison**.

## Current deterministic cohorts

| Domain | Candidate admissions | Current deterministic phenotype | Primary role |
|---|---:|---:|---|
| Hallux valgus | 200 | **193** | Procedure phenotyping and treatment-pattern analysis |
| Scaphoid retrieval | 88 | **68 wrist scaphoid** | Established chronic/nonunion phenotype comparison |
| First CMC OA | 79 | **28** | Anatomical/diagnostic disambiguation benchmark |

### Scaphoid anatomy v0.3

The 88 scaphoid candidates are explicitly separated into:

- **68 wrist-scaphoid episodes (77.3%)**;
- **13 explicit foot-navicular episodes (14.8%)**;
- **7 ambiguous episodes (8.0%)** reserved for physician adjudication.

The earlier 72-case wrist-scaphoid count is **superseded**. Audit of discordant cases showed that the previous rule could treat non-anatomical Chinese words such as `手术` (operation) or `手法` (manual manoeuvre) as "hand" context. v0.3 replaces this shortcut with source-aware local anatomical evidence and an explicit ambiguous state.

Within the 68 high-specificity wrist-scaphoid episodes:

- **23** have an established chronic/nonunion phenotype from diagnosis/complaint/examination text;
- **45** form the other wrist-scaphoid comparison group.

Operative text is not allowed to assign chronic/nonunion case status because operative treatment is analysed downstream.

## Why cohort reconstruction matters

The demographics/diagnosis exports contain repeated rows for the same admission. Raw-row inflation is approximately:

- hallux valgus: **10.85 rows/admission**;
- first-CMC candidate retrieval: **12.40 rows/admission**;
- scaphoid candidate retrieval: **13.40 rows/admission**.

Row-level inference would therefore create severe pseudoreplication. All analyses use reconstructed admission episodes.

## Documentation-era shift

The supplied 2019-2022 exports retain complaint/examination records but lack detailed operative-note, examination/imaging and laboratory modules for the hallux-valgus and scaphoid cohorts. The **2023-2025 era is prespecified as the internally consistent sensitivity period** for scaphoid treatment comparisons.

For the v0.3 strict scaphoid cohort:

- 2015-2018: 15 episodes;
- 2019-2022: 21 episodes;
- 2023-2025: 32 episodes.

This prevents documentation-system changes from being misinterpreted as clinical effects.

## Current exploratory findings

These findings remain provisional until physician validation of the relevant text phenotypes.

### Hallux valgus

Among 114 detailed operative notes:

- osteotomy: **93.0%**;
- K-wire/steel-wire fixation: **90.4%**;
- soft-tissue procedure terms: **97.4%**;
- resection terms: **76.3%**;
- Chevron: **43.0%**;
- fusion: **10.5%**.

The most common multi-label combination is `k_wire + osteotomy + resection + soft_tissue` (34.2%).

A preoperative bilateral-disease mention is more frequent in Chevron-positive than Chevron-negative episodes (69.4% vs 44.6%; exploratory OR 2.81, 95% CI 1.29-6.14, Fisher p=0.013). This is hypothesis-generating, not a causal treatment-selection claim.

### Scaphoid

In the 2023-2025 sensitivity cohort there are 18 established chronic/nonunion and 14 comparison episodes. Age and BMI distributions are similar. Among detailed operative notes, bone-grafting and broader complex-reconstruction markers remain more frequent in the established chronic/nonunion group; public inferential statistics are suppressed whenever a small cell could be reverse-engineered.

This is a treatment-pattern comparison of an established phenotype, **not prediction of incident nonunion**.

### First-CMC OA

Only 28 of 79 broad candidates satisfy the strict first-CMC phenotype. Synovitis, generic wrist arthritis, rheumatoid/gout-related wrist disease and other competing terms occur among non-strict candidates, making this domain a useful hard-negative test for clinical NLP specificity.

## Physician reference standard

The current annotation plan uses only the existing records:

- disease/anatomy adjudication: **367 candidate episodes**;
- scaphoid-state adjudication: **68 strict wrist-scaphoid episodes**;
- procedure adjudication: **163 detailed operative notes**;
- approximately 20% deterministic stratified second review for inter-rater reliability.

Private annotation packets, pseudonymous study IDs and clinical text remain in `annotations/private/` and are never committed.

## Key files

### Protocol and audit

- `docs/STUDY_PROTOCOL.md` - formal fixed-data study protocol;
- `docs/ANALYSIS_PLAN.md` - statistical/computational analysis plan;
- `docs/COHORT_AUDIT_V0_2.md` - current cohort audit;
- `docs/PHENOTYPE_CHANGELOG.md` - rule-version audit trail;
- `docs/ANNOTATION_PROTOCOL_V0_1.md` - physician reference-standard protocol;
- `configs/phenotypes_v0.3.yaml` - current deterministic phenotype definitions;
- `configs/annotation_schema_v0.1.yaml` - annotation label schema;
- `results/INTERIM_FINDINGS_V0_2.md` - current aggregate findings.

### Aggregate data

- `data/aggregate/cohort_overview.csv`;
- `data/aggregate/scaphoid_anatomy_audit.csv`;
- `data/aggregate/source_duplication_audit.csv`;
- `data/aggregate/era_module_coverage.csv`;
- `data/aggregate/scaphoid_comparative_table.csv`;
- `data/aggregate/scaphoid_2023_2025_sensitivity.csv`;
- `data/aggregate/hallux_procedure_combinations.csv`;
- `data/aggregate/hallux_treatment_pattern_contrasts.csv`;
- `data/aggregate/first_cmc_disambiguation_audit.csv`;
- `data/aggregate/annotation_workload_summary.csv`.

### Code and tests

- `src/ortho_pheno/build_safe_release.py` - privacy-preserving aggregate builder;
- `src/ortho_pheno/analysis_v0_1.py` - aggregate cohort analysis;
- `src/ortho_pheno/rules.py` - deterministic phenotype rules;
- `src/ortho_pheno/legacy_xls.py` - legacy binary Excel parser;
- `src/ortho_pheno/make_annotation_packet.py` - local-only annotation packet generator;
- `tests/test_phenotype_rules.py` - synthetic non-PHI regression tests;
- `.github/workflows/ci.yml` - automated tests.

## Privacy boundary

The original archive contains direct identifiers and protected clinical text. **No raw patient data, pseudonymized row-level data, admission identifiers, dates or free-text clinical notes are committed to this public repository.**

Public outputs follow these rules:

- non-zero cells smaller than 5 are shown as `<5`;
- OR/CI/P values are also suppressed if they could reveal a small cell;
- rare procedure combinations are pooled;
- only aggregate or schema-level artifacts are released.

## Validation hierarchy

1. deterministic cohort construction and anatomy audit - **complete through v0.3**;
2. physician gold-standard annotation - **current milestone**;
3. regex/dictionary baseline evaluation on the frozen reference standard;
4. LLM-assisted structured extraction on the same locked labels;
5. hybrid extraction and prespecified error analysis;
6. manuscript claims and figures generated only from versioned outputs.

The study is intentionally designed so that the gold standard is not tuned to model behaviour.
