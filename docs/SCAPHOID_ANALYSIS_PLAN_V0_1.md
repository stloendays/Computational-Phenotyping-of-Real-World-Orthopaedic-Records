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

The comparison phenotype is not uniformly labelled acute because the fixed record does not prove acute status for every episode.

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
- BMI is reported with its actual denominator.

## Physician validation gate

Final clinical estimates require physician adjudication of:

1. wrist-scaphoid anatomy;
2. chronic/nonunion state;
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
3. primary bone-graft outcome versus broader augmentation composite;
4. leave-one-out influence check for the primary 2×2 association;
5. descriptive analysis after excluding records with competing same-admission orthopaedic procedures.

These checks evaluate label and influence robustness rather than claiming an independent temporal validation cohort.

## Claim boundary

The strongest allowed claim is an association between established chronic/nonunion phenotype and the **composition of documented surgery**.

The study cannot establish:

- future nonunion risk;
- treatment efficacy;
- postoperative union;
- causal treatment selection;
- superiority of a graft strategy.
