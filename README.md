# Real-World Scaphoid Treatment Composition Study

This repository supports a **problem-first retrospective study** of wrist-scaphoid presentations in a fixed hospital EHR dataset.

## Primary scientific question

> **Among wrist-scaphoid admissions with disease-concordant detailed operative documentation, is established chronic/nonunion disease associated with greater use of bone-graft augmentation while internal fixation remains common in both phenotype groups?**

Computational text processing is used only to recover and validate the clinical variables required to answer this question. It is **not** the scientific objective of the paper.

## Why this question was selected

The current deterministic pre-validation analysis shows a specific treatment-composition pattern:

| Operative component | Established chronic/nonunion | Comparison phenotype |
|---|---:|---:|
| Internal fixation | 14/15 (93.3%) | 12/13 (92.3%) |
| Bone graft | 8/15 (53.3%) | `<5/13` |
| Graft/reconstruction/fusion augmentation | 9/15 (60.0%) | `<5/13` |

The scientific hypothesis is therefore narrower than “chronic cases receive more complex surgery.” The proposed signal is that **the base fixation construct remains common while biological/reconstructive augmentation increases**.

These values are algorithm-derived and provisional until physician adjudication.

## Study population

The supplied broad scaphoid retrieval contains 88 candidate admission episodes. Phenotype v0.3 currently partitions them into:

- **68 high-specificity wrist-scaphoid** admissions;
- **13 explicit foot-navicular** admissions;
- **7 anatomically ambiguous** admissions.

Within the 68 deterministic wrist-scaphoid admissions:

- **23** have an established chronic/nonunion phenotype;
- **45** form the comparison phenotype.

Detailed operative-note modules are available in 31 wrist-scaphoid admissions. After requiring that the operative record actually treats the wrist-scaphoid disease, the current deterministic analytic sample is:

- **15** established chronic/nonunion operative records;
- **13** comparison operative records;
- **28 total**.

All 28 current disease-concordant detailed operative records occur in **2023-2025**. This is therefore the operative study period itself, not an independent temporal sensitivity cohort.

## Comparison-group caution

The comparison group is not automatically described as acute.

A conservative pre-gold audit of the 13 comparison operative records finds explicit acute/new or recent-injury wording in only **7/13**. The remaining records contain postoperative-history wording, longer-duration wording, or insufficient explicit state evidence.

Therefore:

- the main analysis retains the neutral `comparison phenotype` label;
- a prespecified sensitivity analysis will compare chronic/nonunion records with **physician-confirmed acute/new fractures only**.

See `data/aggregate/scaphoid_comparison_state_audit_v0_1.csv`.

## Primary and secondary outcomes

### Primary outcome

**Bone-graft augmentation**.

### Key contrast outcome

**Internal fixation**.

### Secondary outcomes

- graft/reconstruction/fusion augmentation composite;
- number of major procedure components;
- individual reconstruction/fusion components when sample size permits descriptive reporting.

The primary outcome was frozen before physician-reference scoring and is not replaced by a composite simply because another analysis yields a smaller P value.

## Physician validation

The current validation gate is deliberately limited to the main-paper question:

- **88** scaphoid candidates: wrist / foot / other / uncertain anatomy;
- **68** wrist-scaphoid records: acute/new / chronic / nonunion / indeterminate state;
- **31** detailed operative-note records: target-disease relevance, fixation, bone graft, reconstruction, fusion;
- approximately 20% independent second review for inter-rater agreement.

See GitHub Issue #3 and `docs/SCAPHOID_PHYSICIAN_REVIEW_GUIDE_ZH.md`.

## Main manuscript files

- `docs/SCAPHOID_SCIENTIFIC_QUESTION_V0_1.md` — scientific question and claim boundaries;
- `docs/SCAPHOID_ANALYSIS_PLAN_V0_1.md` — focused statistical analysis plan;
- `docs/DATA_DRIVEN_QUESTION_SELECTION_V0_1.md` — why this question was selected over other signals in the fixed data;
- `docs/MANUSCRIPT_PLAN_SCAPHOID_V0_1.md` — article structure and figure plan;
- `manuscript/SCAPHOID_MANUSCRIPT_DRAFT_V0_1.md` — current English manuscript draft;
- `figures/scaphoid/Figure1_cohort_flow_pre_gold.svg` — article-style cohort flow figure.

## Main analysis code and aggregate outputs

- `src/ortho_pheno/scaphoid_augmentation_analysis_v0_1.py` — focused local analysis;
- `src/ortho_pheno/scaphoid_comparison_state_audit_v0_1.py` — comparison-state evidence audit;
- `data/aggregate/scaphoid_augmentation_signal_v0_1.csv` — public-safe treatment-composition aggregate;
- `data/aggregate/scaphoid_comparison_state_audit_v0_1.csv` — public-safe comparison-state audit;
- `src/ortho_pheno/rules.py` — anatomy/state measurement rules;
- `src/ortho_pheno/procedure_rules.py` — procedure-relevance and component rules.

## Interpretation boundary

This study can test an association between established chronic/nonunion presentation and **documented operative composition**.

It cannot establish:

- risk of future nonunion;
- postoperative union or healing time;
- treatment efficacy;
- causal treatment selection;
- superiority of one graft or fixation strategy.

## Secondary data domains

The same fixed archive also contains hallux-valgus and first-CMC OA records. Those analyses are retained as secondary/supplementary work and do not define the current main manuscript.

## Privacy

The source archive contains direct identifiers and protected clinical text. **No raw patient data, pseudonymized row-level data, admission identifiers, patient-level dates, or clinical free text are committed to this public repository.**

Public artifacts use small-cell suppression (`<5`) when necessary to prevent reverse engineering of patient-level counts.
