# Statistical and Computational Analysis Plan

> **Current manuscript direction:** the main paper is now problem-first and scaphoid-focused. The operative association analysis is governed by `docs/SCAPHOID_SCIENTIFIC_QUESTION_V0_1.md` and `docs/SCAPHOID_ANALYSIS_PLAN_V0_1.md`. The broader multi-disease sections below are retained as secondary/supplementary infrastructure.

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

For the **main scaphoid manuscript**, physician review is restricted to the variables needed for the scientific question:

- all 88 scaphoid-retrieval candidate admissions for wrist/foot/ambiguous anatomy;
- all 68 deterministic wrist-scaphoid admissions for chronic/nonunion state;
- all 31 wrist-scaphoid admissions with a detailed operative-note module for target-disease relevance, fixation and bone-graft labels.

The broader three-disease annotation design remains optional supplementary work and is not a prerequisite for the scaphoid paper.

An approximately 20% deterministic stratified subset should be independently reviewed by a second clinician. The reference standard is frozen before method comparison, and the same labels are used for every extraction system.

### Systems

1. keyword/regex baseline;
2. dictionary/terminology baseline;
3. LLM-assisted structured extraction, if needed;
4. hybrid extraction, if needed.

The main paper does not require an LLM claim. If simple rules and physician abstraction are sufficient, LLM evaluation may remain supplementary or be omitted.

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

Unrelated operations remain in the evaluation set as hard negatives.

**Stage 2 - clinically required component extraction**

For the main scaphoid paper, the required labels are:

- internal fixation;
- bone graft;
- reconstruction/fusion when present.

Report per-label precision, recall and F1. A full multi-label benchmark across all disease domains is supplementary.

Inter-rater reliability is reported on the independently double-reviewed subset. Confidence intervals should be estimated at the admission level when sample size permits.

## 5. Primary scaphoid clinical analysis

### Scientific question

Among high-specificity wrist-scaphoid admissions with disease-concordant detailed operative documentation, is established chronic/nonunion disease associated with **bone-graft augmentation**, while internal fixation remains common in both phenotype groups?

### Primary grouping

Within the v0.3 high-specificity wrist-scaphoid cohort:

- established chronic/nonunion phenotype: 23;
- comparison wrist-scaphoid phenotype: 45.

The comparison group is not uniformly described as acute because the fixed records do not establish acute status for every non-chronic episode.

Established chronic/nonunion status is assigned only from non-operative clinical sources: diagnosis, complaint and physical-examination text. Operative names and operative-note contents are explicitly excluded from exposure assignment.

### Operative denominator

A detailed operative-note module is a data-availability variable, not proof that the documented operation treated the wrist scaphoid.

Current audit:

- detailed operative-note module available: 18/23 versus 13/45;
- disease-concordant detailed operative records: 15/23 versus 13/45.

Only disease-concordant operative admissions contribute to target-disease treatment composition.

### Operative study period

**All 28 disease-concordant detailed operative admissions occur in 2023-2025.** Therefore 2023-2025 is the actual operative-analysis period under the supplied exports. It is not an independent sensitivity subgroup.

Earlier years may contribute to cohort/state description but cannot provide a separate detailed-procedure replication.

### Primary outcome

**Bone-graft augmentation**.

This is selected as a specific biologic augmentation step rather than a post-hoc composite.

### Key contrast outcome

**Internal fixation**.

The scientific pattern of interest is a treatment-composition shift in which fixation remains common across groups while biologic augmentation increases in established chronic/nonunion presentations.

### Secondary outcomes

- graft/reconstruction/fusion augmentation composite;
- number of major procedure components among fixation, graft, reconstruction and fusion;
- individual reconstruction/fusion components, interpreted descriptively when sparse.

### Descriptive statistics

Categorical variables: n (%).

Continuous variables: median (IQR) unless distribution and scale justify mean (SD).

Age, sex and BMI are baseline descriptors. Missing denominators are reported explicitly.

### Primary inference

Bone-graft augmentation:

- Fisher exact test;
- crude odds ratio with 95% confidence interval in the internal/manuscript analysis.

Internal fixation is analysed with the same sparse-table approach as a key contrast.

### Secondary treatment-intensity analysis

Major procedure-component count may be compared with a Mann-Whitney U test. It remains secondary even if its P value is smaller than the primary bone-graft comparison.

### Adjustment

The current 28-record operative sample does not justify a routine high-dimensional multivariable model. No stepwise selection, random forest, XGBoost or neural-network model is used for the primary clinical question.

A sparse-data regression is considered only if physician adjudication materially changes the evaluable sample and the covariate count remains clinically defensible.

### Interpretation

The primary claim concerns association between established phenotype group and documented treatment composition. The study does not predict future nonunion and does not evaluate postoperative union or treatment efficacy.

## 6. Hallux valgus secondary analysis

Hallux-valgus analyses are retained as secondary/supplementary work rather than the main manuscript direction.

Among 193 strict hallux-valgus admissions, 114 have a detailed operative-note module and 113 currently satisfy deterministic target-disease procedure concordance.

Potential secondary outputs include:

- procedure-component prevalence;
- common procedure combinations;
- exploratory associations between preoperative phenotype terms and common procedures.

These analyses must not displace the scaphoid question solely because an exploratory P value is smaller.

## 7. First CMC OA secondary analysis

First-CMC OA is retained primarily as a secondary anatomy/diagnostic disambiguation problem. The small strict cohort is not used for high-capacity prediction.

## 8. Robustness analysis for the scaphoid question

Because the supplied detailed operative records are confined to 2023-2025, temporal replication is not available.

Prespecified robustness checks are therefore:

1. deterministic labels versus physician-adjudicated labels;
2. exclusion of uncertain exposure/procedure-relevance records;
3. primary bone-graft outcome versus the broader augmentation composite;
4. leave-one-out influence analysis for the primary 2×2 association;
5. exclusion of records containing competing same-admission orthopaedic procedures.

These are label/influence robustness analyses, not independent temporal validation.

## 9. Missing-data and uncertainty strategy

- report availability for every key variable;
- distinguish missing module, available module with unrelated procedure, and target-disease procedure documentation;
- do not code undocumented free-text phenotypes as negative without physician validation;
- preserve an explicit `uncertain` state where anatomy, clinical state or procedure relevance cannot be supported;
- avoid multiple imputation for sparse text-derived variables unless assumptions are defensible;
- complete-case regression is allowed only with explicit denominator reporting.

## 10. Multiplicity

The study distinguishes:

- the prespecified bone-graft primary outcome;
- internal fixation as the key contrast;
- secondary augmentation/component-count analyses;
- exploratory supplementary analyses.

Exploratory P values are interpreted descriptively.

## 11. Machine learning boundary

High-capacity ML is not a primary objective.

Any model-performance analysis exists only to validate measurement of the clinical variables required for the paper. If simple abstraction/rules are adequate, more complex models are omitted rather than added for novelty.

## 12. Public-release privacy rules

The public repository contains aggregate outputs only.

- patient-level rows, identifiers, dates and free text are never committed;
- non-zero aggregate cells smaller than 5 are displayed as `<5`;
- if an odds ratio, confidence interval or exact P value could reveal a suppressed 1-4 cell, the inferential statistic is also suppressed;
- rare procedure combinations are pooled rather than released individually.

These rules apply to public artifacts and do not alter the authorized internal statistical calculations.

## 13. Reproducibility outputs

Every result table or figure should be generated from:

- a versioned configuration;
- a deterministic analysis script;
- an aggregate output file;
- a recorded random seed when stochastic procedures are used.

No manual Excel-derived manuscript numbers should remain untraceable to code.
