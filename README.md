# Computational Phenotyping of Real-World Orthopaedic Records

This repository is the reproducible research workspace for reconstructing patient-level orthopaedic phenotypes from heterogeneous Chinese EHR exports and studying real-world disease and treatment patterns.

## Current phase

The project is in a **validation-first, fixed-data** phase. No additional local clinical data are assumed to become available. All confirmatory analyses must therefore be answerable from the existing structured fields, examination/laboratory exports and free-text records.

## Study domains

| Domain | Candidate admissions | Deterministic strict phenotype | Primary role |
|---|---:|---:|---|
| Hallux valgus | 200 | 193 | Surgical-procedure phenotyping and treatment-pattern analysis |
| Scaphoid fracture | 88 | 72 wrist-scaphoid cases | Embedded case-control / phenotype-comparison study |
| First CMC osteoarthritis | 79 | 28 strict first-CMC cases | Anatomical/diagnostic disambiguation and cross-disease NLP validation |

These counts are regenerated from the current rule-based cohort pipeline and must be rerun whenever phenotype definitions change.

## Primary scientific questions

1. Can heterogeneous Chinese orthopaedic EHR exports be converted into an auditable patient-level research dataset without pseudoreplication?
2. Can rule-based, terminology-based and LLM-assisted methods recover clinically meaningful phenotypes from free text with physician-validated accuracy?
3. Within the available scaphoid records, how do established nonunion/chronic phenotypes differ from other wrist-scaphoid fracture phenotypes in presentation and treatment complexity?
4. Can the same computational-phenotyping architecture generalize across deformity, trauma/nonunion and degenerative hand disease?

## Data release

The supplied archive contains **18 hospital exports**: 12 `.xlsx` files covering demographics/diagnoses, complaints/examinations and surgery records, plus 6 legacy `.xls` workbooks containing examination/imaging reports and laboratory data.

Because the raw files contain direct identifiers and protected clinical text, **no raw or patient-level clinical data are committed to this public repository**. The `data/` directory contains only privacy-preserving aggregate artifacts, schema information and small-cell-suppressed summaries.

Key files:

- `data/README.md` - data-release and privacy boundary;
- `data/schema/source_inventory.csv` - complete 18-file source inventory;
- `data/schema/field_map.csv` - canonical field map and release policy;
- `data/aggregate/cohort_overview.csv` - cohort size, demographics and data-availability summary;
- `data/aggregate/year_distribution.csv` - small-cell-suppressed annual distribution;
- `data/aggregate/procedure_phenotype_counts.csv` - aggregate surgical phenotype frequencies;
- `data/aggregate/scaphoid_phenotype_groups.csv` - aggregate chronic/nonunion phenotype groups;
- `docs/DATA_RELEASE_NOTES.md` - release notes and interpretation boundaries.

The aggregate release can be regenerated locally with `src/ortho_pheno/build_safe_release.py`; `src/ortho_pheno/legacy_xls.py` provides read-only access to the six legacy binary Excel files without modifying the originals.

## Study design

The project combines:

- retrospective clinical informatics;
- patient-level record linkage and temporal normalization;
- clinical NLP / computational phenotyping;
- an embedded scaphoid case-control or phenotype-comparison analysis, depending on the evidence contained in the existing records;
- surgical procedure phenotyping in hallux valgus;
- cross-disease diagnostic disambiguation using first-CMC osteoarthritis;
- external public datasets for **methodological benchmarking or pretraining only**, not for pooling with local patients.

## Validation philosophy

A publishable computational-phenotyping result should demonstrate more than model fit. Primary claims should survive tests of:

- phenotype-definition reproducibility;
- patient-level deduplication and leakage checks;
- cohort and coding perturbations;
- missing-data and documentation-process sensitivity;
- physician-validated NLP performance;
- subgroup and distribution-shift checks where sample size permits;
- reproducibility from frozen inputs and configurations.

## Repository principles

- **No raw patient data, pseudonymized row-level data or direct identifiers are committed to GitHub.**
- One admission/patient episode is the statistical unit unless explicitly stated otherwise.
- Every derived phenotype must be traceable to source fields/text and a versioned rule or model.
- Outcome/exposure definitions are frozen before confirmatory analysis.
- Small-sample inference is prioritized over high-capacity predictive modelling.
- Public datasets develop or benchmark computational components; local data answer the clinical questions.

## Analysis hierarchy

### 1. Scaphoid fracture: primary clinical analysis

The current-data design compares **established nonunion/chronic scaphoid phenotypes** with other wrist-scaphoid fracture phenotypes. Unless the existing records themselves document longitudinal conversion from acute fracture to later nonunion, this comparison will not be interpreted as a causal risk-factor study of incident nonunion.

### 2. Hallux valgus: surgical procedure phenotype

Free-text operative records are converted into multi-label procedure variables such as osteotomy, Chevron, fusion, K-wire fixation and soft-tissue procedures. The analysis focuses on real-world surgical-pattern heterogeneity rather than postoperative recurrence because long-term outcomes are not assumed to be available.

### 3. First CMC osteoarthritis: difficult diagnostic phenotype

This domain evaluates anatomical and diagnostic specificity because broad terms such as wrist arthritis can retrieve multiple non-CMC conditions. It serves as a stringent test of cohort specificity and cross-disease generalization.

## Repository structure

```text
configs/                 Frozen phenotype and cohort definitions
data/                    Privacy-preserving aggregate release and schemas
docs/                    Protocol, statistical analysis plan and data governance
src/ortho_pheno/         Cohort construction and phenotype extraction code
tests/                   Synthetic, non-PHI unit tests
results/                 Derived aggregate analysis outputs only
```

## Immediate milestones

1. Freeze cohort and phenotype definitions against the current 18-file archive.
2. Add synthetic unit tests for anatomical/diagnostic disambiguation.
3. Validate the deterministic phenotype rules against physician review.
4. Build the first scaphoid phenotype-comparison table.
5. Quantify hallux-valgus procedure-pattern heterogeneity.
6. Add LLM/NLP benchmarking only after deterministic baselines are frozen.
