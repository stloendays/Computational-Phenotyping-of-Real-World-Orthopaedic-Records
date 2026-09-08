# Study Protocol

## 1. Study type

Retrospective clinical-informatics study with an embedded observational comparative analysis. The dataset is fixed: no additional local clinical data are assumed to become available.

## 2. Data domains

The study uses existing local records covering three orthopaedic domains:

- hallux valgus;
- wrist scaphoid fracture / established scaphoid nonunion phenotypes;
- first carpometacarpal osteoarthritis.

Available information includes combinations of demographics, diagnoses, complaint/examination text, operative notes, laboratory records and imaging reports/identifiers. Data completeness differs by disease and calendar period.

## 3. Unit of analysis

The primary analytical unit is the admission-level patient episode identified by the local admission identifier. Raw diagnosis rows are not treated as independent observations.

If repeated episodes from the same individual can be identified reliably, episode-level dependence will be documented and handled explicitly in sensitivity analyses.

## 4. Primary aims

### Aim 1 - Cohort reconstruction

Construct a reproducible, admission-level research dataset from heterogeneous source tables while preventing pseudoreplication and preserving provenance.

### Aim 2 - Computational phenotyping

Evaluate the accuracy and robustness of deterministic, terminology-based and LLM-assisted extraction of disease, anatomy and procedure phenotypes from Chinese orthopaedic free text.

### Aim 3 - Scaphoid phenotype comparison

Compare established chronic/nonunion scaphoid phenotypes with other **high-specificity wrist-scaphoid phenotypes** using variables observable in the existing records.

This analysis is interpreted as a retrospective phenotype-comparison/case-control analysis. It is not interpreted as a causal study of incident nonunion unless longitudinal evidence within the existing records establishes acute-to-nonunion progression.

### Aim 4 - Cross-disease generalization

Assess whether the phenotyping architecture retains specificity across deformity, trauma/nonunion and degenerative disease domains.

## 5. Prespecified hypotheses

H1. Admission-level deduplication and anatomical disambiguation will materially change apparent cohort counts relative to raw-row or broad-keyword counts.

H2. A hybrid extraction strategy combining deterministic rules with semantic inference will improve free-text phenotype recovery over simple keyword matching alone when evaluated against physician-reviewed labels.

H3. Established scaphoid nonunion/chronic phenotypes will show greater treatment complexity than other high-specificity wrist-scaphoid phenotypes, reflected in higher frequencies of grafting, reconstruction or salvage-type procedures.

No hypothesis concerning long-term postoperative efficacy, radiographic recurrence or functional recovery is prespecified because these outcomes are not available consistently in the fixed dataset.

## 6. Disease definitions

Operational definitions are version-controlled. The current primary deterministic definitions are frozen in `configs/phenotypes_v0.3.yaml`; earlier versions remain in repository history for auditability.

### 6.1 Hallux valgus

Inclusion requires evidence consistent with hallux valgus/bunion pathology in the diagnosis and/or supporting clinical text. Laterality, deformity-angle mentions and procedure components are secondary phenotypes.

### 6.2 Scaphoid anatomy

The 88 candidate scaphoid retrievals are assigned to three deterministic anatomy states under v0.3:

- `wrist_scaphoid`;
- `foot_navicular`;
- `ambiguous`.

High-specificity wrist evidence includes an explicit wrist/hand-to-scaphoid relation, scaphoid waist/pole terminology, or generic scaphoid wording plus explicit wrist context in the absence of foot-navicular evidence. The generic character `手` is not treated as anatomical evidence because words such as `手术` and `手法` otherwise produce false positives.

The current deterministic audit yields **68 wrist-scaphoid, 13 explicit foot-navicular and 7 ambiguous episodes**. Ambiguous episodes are retained for physician adjudication but excluded from the primary wrist-scaphoid clinical comparison until adjudicated.

### 6.3 Established scaphoid nonunion/chronic phenotype

Within strict wrist-scaphoid episodes, chronic/nonunion status is defined from explicit documentation of nonunion, non-healing, chronic/old scaphoid fracture, SNAC or equivalent clinician-documented chronicity.

For treatment-comparison analyses, state-defining evidence is restricted to diagnosis, complaint and physical-examination text. Operation names and operative-note contents cannot assign chronic/nonunion case status because treatment is analysed downstream.

Under v0.3 the deterministic strict wrist-scaphoid cohort contains **23 established chronic/nonunion phenotypes and 45 other wrist-scaphoid episodes**.

### 6.4 First CMC osteoarthritis

Requires first-CMC/trapeziometacarpal-specific evidence. Broad wrist arthritis terms without first-CMC anatomical support do not satisfy the strict phenotype definition.

## 7. Exposure and outcome framework

### 7.1 Scaphoid analysis

Primary grouping variable:

- established chronic/nonunion scaphoid phenotype;
- other high-specificity wrist-scaphoid phenotype.

The comparison group is intentionally not labelled uniformly "acute" because the fixed records do not establish acute status for every non-chronic episode.

Primary comparative outcomes available from current records include treatment-complexity components such as grafting, reconstruction, fixation and fusion/salvage procedures.

Because chronic/nonunion status may be present at the first local encounter, associations are interpreted descriptively/etiologically with caution and are not described as prospective predictors of future nonunion.

### 7.2 Hallux valgus analysis

Primary endpoint is procedure phenotype rather than long-term efficacy. Operative notes are represented as multi-label components including osteotomy, Chevron, fusion, K-wire fixation, resection and soft-tissue/tendon/ligament procedures.

### 7.3 First CMC analysis

Primary endpoint is strict diagnostic/anatomical classification performance and procedure extraction feasibility.

## 8. Physician reference standard and NLP validation

The fixed dataset is sufficiently modest for broad physician adjudication rather than convenience sampling. The current annotation protocol (`docs/ANNOTATION_PROTOCOL_V0_1.md`) prespecifies:

- disease/anatomy review of all 367 candidate episodes across the three domains;
- scaphoid-state review of all 68 deterministic strict wrist-scaphoid episodes;
- multi-label procedure review of all 163 detailed operative notes in the current strict cohorts;
- an approximately 20% deterministic stratified second-review subset for inter-rater reliability.

The reference standard is locked before comparing extraction methods.

Candidate systems:

1. keyword/regular-expression baseline;
2. clinical terminology dictionary;
3. LLM-assisted extraction;
4. hybrid rule + terminology + semantic extraction.

Primary metrics:

- precision;
- recall;
- specificity where meaningful;
- F1 score;
- exact-match accuracy for structured fields;
- macro-F1 and micro-F1 for multi-label procedure categories;
- inter-rater reliability for the independently double-reviewed subset.

All automated outputs used in confirmatory clinical analyses must retain provenance to source text and extraction-rule/model version.

## 9. Statistical analysis

### 9.1 Descriptive statistics

Continuous variables: mean (SD) or median (IQR), depending on distribution.

Categorical variables: count and percentage.

### 9.2 Group comparisons

- chi-square or Fisher exact test for categorical variables;
- t test or Mann-Whitney U test for continuous variables where appropriate;
- effect sizes and 95% confidence intervals reported alongside P values when privacy thresholds permit public release.

### 9.3 Regression

For scaphoid comparisons, logistic regression may be used only with a parsimonious set of prespecified covariates supported by available sample size. Firth penalized logistic regression is preferred when sparse cells or separation are present.

High-capacity machine-learning models are exploratory only and are not the primary inferential analysis.

## 10. Missing data

Missingness is treated as a property of the documentation process, not automatically as absence of a clinical feature.

Analyses distinguish:

- structurally unavailable variables;
- variables not measured/documented;
- documented negative findings;
- true numeric missing values;
- anatomy/state uncertainty.

No unvalidated imputation of free-text clinical phenotypes will be performed.

## 11. Bias control

Key threats include:

- diagnosis-keyword retrieval bias;
- anatomical ambiguity;
- duplicated diagnosis rows;
- calendar-period documentation changes;
- differential availability of operative records;
- incorporation bias if outcome-defining text is reused as a predictor;
- semantic false positives from non-anatomical Chinese words containing characters such as `手`.

Mitigations include strict source provenance, frozen versioned definitions, admission-level deduplication, explicit uncertainty states, synthetic regression tests, sensitivity analyses by documentation period, and separation of phenotype-defining evidence from explanatory variables when possible.

## 12. Sensitivity analyses

Planned sensitivity checks include:

- strict vs broad disease definitions;
- exclusion and separate adjudication of anatomically ambiguous cases;
- analysis restricted to episodes with complete operative documentation;
- calendar-period restriction where source-system completeness differs materially;
- alternative chronic/nonunion term sets only if frozen before result inspection.

The first audit identified 2023-2025 as the internally consistent documentation-era sensitivity period for scaphoid treatment comparisons.

## 13. External datasets

External public datasets may be used for methodological benchmarking, terminology normalization or pretraining. External patients are not pooled with the local clinical cohort for the primary clinical analyses.

## 14. Reproducibility and governance

No raw patient data, names, contact information, admission identifiers or free-text clinical notes containing PHI are committed to this repository.

The repository stores:

- code;
- frozen configuration files;
- synthetic test data;
- aggregate results;
- study documentation.

Physician annotation packets and row-level labels remain in `annotations/private/` or another approved local protected environment. Only aggregate validation metrics are eligible for public release.

## 15. Interpretation boundary

The study supports claims about cohort reconstruction accuracy, clinical-text phenotyping and associations observable in the existing records. It does not support claims about long-term postoperative efficacy or causal treatment effects without longitudinal outcome data.
