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

Construct a reproducible, patient-level research dataset from heterogeneous source tables while preventing pseudoreplication and preserving provenance.

### Aim 2 - Computational phenotyping

Evaluate the accuracy and robustness of deterministic, terminology-based and LLM-assisted extraction of disease, anatomy and procedure phenotypes from Chinese orthopaedic free text.

### Aim 3 - Scaphoid phenotype comparison

Compare established chronic/nonunion scaphoid phenotypes with acute wrist-scaphoid fracture phenotypes using variables observable in the existing records.

This analysis is interpreted as a retrospective phenotype-comparison/case-control analysis. It is not interpreted as a causal study of incident nonunion unless longitudinal evidence within the existing records establishes acute-to-nonunion progression.

### Aim 4 - Cross-disease generalization

Assess whether the phenotyping architecture retains specificity across deformity, trauma/nonunion and degenerative disease domains.

## 5. Prespecified hypotheses

H1. Patient-level deduplication and anatomical disambiguation will materially change apparent cohort counts relative to raw-row counts.

H2. A hybrid extraction strategy combining deterministic rules with semantic inference will improve free-text phenotype recovery over simple keyword matching alone when evaluated against physician-reviewed labels.

H3. Established scaphoid nonunion/chronic phenotypes will show greater treatment complexity than acute scaphoid fracture phenotypes, reflected in higher frequencies of grafting, reconstruction or salvage-type procedures.

No hypothesis concerning long-term postoperative efficacy, radiographic recurrence or functional recovery is prespecified because these outcomes are not available consistently in the fixed dataset.

## 6. Disease definitions

Operational definitions are version-controlled in `configs/phenotypes_v0.1.yaml`.

### 6.1 Hallux valgus

Inclusion requires evidence consistent with hallux valgus/bunion pathology in the diagnosis and/or supporting clinical text. Laterality, deformity-angle mentions and procedure components are secondary phenotypes.

### 6.2 Wrist scaphoid fracture

Records referring to foot navicular injury are excluded. Wrist/hand anatomical context, diagnosis text, examination text and operative-note evidence are used jointly for anatomical disambiguation.

### 6.3 Established scaphoid nonunion/chronic phenotype

Defined from explicit documentation of nonunion, non-healing, chronic/old scaphoid fracture, SNAC or equivalent clinician-documented chronicity. The exact term list and precedence rules are frozen before confirmatory analysis.

### 6.4 First CMC osteoarthritis

Requires first-CMC/trapeziometacarpal-specific evidence. Broad wrist arthritis terms without first-CMC anatomical support do not satisfy the strict phenotype definition.

## 7. Exposure and outcome framework

### 7.1 Scaphoid analysis

Primary grouping variable:

- established chronic/nonunion scaphoid phenotype;
- acute/other wrist-scaphoid fracture phenotype.

Primary comparative outcomes available from current records include treatment-complexity components such as grafting, reconstruction, fixation and fusion/salvage procedures.

Because chronic/nonunion status may be present at the first local encounter, associations are interpreted descriptively/etiologically with caution and are not described as prospective predictors of future nonunion.

### 7.2 Hallux valgus analysis

Primary endpoint is procedure phenotype rather than long-term efficacy. Operative notes are represented as multi-label components including osteotomy, Chevron, fusion, K-wire fixation, resection and soft-tissue/tendon/ligament procedures.

### 7.3 First CMC analysis

Primary endpoint is strict diagnostic/anatomical classification performance and procedure extraction feasibility.

## 8. NLP validation

A physician-reviewed subset should be created from the existing records only. If annotation is performed, the evaluation set must be frozen before comparing extraction methods.

Candidate systems:

1. keyword/regular-expression baseline;
2. clinical terminology dictionary;
3. LLM-assisted extraction;
4. hybrid rule + terminology + semantic extraction.

Primary metrics:

- precision;
- recall;
- F1 score;
- exact-match accuracy for structured fields;
- macro-F1 for multi-label procedure categories.

All automated outputs used in confirmatory clinical analyses must retain provenance to source text and extraction-rule/model version.

## 9. Statistical analysis

### 9.1 Descriptive statistics

Continuous variables: mean (SD) or median (IQR), depending on distribution.

Categorical variables: count and percentage.

### 9.2 Group comparisons

- chi-square or Fisher exact test for categorical variables;
- t test or Mann-Whitney U test for continuous variables where appropriate;
- effect sizes and 95% confidence intervals reported alongside P values.

### 9.3 Regression

For scaphoid comparisons, logistic regression may be used only with a parsimonious set of prespecified covariates supported by available sample size. Firth penalized logistic regression is preferred when sparse cells or separation are present.

High-capacity machine-learning models are exploratory only and are not the primary inferential analysis.

## 10. Missing data

Missingness is treated as a property of the documentation process, not automatically as absence of a clinical feature.

Analyses will distinguish:

- structurally unavailable variables;
- variables not measured/documented;
- documented negative findings;
- true numeric missing values.

No unvalidated imputation of free-text clinical phenotypes will be performed.

## 11. Bias control

Key threats include:

- diagnosis-keyword retrieval bias;
- anatomical ambiguity;
- duplicated diagnosis rows;
- calendar-period documentation changes;
- differential availability of operative records;
- incorporation bias if outcome-defining text is reused as a predictor.

Mitigations include strict source provenance, frozen definitions, patient-level deduplication, sensitivity analyses by documentation period, and separation of phenotype-defining evidence from explanatory variables when possible.

## 12. Sensitivity analyses

Planned sensitivity checks include:

- strict vs broad disease definitions;
- exclusion of anatomically ambiguous cases;
- analysis restricted to episodes with complete operative documentation;
- calendar-period restriction where source-system completeness differs materially;
- alternative chronic/nonunion term sets frozen before result inspection.

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

Any manually reviewed labels should be stored only in an approved local environment or converted to de-identified/non-reconstructable aggregate artifacts before publication.

## 15. Interpretation boundary

The study supports claims about cohort reconstruction accuracy, clinical-text phenotyping and associations observable in the existing records. It does not support claims about long-term postoperative efficacy or causal treatment effects without longitudinal outcome data.
