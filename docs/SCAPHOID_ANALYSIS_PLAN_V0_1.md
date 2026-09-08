# Focused Scaphoid Analysis Plan v0.2

## Study question

Among physician-confirmed wrist-scaphoid admissions with disease-concordant detailed operative documentation, is an established chronic/nonunion presentation associated with **bone-graft augmentation**, while internal fixation remains common across phenotype groups?

## Study design

Retrospective, fixed-data, exploratory comparative study.

The study is problem-first. Computational text processing is a measurement aid, not the scientific objective.

## Candidate retrieval

The supplied broad scaphoid search retrieved **88 admission episodes**.

The current deterministic v0.3 audit partitions these into 68 wrist scaphoid, 13 foot navicular and 7 ambiguous records. These counts are useful for pre-validation auditing but **do not define the final clinical cohort**.

## Two-stage physician cohort definition

### Stage 1 — anatomy reference standard

All 88 candidates undergo blinded physician anatomy review:

- `wrist_scaphoid`;
- `foot_navicular`;
- `other`;
- `uncertain`.

The final wrist-scaphoid cohort is defined by physician anatomy Gold, not by deterministic-rule positivity.

This two-stage design prevents verification bias that would arise if downstream state/procedure review were restricted to the rule-positive 68 records.

### Stage 2 — generated after Stage-1 anatomy freeze

After Stage 1 is adjudicated and frozen, `make_scaph_physician_packet_v0_1.py downstream` generates state and procedure review files for physician-confirmed wrist-scaphoid records.

Therefore, the final Stage-2 sample sizes are **not fixed in advance** to the current deterministic 68 wrist records or 31 detailed-note records.

## Clinical-state exposure

For physician-confirmed wrist-scaphoid records, state is determined from:

- diagnosis;
- complaint;
- physical examination.

Operative text is excluded from state assignment.

State categories:

1. `acute_or_new_fracture`;
2. `established_chronic_fracture`;
3. `established_nonunion`;
4. `chronic_nonunion_not_distinguishable`;
5. `insufficient_or_uncertain`.

For the primary clinical analysis, categories 2-4 form the `established chronic/nonunion` group. Physician-confirmed wrist-scaphoid records that are not established chronic/nonunion and are sufficiently classifiable form the main comparison group. Uncertain state is excluded from the relevant inferential comparison.

### Deterministic pre-validation observation

Under the current deterministic rules, 23/68 wrist-scaphoid records are classified established chronic/nonunion and 45/68 comparison. These are provisional audit counts only.

## Comparison-state audit and acute-only sensitivity

In the current deterministic operative comparison group, conservative source-text auditing finds explicit acute/new or recent-injury wording in only **7/13** records. The remaining records contain postoperative-history wording, longer-duration wording without an explicit chronic keyword, or insufficient explicit state evidence.

Therefore:

- the main comparison group is not labelled uniformly acute;
- a prespecified sensitivity analysis restricts controls to **physician-confirmed `acute_or_new_fracture`** records only.

See `data/aggregate/scaphoid_comparison_state_audit_v0_1.csv`.

## Operative analytic population

Within physician-confirmed wrist-scaphoid records that have a detailed operative-note module, physicians first determine:

`target_disease_procedure_present = yes / no / uncertain`.

Only disease-concordant wrist-scaphoid operative records enter the treatment-composition analysis.

### Deterministic pre-validation observation

The current rule-based audit identifies:

- 31 detailed-note module records among deterministic wrist-scaphoid cases;
- 28 disease-concordant detailed operative records;
- 15 established chronic/nonunion and 13 comparison operative records.

All 28 current disease-concordant records occur in **2023-2025**. These are provisional denominators; final manuscript denominators will be regenerated from physician anatomy/state/procedure Gold.

The 2023-2025 period is the operative study period represented by the supplied detailed records, not an independent temporal validation subset.

## Primary outcome

### Bone-graft augmentation

Binary physician-adjudicated target-disease procedure component:

- yes: bone graft/harvest explicitly used as part of the wrist-scaphoid operation;
- no: no graft component after review.

Bone graft was selected before physician-reference scoring because it is a specific biologic augmentation step and avoids defining the primary result through a post-hoc composite.

## Key contrast outcome

### Internal fixation

The scientific pattern being tested is a dissociation:

- fixation remains common across phenotype groups;
- graft augmentation increases in established chronic/nonunion presentations.

## Secondary outcomes

1. graft/reconstruction/fusion augmentation composite;
2. number of major procedure components among fixation, graft, reconstruction and fusion;
3. individual reconstruction/fusion components, reported descriptively when sparse.

These remain secondary regardless of their P values.

## Baseline descriptors

Report by physician-adjudicated operative phenotype group:

- age;
- sex;
- BMI;
- other clearly documented preoperative descriptors if sufficiently complete and clinically interpretable.

Missing denominators are reported explicitly.

## Statistical analysis

### Primary analysis

Bone-graft augmentation:

- 2×2 table;
- Fisher exact test;
- crude odds ratio and 95% confidence interval.

### Key contrast

Internal fixation:

- Fisher exact test;
- crude odds ratio and 95% confidence interval.

### Secondary treatment-intensity analysis

Major procedure-component count:

- median and IQR;
- Mann-Whitney U test.

### Adjustment

No routine multivariable model is prespecified for the current small operative sample. Sparse-data regression is considered only if the physician-defined final sample supports a clinically defensible covariate set.

No stepwise selection, random forest, XGBoost or neural-network model is used to answer the primary question.

## Missingness and uncertainty

- missing detailed operative note ≠ no surgery;
- unrelated detailed operative note ≠ target-disease surgery;
- absence of a chronic keyword ≠ acute disease;
- undocumented procedure component is not treated as clinically validated absence until physician review;
- anatomy/state/relevance uncertainty is retained explicitly rather than force-classified.

## Physician validation and double review

### Stage 1

- all 88 anatomy candidates undergo primary review;
- approximately 20% undergo independent second review;
- disagreements are adjudicated before Stage-1 freeze.

### Stage 2

Generated only from physician-confirmed wrist scaphoid:

- every physician-confirmed wrist record receives state review;
- every physician-confirmed wrist record with a detailed operative module receives procedure relevance/component review;
- approximately 20% of each Stage-2 layer undergoes independent second review.

Reviewer 2 remains blinded to reviewer 1 and to all rule/model outputs.

## Sensitivity and robustness analyses

1. primary physician-defined chronic/nonunion vs full classifiable comparison group;
2. **physician-confirmed acute-only sensitivity analysis**;
3. exclusion of uncertain procedure relevance;
4. primary bone-graft outcome vs broader augmentation composite;
5. leave-one-out influence analysis for the primary 2×2 association;
6. exclusion of records with competing same-admission orthopaedic procedures;
7. deterministic pre-validation estimate vs physician-adjudicated estimate, reported as measurement robustness rather than model superiority.

Because the supplied detailed operative records are concentrated in 2023-2025, historical detailed-procedure replication is not available.

## Claim boundary

The strongest allowed claim is an association between established chronic/nonunion presentation and **documented operative composition**.

The study cannot establish:

- future nonunion risk;
- postoperative union or healing time;
- treatment efficacy;
- causal treatment selection;
- superiority of a graft technique.
