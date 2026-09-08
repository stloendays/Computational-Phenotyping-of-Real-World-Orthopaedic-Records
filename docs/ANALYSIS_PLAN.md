# Statistical and Computational Analysis Plan

## 1. Analysis philosophy

The primary objective is valid inference from a fixed, modest-sized clinical dataset. Computational methods are used to reconstruct and validate phenotypes; they are not used to manufacture predictive claims unsupported by available outcomes.

## 2. Cohort audit before inference

Before any confirmatory analysis, generate an audit table for each disease domain containing:

- raw row count;
- unique admission count;
- strict phenotype count;
- anatomically ambiguous count;
- operative-note availability;
- imaging-report availability;
- laboratory availability;
- calendar-period distribution.

No manuscript-level effect estimate is generated before this audit is frozen.

## 3. Aim 1: Cohort reconstruction

### Primary outputs

- reduction from raw rows to unique episodes;
- discordance between broad keyword retrieval and strict phenotype classification;
- proportion of records requiring anatomical disambiguation;
- source-period completeness profile.

### Key quality indicators

- duplicate-row inflation factor = raw rows / unique episodes;
- strict phenotype precision on a manually reviewed sample;
- unresolved ambiguity rate.

## 4. Aim 2: NLP phenotype validation

### Evaluation design

A physician-reviewed evaluation subset is frozen before method comparison. The same evaluation set is used for all extraction systems.

### Systems

1. keyword/regex baseline;
2. dictionary/terminology baseline;
3. LLM-assisted structured extraction;
4. hybrid extraction.

### Metrics

For binary phenotypes:

- precision;
- recall;
- F1;
- specificity where meaningful;
- exact agreement.

For multi-label procedure extraction:

- per-label F1;
- macro-F1;
- micro-F1;
- exact-set match.

Confidence intervals should be estimated by patient-level bootstrap when sample size permits.

### Error taxonomy

Errors are categorized as:

- anatomical confusion;
- negation failure;
- temporal confusion;
- procedure-component omission;
- overcalling from broad terminology;
- abbreviation/variant failure;
- unsupported semantic inference.

## 5. Aim 3: Scaphoid comparison

### Primary grouping

- established chronic/nonunion phenotype;
- acute/other wrist-scaphoid phenotype.

### Primary clinical comparison

Treatment-complexity components, especially:

- fixation;
- bone grafting;
- reconstruction;
- fusion/salvage.

### Descriptive statistics

Categorical variables: n (%).

Continuous variables: mean (SD) or median (IQR) depending on distribution.

### Unadjusted inference

Categorical comparisons: Fisher exact test preferred for sparse cells.

Continuous comparisons: Mann-Whitney U or t test, selected according to distribution and scale.

Report effect sizes with 95% confidence intervals.

### Adjusted analysis

If event counts support multivariable analysis, use a parsimonious logistic model. Firth logistic regression is preferred when separation or sparse events occur.

No stepwise variable selection is used for confirmatory claims.

Potential adjustment covariates are limited to variables demonstrably available before or at the defining clinical episode and selected before result inspection.

### Interpretation

The primary claim concerns association between phenotype group and treatment complexity. The model is not described as predicting future nonunion unless the local record explicitly establishes longitudinal progression.

## 6. Aim 4: Hallux valgus procedure phenotyping

### Primary outputs

- prevalence of operative components;
- co-occurrence matrix of procedure labels;
- common procedure combinations;
- association of available baseline phenotype variables with broad procedure classes.

### Optional exploratory analyses

- hierarchical clustering of procedure combinations;
- simple latent treatment-pattern groups;
- penalized logistic regression for common procedure labels only.

These analyses are exploratory and should not be framed as treatment recommendations.

## 7. First CMC OA cross-disease validation

Primary outputs:

- broad-keyword retrieval count;
- strict first-CMC phenotype count;
- false-positive categories from broad retrieval;
- NLP precision/recall under strict anatomy requirements.

The small strict cohort is not used to train a high-capacity predictive model.

## 8. Calendar-period sensitivity

Because documentation completeness differs across periods, repeat key descriptive analyses under:

1. all available years;
2. years with complete operative-note capture;
3. the most internally consistent documentation era.

The purpose is to test robustness to source-system changes, not to optimize significance.

## 9. Missing-data strategy

- report availability for every key variable;
- do not code undocumented free-text phenotypes as negative;
- avoid multiple imputation for sparse text-derived variables unless assumptions are defensible;
- complete-case regression is allowed only with explicit denominator reporting and sensitivity analysis.

## 10. Multiplicity

The study distinguishes:

- prespecified primary comparisons;
- secondary analyses;
- exploratory analyses.

Exploratory P values are interpreted descriptively. False-discovery-rate adjustment may be used for large families of procedure-label comparisons.

## 11. Machine learning boundary

High-capacity ML is not a primary objective. Any exploratory ML model must use patient-level separation and nested tuning where applicable.

Performance claims require:

- no leakage between train/test patients;
- confidence intervals;
- calibration assessment if probabilistic prediction is reported;
- comparison with a simple baseline.

If sample size does not support these requirements, the ML analysis is omitted rather than overstated.

## 12. Reproducibility outputs

Every result table or figure should be generated from:

- a versioned configuration;
- a deterministic analysis script;
- an aggregate output file;
- a recorded random seed when stochastic procedures are used.

No manual Excel-derived manuscript numbers should remain untraceable to code.
