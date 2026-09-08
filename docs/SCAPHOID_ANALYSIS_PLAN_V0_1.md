# Focused Scaphoid Analysis Plan v0.1

## Study question

Among high-specificity wrist-scaphoid admissions with disease-concordant detailed operative documentation, is an established chronic/nonunion phenotype associated with **bone-graft augmentation**, while internal fixation remains common in both phenotype groups?

## Study design

Retrospective, fixed-data, exploratory comparative study.

The study is explicitly **problem-first**. Computational text processing is used only to measure exposure and operative components from the existing records.

## Cohort construction

### Candidate retrieval

88 admissions were retrieved under the supplied broad scaphoid search.

### Anatomy restriction

Phenotype v0.3 partitions these candidates into:

- 68 high-specificity wrist-scaphoid admissions;
- 13 explicit foot-navicular admissions;
- 7 anatomically ambiguous admissions.

Only the 68 high-specificity wrist-scaphoid admissions enter the current pre-validation clinical study.

## Exposure

### Established chronic/nonunion

Defined from diagnosis, complaint and physical-examination text only.

Operative text is excluded from exposure assignment.

Current deterministic counts:

- established chronic/nonunion: 23;
- comparison phenotype: 45.

The comparison phenotype is **not** uniformly labelled acute because the fixed record does not prove acute status for every episode.

### Comparison-state audit

A conservative deterministic audit of the 13 disease-concordant operative records in the comparison group found explicit acute/new or recent-injury wording in 7/13. The remaining records include postoperative-history wording, month/year duration wording without a chronic keyword, or insufficient explicit state evidence.

This audit does not reclassify records. It establishes that the main comparison group must retain the neutral label `comparison phenotype` until physician adjudication.

The aggregate audit is versioned in `data/aggregate/scaphoid_comparison_state_audit_v0_1.csv`.

## Operative analytic population

Detailed operative-note availability and target-disease relevance are separated.

Current disease-concordant detailed operative sample:

- chronic/nonunion: 15;
- comparison: 13;
- total: 28.

**All 28 records occur in 2023-2025.** Consequently, 2023-2025 is the operative study period itself. It is not treated as an independent sensitivity cohort.

Earlier years remain useful for cohort/state description but cannot independently replicate detailed procedure composition under the supplied exports.

## Primary outcome

### Bone-graft augmentation

Binary target-disease procedure component:

- yes: bone graft/harvest explicitly documented in the disease-concordant operative record;
- no: no such component documented after physician validation.

This outcome was selected because it represents a specific biologic augmentation step and does not require constructing a post-hoc severity score.

## Key contrast outcome

### Internal fixation

The primary scientific pattern is expected to be a dissociation:

- internal fixation remains common across phenotype groups;
- bone-graft augmentation increases in established chronic/nonunion presentations.

This contrast is more informative than simply stating that chronic/nonunion surgery is 'more complex'.

## Secondary outcomes

1. any augmentation composite: bone graft, reconstruction or fusion;
2. number of major procedure components among fixation, graft, reconstruction and fusion;
3. individual fusion/reconstruction components, reported descriptively when sparse.

The composite and component-count analyses remain secondary even if their P values are smaller than the primary analysis.

## Baseline descriptors

Report by operative phenotype group:

- age;
- sex;
- BMI;
- relevant documented disease-severity descriptors where physician validation supports them.

Current deterministic operative subset shows similar age and BMI distributions between groups; these are descriptive observations pending reference-standard validation.

## Statistical analysis

### Primary analysis

Bone-graft augmentation:

- 2×2 table;
- Fisher exact test;
- crude odds ratio and 95% confidence interval in the internal/manuscript analysis.

The primary comparison is `established chronic/nonunion` versus the full physician-adjudicated non-established comparison group, because this preserves the fixed-data cohort without post-hoc exclusion.

### Key contrast

Internal fixation:

- Fisher exact test;
- odds ratio and 95% confidence interval.

### Secondary treatment-intensity analysis

Major procedure-component count:

- median and IQR;
- Mann-Whitney U test.

### Adjustment

No routine multivariable model is prespecified for the 28-record operative sample. A sparse-data regression is only considered if physician adjudication changes the evaluable sample sufficiently and the covariate count remains clinically defensible.

No model selection by P value is allowed.

## Missing data

- missing detailed operative note ≠ no surgery;
- detailed operative note for another anatomical problem ≠ target-disease surgery;
- undocumented procedure component ≠ validated absence until physician review;
- absence of an acute keyword ≠ chronic disease;
- BMI is reported with its actual denominator.

## Physician validation gate

Final clinical estimates require physician adjudication of:

1. wrist-scaphoid anatomy;
2. clinical state using the prespecified categories `acute/new`, `established chronic`, `established nonunion`, `chronic/nonunion not distinguishable`, or `insufficient/uncertain`;
3. operative-note target-disease relevance;
4. internal fixation;
5. bone graft;
6. reconstruction/fusion when relevant.

The frozen deterministic baseline is evaluated against this reference standard but cannot define the reference standard.

## Sensitivity analyses

Given the fixed export structure, there is no independent earlier-era detailed-note replication.

Prespecified robustness checks are therefore:

1. physician-adjudicated labels versus deterministic labels;
2. exclusion of uncertain exposure or procedure relevance;
3. **acute-only sensitivity analysis:** compare established chronic/nonunion records only with physician-confirmed `acute/new fracture` operative records; postoperative-history, long-duration-but-indeterminate and insufficient-state comparison records are excluded from this sensitivity analysis;
4. primary bone-graft outcome versus broader augmentation composite;
5. leave-one-out influence check for the primary 2×2 association;
6. descriptive analysis after excluding records with competing same-admission orthopaedic procedures.

The acute-only analysis is prespecified because the deterministic comparison-state audit showed that only 7/13 current comparison operative records carry explicit acute/recent-injury wording. It is not introduced in response to the final physician-labelled effect estimate.

These checks evaluate state-definition, label and influence robustness rather than claiming an independent temporal validation cohort.

## Claim boundary

The strongest allowed claim is an association between established chronic/nonunion phenotype and the **composition of documented surgery**.

The study cannot establish:

- future nonunion risk;
- treatment efficacy;
- postoperative union;
- causal treatment selection;
- superiority of a graft strategy.
