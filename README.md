# Computational Phenotyping of Real-World Orthopaedic Records

A reproducible clinical-informatics study for reconstructing admission-level orthopaedic phenotypes from heterogeneous Chinese EHR exports and analysing real-world disease and treatment patterns.

## Current status

The project is in a **validation-first, fixed-data** phase. No additional local clinical data are assumed to become available.

Completed:

- full 18-file source inventory;
- admission-level reconstruction and deduplication;
- phenotype rule audit through **v0.3**;
- scaphoid anatomy and rule-transition audits;
- calendar-era sensitivity analysis;
- **procedure-context audit separating note availability from target-disease procedure attribution**;
- anatomy-aware hallux/scaphoid/first-CMC procedure summaries;
- synthetic leakage/regression tests and CI;
- local-only physician annotation packet generator;
- blinded deterministic baseline-prediction generator that never reads `gold_*` columns.

Current locked milestone: **physician reference-standard annotation before any LLM-assisted extraction comparison**.

## Current deterministic cohorts

| Domain | Candidate admissions | Current deterministic phenotype | Primary role |
|---|---:|---:|---|
| Hallux valgus | 200 | **193** | Procedure phenotyping and treatment-pattern analysis |
| Scaphoid retrieval | 88 | **68 wrist scaphoid** | Established chronic/nonunion phenotype comparison |
| First CMC OA | 79 | **28** | Anatomical/diagnostic disambiguation benchmark |

### Scaphoid anatomy v0.3

The 88 scaphoid candidates are separated into:

- **68 wrist-scaphoid episodes (77.3%)**;
- **13 explicit foot-navicular episodes (14.8%)**;
- **7 ambiguous episodes (8.0%)** reserved for physician adjudication.

The earlier 72-case wrist-scaphoid count is superseded. Audit of discordant cases showed that a previous character-level heuristic could treat non-anatomical words such as `手术` or `手法` as hand context. The rule-transition audit shows that 68/72 previous selections remain wrist scaphoid, the four removed episodes are explicit foot-navicular records, and **no new wrist cases were added to increase sample size**.

Within the 68 high-specificity wrist-scaphoid episodes:

- **23** have an established chronic/nonunion phenotype from diagnosis/complaint/examination text;
- **45** form the other wrist-scaphoid comparison group.

Operative text is prohibited from assigning chronic/nonunion case status because operative treatment is analysed downstream.

## Why cohort reconstruction matters

The demographics/diagnosis exports contain repeated rows for the same admission. Raw-row inflation is approximately:

- hallux valgus: **10.85 rows/admission**;
- first-CMC candidate retrieval: **12.40 rows/admission**;
- scaphoid candidate retrieval: **13.40 rows/admission**.

All inferential analyses therefore use reconstructed admission episodes rather than raw rows.

## Documentation-era shift

The supplied 2019-2022 exports retain complaint/examination records but lack detailed operative-note, examination/imaging and laboratory modules for hallux-valgus and scaphoid cohorts. The **2023-2025 era is prespecified as the internally consistent sensitivity period** for scaphoid treatment comparisons.

For the v0.3 strict scaphoid cohort:

- 2015-2018: 15 episodes;
- 2019-2022: 21 episodes;
- 2023-2025: 32 episodes.

## Procedure attribution: a second EHR leakage problem

A detailed operative-note module does not guarantee that the documented operation treated the target study disease. The same admission can contain an operation for a different anatomical problem, and generic terms such as `切除`, `软组织`, `内固定` or `钢针` can otherwise be falsely attributed to the target disease.

Current audit:

| Domain | Detailed-note module admissions | Disease-concordant procedure-note admissions |
|---|---:|---:|
| Hallux valgus | 114 | **113** |
| Wrist scaphoid | 31 | **28** |
| First-CMC OA | 18 | **18** |

Module availability remains a data-quality variable. Clinical procedure prevalence uses disease-concordant notes. **All module-available notes remain in physician/model validation as hard negatives**, so relevance attribution itself is evaluated rather than hidden preprocessing.

## Current exploratory findings

These findings remain provisional until physician validation.

### Hallux valgus

Among **113 disease-concordant operative admissions**:

- osteotomy: **106/113 (93.8%)**;
- K-wire/steel-wire fixation: **103/113 (91.2%)**;
- soft-tissue procedure terms: **111/113 (98.2%)**;
- resection: **86/113 (76.1%)**;
- Chevron: **49/113 (43.4%)**;
- fusion: **12/113 (10.6%)**.

The most common multi-label combination is `k_wire + osteotomy + resection + soft_tissue` (**39/113, 34.5%**).

A preoperative bilateral-disease mention is more frequent in Chevron-positive than Chevron-negative disease-concordant episodes (**69.4% vs 45.3%; exploratory OR 2.74, 95% CI 1.25-5.98, Fisher p=0.013**). This is hypothesis-generating, not a causal treatment-selection claim.

### Scaphoid

The phenotype groups remain 23 established chronic/nonunion versus 45 other wrist-scaphoid episodes. Detailed-note **module availability** is 18/23 versus 13/45, but target-disease procedure-note availability is **15/23 versus 13/45** after excluding detailed notes that document only other anatomical operations.

Among disease-concordant operative records:

- internal fixation: **14/15 vs 12/13**;
- bone grafting: **8/15 vs `<5/13`**;
- graft/reconstruction/fusion composite: **9/15 vs `<5/13`**.

Small-cell inferential statistics are suppressed in the public release. This remains a treatment-pattern comparison of established phenotypes, **not prediction of incident nonunion**.

### First-CMC OA

Only 28 of 79 broad candidates satisfy the strict first-CMC phenotype. All **18/18** strict first-CMC admissions with a detailed-note module are currently disease-concordant under the deterministic procedure-context rules. The domain remains a hard-negative benchmark for diagnostic/anatomical specificity rather than a high-capacity prediction cohort.

## Physician reference standard

The current annotation plan uses only existing records:

- disease/anatomy adjudication: **367 candidate episodes**;
- scaphoid-state adjudication: **68 wrist-scaphoid episodes**;
- procedure adjudication: **163 module-available detailed-operative-note admissions**;
- approximately 20% deterministic stratified second review for inter-rater reliability.

Procedure review is hierarchical:

1. `target_disease_procedure_present = yes / no / uncertain`;
2. multi-label procedure components when attributable to the target disease.

The local procedure annotation packet has been regenerated with this relevance label. Private annotation rows, study IDs and clinical text remain under `annotations/private/` and are never committed.

## Blinded deterministic baseline

`src/ortho_pheno/generate_rule_predictions.py` can generate local deterministic predictions from the private annotation packet before gold labels are scored. The loader explicitly removes every column whose name starts with `gold_`, providing a code-level guard against accidental label leakage.

The same locked reference standard will later score:

1. deterministic rules;
2. terminology/dictionary baselines;
3. LLM-assisted structured extraction;
4. hybrid extraction.

## Key files

### Protocol and audit

- `docs/STUDY_PROTOCOL.md` - fixed-data study protocol;
- `docs/ANALYSIS_PLAN.md` - current statistical/computational analysis plan;
- `docs/COHORT_AUDIT_V0_2.md` - current cohort audit;
- `docs/PROCEDURE_CONTEXT_AUDIT_V0_1.md` - cross-anatomy procedure-attribution audit;
- `docs/PHENOTYPE_CHANGELOG.md` - phenotype-rule audit trail;
- `docs/ANNOTATION_PROTOCOL_V0_2.md` - current physician reference-standard protocol;
- `configs/phenotypes_v0.3.yaml` - current deterministic phenotype definitions;
- `configs/annotation_schema_v0.1.yaml` - current annotation schema;
- `results/INTERIM_FINDINGS_V0_3.md` - current aggregate findings.

### Aggregate data

- `data/aggregate/cohort_overview.csv`;
- `data/aggregate/scaphoid_anatomy_audit.csv`;
- `data/aggregate/scaphoid_rule_version_transition.csv`;
- `data/aggregate/procedure_note_relevance_audit.csv`;
- `data/aggregate/procedure_phenotype_counts_concordant.csv`;
- `data/aggregate/scaphoid_procedure_by_group_concordant.csv`;
- `data/aggregate/hallux_procedure_combinations_concordant.csv`;
- `data/aggregate/hallux_treatment_pattern_contrasts_concordant.csv`;
- `data/aggregate/source_duplication_audit.csv`;
- `data/aggregate/era_module_coverage.csv`;
- `data/aggregate/first_cmc_disambiguation_audit.csv`;
- `data/aggregate/annotation_workload_summary.csv`.

Historical naive/full-note summaries are retained for auditability and are not silently overwritten.

### Code and tests

- `src/ortho_pheno/build_safe_release.py` - privacy-preserving aggregate builder;
- `src/ortho_pheno/analysis_v0_2.py` - current phenotype-v0.3 aggregate-analysis entrypoint;
- `src/ortho_pheno/scaphoid_anatomy_audit.py` - independent 68/13/7 anatomy audit;
- `src/ortho_pheno/procedure_rules.py` - canonical anatomy-aware procedure taxonomy;
- `src/ortho_pheno/procedure_context_audit.py` - disease-concordant procedure audit;
- `src/ortho_pheno/make_annotation_packet.py` - local-only physician packet generator;
- `src/ortho_pheno/generate_rule_predictions.py` - blinded deterministic baseline generator;
- `src/ortho_pheno/evaluate_annotations.py` - aggregate validation metrics;
- `src/ortho_pheno/rules.py` - deterministic disease/anatomy rules;
- `tests/` - synthetic non-PHI regression/leakage tests;
- `.github/workflows/ci.yml` - automated tests.

## Privacy boundary

The original archive contains direct identifiers and protected clinical text. **No raw patient data, pseudonymized row-level data, admission identifiers, dates or free-text clinical notes are committed to this public repository.**

Public outputs follow these rules:

- non-zero cells smaller than 5 are shown as `<5`;
- OR/CI/P values are suppressed if they could reveal a small cell;
- rare procedure combinations are pooled;
- only aggregate or schema-level artifacts are released.

## Validation hierarchy

1. admission-level reconstruction and phenotype-v0.3 anatomy audit - **complete**;
2. procedure-context/leakage audit - **complete**;
3. private physician annotation packet and blinded baseline infrastructure - **complete**;
4. physician gold-standard annotation and adjudication - **current locked milestone**;
5. deterministic baseline scoring on the frozen reference standard;
6. LLM-assisted extraction on the identical locked labels;
7. hybrid extraction, error taxonomy and manuscript figures.

The study is intentionally structured so that neither rules nor LLMs can redefine the reference standard after seeing their own errors.
