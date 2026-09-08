# Computational Phenotyping of Real-World Orthopaedic Records

This repository is a reproducible clinical-informatics workspace for reconstructing patient-level orthopaedic phenotypes from heterogeneous Chinese EHR exports and studying real-world disease and treatment patterns.

## Current phase

The project is in a **validation-first, fixed-data** phase. No additional local clinical data are assumed to become available. The first reproducible cohort audit and exploratory aggregate analysis are complete; the current locked milestone is physician validation of deterministic phenotypes before any LLM-assisted comparison.

## Study domains

| Domain | Candidate admissions | Deterministic strict phenotype | Primary role |
|---|---:|---:|---|
| Hallux valgus | 200 | 193 | Surgical-procedure phenotyping and treatment-pattern analysis |
| Scaphoid fracture | 88 | 72 wrist-scaphoid cases | Established chronic/nonunion phenotype comparison |
| First CMC osteoarthritis | 79 | 28 strict first-CMC cases | Anatomical/diagnostic disambiguation and cross-disease NLP validation |

The current scaphoid v0.2 definition identifies **23 established chronic/nonunion phenotypes and 49 other strict wrist-scaphoid episodes**. Case status is assigned only from diagnosis, complaint and physical-examination text; operative text is excluded from case definition to avoid circularity when treatment is analysed downstream.

## Primary scientific questions

1. Can heterogeneous Chinese orthopaedic EHR exports be converted into an auditable patient-level research dataset without pseudoreplication?
2. Can deterministic and LLM-assisted extraction systems recover clinically meaningful phenotypes from free text with physician-validated accuracy?
3. Within the fixed scaphoid records, how do established chronic/nonunion phenotypes differ from other wrist-scaphoid phenotypes in treatment complexity?
4. Can the same computational-phenotyping architecture generalize across deformity, trauma/nonunion and degenerative hand disease?

## Completed cohort audit

The audit demonstrates three important properties of the source data.

### Repeated diagnosis rows are not independent observations

The diagnosis/demographics exports contain approximately **10.85, 12.40 and 13.40 rows per admission** for hallux valgus, first-CMC candidates and scaphoid candidates, respectively. All analyses therefore reconstruct admission-level episodes before inference.

### Documentation architecture changes by calendar era

The supplied 2019-2022 exports retain complaint/examination records but lack operative-note, examination/imaging and laboratory modules for the hallux-valgus and scaphoid cohorts. The **2023-2025 era is therefore prespecified as the internally consistent sensitivity period** for scaphoid treatment comparisons.

### Broad keyword retrieval has different specificity across diseases

Hallux-valgus retrieval is highly specific under the current deterministic rules, whereas first-CMC retrieval is deliberately difficult: only 28 of 79 candidate episodes satisfy the strict first-CMC phenotype. Synovitis, generic wrist arthritis, rheumatoid/gout-related wrist disease and other competing terms occur among the non-strict candidates.

## First aggregate findings

These findings are exploratory until physician validation is complete.

- Among 114 strict hallux-valgus episodes with detailed operative notes, osteotomy occurs in 93.0%, K-wire/steel-wire fixation in 90.4%, soft-tissue procedure terms in 97.4%, resection terms in 76.3%, Chevron in 43.0% and fusion in 10.5%.
- The most common hallux procedure combination is `k_wire + osteotomy + resection + soft_tissue` (34.2%).
- A preoperative bilateral-disease mention is more frequent in Chevron-positive than Chevron-negative hallux operative episodes (69.4% vs 44.6%; exploratory OR 2.81, 95% CI 1.29-6.14, Fisher p=0.013).
- In the 2023-2025 scaphoid sensitivity cohort, age and BMI distributions are similar across phenotype groups; bone-grafting and broader complex-reconstruction markers are more frequent in the established chronic/nonunion group. Public inferential statistics are suppressed whenever exact small cells could be reconstructed.

These are treatment-pattern associations, not treatment recommendations or causal estimates of incident nonunion.

## Data release and privacy boundary

The supplied archive contains **18 hospital exports**: 12 `.xlsx` files covering demographics/diagnoses, complaints/examinations and surgery records, plus 6 legacy `.xls` workbooks containing examination/imaging reports and laboratory data.

Because the raw files contain direct identifiers and protected clinical text, **no raw, pseudonymized row-level or patient-level clinical data are committed to this public repository**. The `data/` directory contains only privacy-preserving aggregate artifacts, schema information and small-cell-suppressed summaries.

Public-release rules include:

- non-zero cells smaller than 5 are displayed as `<5`;
- inferential statistics are also suppressed when they could reveal a suppressed cell;
- rare multi-label procedure combinations are pooled;
- no patient-level dates, identifiers or free text are released.

## Key reproducible artifacts

### Protocol and definitions

- `docs/STUDY_PROTOCOL.md` - fixed-data research protocol;
- `docs/ANALYSIS_PLAN.md` - statistical/computational analysis plan;
- `configs/phenotypes_v0.2.yaml` - frozen cohort-audit phenotype definitions;
- `docs/PHENOTYPE_CHANGELOG.md` - versioned rationale for phenotype-rule changes;
- `docs/COHORT_AUDIT_V0_1.md` - first cohort audit;
- `results/INTERIM_FINDINGS_V0_1.md` - current aggregate findings.

### Data structure and aggregate results

- `data/schema/source_inventory.csv` - complete 18-file source inventory;
- `data/schema/field_map.csv` - canonical field map and release policy;
- `data/aggregate/cohort_overview.csv` - cohort size, demographics and data availability;
- `data/aggregate/source_duplication_audit.csv` - row-inflation audit;
- `data/aggregate/era_module_coverage.csv` - documentation coverage by era;
- `data/aggregate/scaphoid_comparative_table.csv` - exploratory scaphoid comparison;
- `data/aggregate/scaphoid_2023_2025_sensitivity.csv` - consistent-era sensitivity analysis;
- `data/aggregate/hallux_procedure_combinations.csv` - common hallux procedure combinations;
- `data/aggregate/hallux_treatment_pattern_contrasts.csv` - exploratory treatment-pattern contrasts;
- `data/aggregate/first_cmc_disambiguation_audit.csv` - first-CMC specificity audit.

### Code and tests

- `src/ortho_pheno/build_safe_release.py` - privacy-preserving cohort release builder;
- `src/ortho_pheno/analysis_v0_1.py` - aggregate cohort audit and exploratory analysis;
- `src/ortho_pheno/legacy_xls.py` - read-only legacy binary Excel parser;
- `src/ortho_pheno/rules.py` - dependency-light deterministic phenotype rules;
- `tests/test_phenotype_rules.py` - synthetic, non-PHI regression tests;
- `.github/workflows/ci.yml` - automated rule tests.

## Study design

The project combines:

- retrospective clinical informatics;
- patient-level record linkage and temporal normalization;
- clinical NLP / computational phenotyping;
- a scaphoid established-phenotype comparison with calendar-era sensitivity analysis;
- surgical procedure phenotyping in hallux valgus;
- cross-disease diagnostic disambiguation using first-CMC osteoarthritis;
- external public datasets for **methodological benchmarking or pretraining only**, never for pooling with local patients.

## Validation hierarchy

The analysis follows a locked sequence:

1. **deterministic rules and cohort audit** - complete for v0.2;
2. **physician gold-standard annotation** - current milestone;
3. regex/dictionary baseline evaluation on the frozen gold standard;
4. LLM-assisted structured extraction on the same frozen evaluation set;
5. hybrid extraction and prespecified error analysis;
6. manuscript-level claims only after validation and sensitivity checks.

This ordering prevents the gold standard from being tuned to model outputs.

## Repository principles

- One admission episode is the primary statistical unit unless explicitly stated otherwise.
- Every derived phenotype must be traceable to source fields/text and a versioned rule or model.
- Outcome/exposure definitions are frozen before confirmatory analysis.
- Missing text is not automatically interpreted as phenotype absence.
- Small-sample inference is prioritized over high-capacity predictive modelling.
- Public datasets develop or benchmark computational components; the fixed local dataset answers the clinical questions.
- Rule changes prompted by leakage, ambiguity or data-generation artifacts are documented before re-analysis.

## Repository structure

```text
configs/                 Frozen phenotype, cohort and annotation definitions
data/                    Privacy-preserving aggregate release and schemas
docs/                    Protocol, analysis plan, annotation protocol and governance
src/ortho_pheno/         Cohort construction, phenotype extraction and evaluation code
tests/                   Synthetic, non-PHI unit tests
results/                 Derived aggregate analysis outputs only
annotations/private/     Local-only physician annotation artifacts (gitignored)
```

## Current milestones

- [x] Inventory the complete 18-file source archive.
- [x] Reconstruct admission-level strict cohorts: 193 / 72 / 28.
- [x] Freeze v0.2 anatomy and scaphoid source-scope rules.
- [x] Complete cohort-audit v0.1 and calendar-era sensitivity analysis.
- [x] Add synthetic phenotype-rule tests and CI.
- [ ] Freeze physician annotation protocol and schema.
- [ ] Complete physician gold-standard adjudication using existing records only.
- [ ] Benchmark regex/dictionary extraction against the frozen gold standard.
- [ ] Evaluate LLM-assisted and hybrid extraction without changing the gold-standard labels.
- [ ] Generate manuscript figures/tables from versioned aggregate outputs.
