# Statistical and Computational Analysis Plan

## 1. Analysis philosophy

The primary objective is valid inference from a fixed, modest-sized clinical dataset. Computational methods are used to reconstruct and validate phenotypes; they are not used to manufacture predictive claims unsupported by available outcomes.

## 2. Cohort audit before inference

Before any confirmatory analysis, generate an audit table for each disease domain containing:

- raw row count;
- unique admission count;
- strict phenotype count;
- anatomically ambiguous count;
- operative-note module availability;
- target-disease procedure-note availability;
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
- strict phenotype precision against physician adjudication;
- unresolved ambiguity rate.

### Scaphoid anatomy gate

Under phenotype **v0.3**, every scaphoid candidate is first assigned to one of three deterministic anatomy states:

- `wrist_scaphoid`;
- `foot_navicular`;
- `ambiguous`.

Only deterministic `wrist_scaphoid` episodes enter the primary pre-validation clinical comparison. `ambiguous` episodes are retained for physician adjudication and are not forced into either group.

The frozen v0.3 candidate audit is:

- 68 wrist-scaphoid;
- 13 foot-navicular;
- 7 ambiguous;
- 88 candidates total.

The standalone Chinese character `手` cannot establish hand anatomy because common words such as `手术` and `手法` otherwise produce false positives. Explicit local anatomical relations are required.

## 4. Aim 2: Physician reference standard and NLP phenotype validation

### Evaluation design

The fixed dataset is sufficiently modest to support broad physician adjudication rather than convenience sampling. The current plan reviews:

- all 367 disease/anatomy candidate episodes;
- all 68 deterministic strict wrist-scaphoid episodes for clinical state;
- all 163 strict-cohort admissions with a detailed operative-note module for procedure relevance and multi-label procedure phenotypes.

An approximately 20% deterministic stratified subset is independently reviewed by a second clinician. The reference standard is frozen before method comparison, and the same labels are used for every extraction system.

### Systems

1. keyword/regex baseline;
2. dictionary/terminology baseline;
3. LLM-assisted structured extraction;
4. hybrid extraction.

### Disease/anatomy and state metrics

For binary/categorical phenotypes:

- precision;
- recall;
- F1;
- specificity where meaningful;
- exact agreement;
- confusion matrix.

### Procedure attribution and procedure-label metrics

Procedure evaluation is explicitly hierarchical.

**Stage 1 - relevance/attribution**

Each module-available operative admission receives:

`target_disease_procedure_present = yes / no / uncertain`

This stage is evaluated as a clinical extraction task rather than hidden preprocessing. Unrelated operations remain in the evaluation set as hard negatives.

**Stage 2 - multi-label procedure extraction**

Procedure-component labels are clinically interpreted only for physician-adjudicated target-disease procedure records. Report:

- per-label precision, recall and F1;
- macro-F1;
- micro-F1;
- exact-set match;
- label-cardinality error.

A secondary end-to-end evaluation may score the joint task in which an algorithm must first identify target-disease relevance and then recover the correct procedure set.

Inter-rater reliability is reported on the independently double-reviewed subset. Confidence intervals should be estimated by admission-level bootstrap when sample size permits.

### Error taxonomy

Errors are categorized as:

- anatomical confusion;
- negation failure;
- temporal/state confusion;
- procedure-attribution error;
- procedure-component omission;
- overcalling from broad terminology;
- abbreviation/variant failure;
- unsupported semantic inference;
- source-scope violation;
- documentation insufficiency.

## 5. Aim 3: Scaphoid comparison

### Primary grouping

Within the v0.3 high-specificity wrist-scaphoid cohort:

- established chronic/nonunion phenotype: 23;
- other wrist-scaphoid phenotype: 45.

The comparison group is not uniformly described as acute because the fixed records do not establish acute status for every non-chronic episode.

Established chronic/nonunion status is assigned only from non-operative clinical sources: diagnosis, complaint and physical-examination text. Operative names and operative-note contents are explicitly excluded from case assignment because treatment variables are downstream comparison outcomes. This prevents circular case definition and leakage.

### Procedure denominator rule

A detailed operative-note module is a data-availability variable, not proof that the documented operation treated the wrist scaphoid. The current audit gives:

- module-available detailed operative admissions: 18/23 versus 13/45;
- disease-concordant procedure admissions: 15/23 versus 13/45.

Only disease-concordant operative admissions contribute to target-disease procedure prevalence and treatment-complexity comparisons. Module availability remains separately reported to characterize documentation architecture.

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

Report effect sizes with 95% confidence intervals when public-release cell-size constraints permit.

### Adjusted analysis

If event counts support multivariable analysis, use a parsimonious logistic model. Firth logistic regression is preferred when separation or sparse events occur.

No stepwise variable selection is used for confirmatory claims.

Potential adjustment covariates are limited to variables demonstrably available before or at the defining clinical episode and selected before result inspection.

### Interpretation

The primary claim concerns association between established phenotype group and treatment complexity. The model is not described as predicting future nonunion unless the local record explicitly establishes longitudinal progression from an acute baseline.

## 6. Aim 4: Hallux valgus procedure phenotyping

### Procedure denominator rule

Among 193 strict hallux-valgus admissions, 114 have a detailed operative-note module and 113 currently satisfy deterministic target-disease procedure concordance. The latter is the pre-validation denominator for clinical treatment-pattern summaries. All 114 remain in the physician/algorithm validation set so procedure attribution can be measured.

### Primary outputs

- target-disease procedure relevance accuracy;
- prevalence of operative components among disease-concordant notes;
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
- competing-diagnosis categories from broad retrieval;
- NLP precision/recall under strict anatomy requirements;
- procedure-attribution specificity in a small degenerative-hand domain.

The current deterministic audit identifies 18 detailed-note module admissions and 18 disease-concordant procedure admissions. The small strict cohort is not used to train a high-capacity predictive model.

## 8. Calendar-period sensitivity

Because documentation completeness differs across periods, repeat key descriptive analyses under:

1. all available years;
2. years with complete operative-note capture;
3. the most internally consistent documentation era.

The cohort audit identifies **2023-2025** as the internally consistent era for the current scaphoid treatment-comparison sensitivity analysis. Under v0.3 this era contains 18 established chronic/nonunion and 14 comparison episodes.

In the supplied exports, 2019-2022 retains complaint/examination records but lacks the operative-note, imaging-exam and laboratory modules for hallux-valgus and scaphoid cohorts. The purpose of restriction is to test robustness to the source-system shift, not to optimize statistical significance.

## 9. Missing-data and uncertainty strategy

- report availability for every key variable;
- distinguish missing module, available module with unrelated procedure, and target-disease procedure documentation;
- do not code undocumented free-text phenotypes as negative;
- preserve an explicit `uncertain` state where anatomy, clinical state or procedure relevance cannot be supported;
- avoid multiple imputation for sparse text-derived variables unless assumptions are defensible;
- complete-case regression is allowed only with explicit denominator reporting and sensitivity analysis.

## 10. Multiplicity

The study distinguishes:

- prespecified primary comparisons;
- secondary analyses;
- exploratory analyses.

Exploratory P values are interpreted descriptively. False-discovery-rate adjustment may be used for large families of procedure-label comparisons.

## 11. Machine learning boundary

High-capacity ML is not a primary objective. Any exploratory ML model must use admission/patient-level separation and nested tuning where applicable.

Performance claims require:

- no leakage between train/test episodes from the same patient where patient identity can be resolved;
- confidence intervals;
- calibration assessment if probabilistic prediction is reported;
- comparison with a simple baseline.

If sample size does not support these requirements, the ML analysis is omitted rather than overstated.

## 12. Public-release privacy rules

The public repository contains aggregate outputs only.

- patient-level rows, identifiers, dates and free text are never committed;
- non-zero aggregate cells smaller than 5 are displayed as `<5`;
- if an odds ratio, confidence interval or exact P value could reveal a suppressed 1-4 cell, the inferential statistic is also suppressed;
- rare multi-label procedure combinations are pooled rather than released individually.

These rules apply to public artifacts and do not alter the internal statistical calculations.

## 13. Reproducibility outputs

Every result table or figure should be generated from:

- a versioned configuration;
- a deterministic analysis script;
- an aggregate output file;
- a recorded random seed when stochastic procedures are used.

No manual Excel-derived manuscript numbers should remain untraceable to code. Rule changes are documented in `docs/PHENOTYPE_CHANGELOG.md` or the corresponding procedure-context audit before regenerated results are treated as current.
