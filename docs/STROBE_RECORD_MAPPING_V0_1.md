# STROBE + RECORD Reporting Map v0.1

**Manuscript:** focused retrospective wrist-scaphoid treatment-composition study  
**Current draft:** `manuscript/SCAPHOID_MANUSCRIPT_DRAFT_V0_4.md`  
**Current analysis plan:** `docs/SCAPHOID_ANALYSIS_PLAN_V0_3.md`

This document is a submission-preparation audit. It does not change the scientific question, exposure, primary outcome, or statistical hierarchy.

## Why both guidelines apply

The study is an observational retrospective study and therefore follows **STROBE** reporting principles. It also uses routinely collected hospital EHR data that were not originally created for the present research question, so **RECORD** is used as the relevant STROBE extension for routinely collected health data.

Primary references:

- STROBE Statement combined checklist for cohort, case-control, and cross-sectional observational studies: https://www.strobe-statement.org/checklists/
- Benchimol EI, et al. The REporting of studies Conducted using Observational Routinely-collected health Data (RECORD) Statement. *PLoS Med*. 2015;12:e1001885. doi:10.1371/journal.pmed.1001885.

Status legend:

- **READY** — current manuscript/repository already contains the necessary substance;
- **PARTIAL** — substance exists but needs explicit manuscript wording or final Gold values;
- **BLOCKED** — cannot be finalized until physician Gold or administrative information is available;
- **NOT APPLICABLE** — item does not materially apply to this study.

---

# Title and abstract

| Guideline item | Requirement | Current status | Manuscript action |
|---|---|---|---|
| STROBE 1a | Identify the observational design in title/abstract | **PARTIAL** | Current title says “Retrospective Study,” which is acceptable. Keep “retrospective” in the final title or abstract. |
| STROBE 1b | Balanced summary of methods and findings | **BLOCKED** | Abstract structure exists in v0.4. Replace provisional deterministic values with physician-Gold results before submission. |
| RECORD 1.1 | Name the type of routinely collected data | **PARTIAL** | State explicitly in the abstract that the source was routinely collected hospital electronic health records / EHR exports. Do not describe it only as a “database.” |
| RECORD 1.2 | Report geographic region and time frame where appropriate | **PARTIAL** | State single-centre hospital setting and source-data period 2015-2025. The operative analytic records currently appear concentrated in 2023-2025; final Gold period must be reported separately. |
| RECORD 1.3 | State database linkage if performed | **PARTIAL** | This study performs record-level linkage across hospital export modules rather than linkage of independent external databases. Abstract wording should say that diagnosis, complaint/examination, and operative modules were linked at the admission-episode level. |

### Recommended title-level design wording

Current clinical title can remain concise. The abstract Methods should include a phrase such as:

> “We conducted a retrospective observational study using routinely collected hospital electronic health-record exports.”

---

# Introduction

| Guideline item | Requirement | Current status | Manuscript action |
|---|---|---|---|
| STROBE 2 | Explain scientific background/rationale | **READY** | v0.4 correctly frames mechanical fixation versus biological augmentation rather than an AI framework. |
| STROBE 3 | State objectives and prespecified hypotheses | **READY** | Primary bone-graft outcome, fixation contrast, and duration secondary hypothesis are explicitly ordered. Preserve this hierarchy. |
| RECORD introduction extension | Explain why routinely collected data are suitable for the question | **PARTIAL** | Add 1-2 sentences explaining that operative notes permit decomposition of treatment components unavailable in claims-only datasets, while acknowledging routine documentation limitations. |

---

# Methods — study design and setting

| Guideline item | Requirement | Current status | Manuscript action |
|---|---|---|---|
| STROBE 4 | Present key study-design elements early | **READY** | v0.4 identifies a retrospective fixed-data observational study. |
| STROBE 5 | Setting, location, dates, recruitment/data-collection periods | **PARTIAL** | Report hospital/department type, country/region, source period 2015-2025, and final operative analytic period after Gold. Do not imply continuous module completeness across 2015-2025. |
| RECORD 1.2/setting | Geographic/time context for routine data | **PARTIAL** | Explicitly distinguish **source archive period** from **effective detailed-operative analysis period**. |

### Required wording about the time structure

The manuscript should explicitly state that the source export spans 2015-2025 but that the supplied modules show a structural data-availability discontinuity, with detailed disease-concordant scaphoid operative records currently concentrated in 2023-2025.

Do not describe the dataset as a complete continuous 2015-2025 operative cohort.

---

# Methods — participants and cohort construction

| Guideline item | Requirement | Current status | Manuscript action |
|---|---|---|---|
| STROBE 6a | Eligibility criteria and participant selection | **PARTIAL** | Two-stage physician selection is documented. Final counts/reasons require Gold. |
| STROBE 6b | Matching criteria if matched | **NOT APPLICABLE** | Final study is not a matched case-control design. |
| RECORD 6.1 | List codes/algorithms used for population selection in detail | **READY/PARTIAL** | Repository contains deterministic audit rules plus physician Gold workflow. Main paper should describe broad “舟骨” retrieval, physician anatomy adjudication, state criteria, and operative relevance; technical rules can be Supplementary. |
| RECORD 6.2 | Report validation of codes/algorithms | **PARTIAL** | Physician reference standard is designed but not complete. After Gold, report agreement/accuracy only for measurement methods actually relied upon. |
| RECORD 6.3 | Show linkage/selection process graphically if relevant | **BLOCKED** | Final Figure 1 will show 88 broad candidates -> physician anatomy -> state -> detailed note -> target-disease operation -> final groups. |

## Final participant-flow logic to report

The final main-text flow should be physician-defined, not deterministic-rule-defined:

```text
88 broad scaphoid candidate admissions
    -> physician anatomy adjudication
       -> physician-confirmed wrist scaphoid
          -> physician state adjudication
             -> acute/new
             -> established chronic/nonunion
             -> insufficient/uncertain
          -> detailed operative-note module available
             -> target-disease procedure yes/no/uncertain
                -> final acute/new operative group
                -> final chronic/nonunion operative group
```

The deterministic 68/13/7 audit belongs in Supplementary or measurement-robustness reporting, not as the final participant definition.

---

# Methods — routinely collected data source and linkage

| RECORD item | Requirement | Current status | Manuscript action |
|---|---|---|---|
| RECORD 12.1 | Describe investigators’ access to the data source | **PARTIAL** | State that investigators received a fixed export rather than direct unrestricted access to the live HIS/EMR. This explains why no additional local fields/follow-up can be retrieved. |
| RECORD 12.2 | Describe data cleaning | **READY/PARTIAL** | Repository documents duplicate diagnosis rows, one-to-many module structure, anatomy disambiguation, procedure attribution, range checks, and structural missingness. Condense into Methods; detailed audit in Supplementary. |
| RECORD 12.3 | Describe person-level/data linkage | **PARTIAL** | State explicitly that hospital modules were deterministically linked at the admission-episode level using the supplied admission identifier. Report that raw one-to-many diagnosis/lab/operation rows were not treated as independent patients. |

## Required data-linkage wording

Suggested Methods concept:

> “Records from diagnostic, presenting-complaint/physical-examination, and operative exports were linked deterministically using the supplied admission-episode identifier. Because the source exports contained one-to-many diagnosis and procedure rows, analyses were constructed at the admission-episode level; repeated source rows were retained as child records or aggregated features rather than counted as independent observations.”

## Pseudoreplication issue that must be reported

The raw basic/diagnostic exports previously showed approximately:

- hallux: 10.85 rows/admission;
- CMC: 12.40 rows/admission;
- scaphoid: 13.40 rows/admission.

Only scaphoid is relevant to the main manuscript. The exact scaphoid diagnostic-row inflation can be mentioned in Supplementary as evidence for why patient/admission-level reconstruction was necessary.

---

# Methods — variables and measurement

| Guideline item | Requirement | Current status | Manuscript action |
|---|---|---|---|
| STROBE 7 | Define exposures, outcomes, confounders, diagnostic criteria | **READY** | Current plan clearly defines established chronic/nonunion, acute/new, bone graft, fixation, augmentation composite, duration. |
| STROBE 8 | Give source and assessment method for each variable | **PARTIAL** | Add a compact source-to-variable table in Supplementary or Methods. |
| RECORD 6.1/6.2 | Explain free-text/code-based definitions and validation | **PARTIAL** | State which source text physician reviewers see and which text is prohibited for exposure assignment. |

## Source-to-variable map for final paper

| Variable | Source data | Final measurement |
|---|---|---|
| wrist-scaphoid anatomy | diagnosis, complaint/exam, operation/anatomical context for Stage 1 | physician adjudication |
| clinical state | diagnosis + complaint + physical examination only | physician adjudication |
| relevant duration | diagnosis + complaint + physical examination | physician value/unit/basis adjudication |
| target-disease operation | detailed operative note + operation name | physician procedure-relevance adjudication |
| internal fixation | disease-concordant operative note | physician component adjudication |
| bone graft | disease-concordant operative note | physician component adjudication |
| reconstruction/fusion | disease-concordant operative note | physician component adjudication |
| age/sex/BMI | structured basic-information export | episode-level structured fields; BMI range checked |

Critical design statement:

> Operation text is excluded from clinical-state assignment because operative treatment is the downstream variable of interest.

---

# Methods — bias

| Guideline item | Requirement | Current status | Manuscript action |
|---|---|---|---|
| STROBE 9 | Explain efforts to address bias | **READY/PARTIAL** | Several biases are already recognized; consolidate them into one Methods subsection. |
| RECORD 19.1 | Discuss biases from routine data | **PARTIAL** | Must explicitly discuss misclassification, unmeasured confounding, missingness, and changing data availability over time. |

## Biases that should be named explicitly

### 1. Anatomical misclassification

Broad “舟骨” terminology can retrieve wrist scaphoid and foot navicular records.

Mitigation:

- all 88 broad candidates receive physician anatomy adjudication before downstream cohort definition.

### 2. Verification bias

Risk: reviewing state/procedure only within deterministic wrist-rule positives would allow the rule to define the clinical cohort.

Mitigation:

- Stage 1 physician review covers all 88 broad candidates;
- downstream Stage 2 is generated from physician-confirmed anatomy Gold.

### 3. Procedure-attribution bias

Risk: a detailed operative note in a scaphoid admission may describe treatment of another anatomical problem.

Mitigation:

- target-disease procedure relevance adjudicated before fixation/graft labels;
- unrelated operations do not enter clinical procedure denominators.

### 4. Information/documentation bias

Routine documentation was not collected prospectively for this research question; absence of a phrase does not necessarily equal absence of a clinical feature.

Mitigation:

- physician `uncertain` categories retained;
- missing/uncertain are not silently recoded as negative;
- main state comparison uses explicit physician-confirmed acute/new versus established chronic/nonunion.

### 5. Structural data-availability bias over time

The supplied export has a module discontinuity around 2019-2022 and detailed disease-concordant scaphoid operative records currently occur in 2023-2025.

Mitigation/reporting:

- do not impute structurally absent modules;
- describe the effective operative study period transparently;
- do not present earlier years as an independent validation cohort.

### 6. Residual confounding by disease severity and surgeon preference

Important variables such as standardized displacement, proximal-pole vascularity, humpback deformity, bone defect size, cystic change and CT geometry are incompletely captured.

Implication:

- association cannot be interpreted as causal treatment selection;
- no multivariable “adjustment” should be used to imply those missing severity variables have been controlled.

### 7. Hypothesis-generation bias / same-dataset discovery

The primary bone-graft hypothesis was generated from deterministic exploration of the same fixed dataset.

Mitigation/reporting:

- describe the work as exploratory/hypothesis-generating;
- physician Gold and primary outcome hierarchy were frozen before final effect scoring;
- maintain the analysis changelog;
- do not present final P value as independent confirmation.

---

# Methods — study size

| Guideline item | Requirement | Current status | Manuscript action |
|---|---|---|---|
| STROBE 10 | Explain how study size was arrived at | **PARTIAL** | Add a direct fixed-data statement; do not invent a power calculation. |

### Required study-size statement

> “The study size was determined by the complete fixed hospital export available for the prespecified broad scaphoid retrieval. No prospective sample-size target or post-hoc power-based inclusion rule was used.”

The final operative denominator will be determined entirely by physician anatomy/state/procedure Gold.

---

# Methods — quantitative variables

| Guideline item | Requirement | Current status | Manuscript action |
|---|---|---|---|
| STROBE 11 | Explain treatment of quantitative variables and cut points | **READY** | Duration is continuous in days; no local cutoff optimization. Age/BMI reported continuously/descriptively. |

Duration rules:

- physician enters original value + unit;
- analysis converts with fixed units;
- continuous median/IQR + Mann-Whitney;
- no threshold selected to maximize significance;
- any one-year descriptive split must be literature-anchored and secondary.

---

# Methods — statistical analysis and missingness

| Guideline item | Requirement | Current status | Manuscript action |
|---|---|---|---|
| STROBE 12a | Describe statistical methods | **READY** | Fisher exact, conditional OR/95% CI, Mann-Whitney, leave-one-out are frozen. |
| STROBE 12b | Subgroups/interactions | **READY** | Duration analysis is explicitly secondary within chronic/nonunion. No broad interaction search. |
| STROBE 12c | Missing data | **PARTIAL** | Add explicit variable-specific denominator language. |
| STROBE 12d | Matching/follow-up treatment | **NOT APPLICABLE** | No matched design and no longitudinal outcome analysis. |
| STROBE 12e | Sensitivity analyses | **READY** | Leave-one-out, augmentation composite, deterministic-vs-Gold measurement robustness, injury-basis duration. |
| RECORD 12.2 | Cleaning of duplicate/repeated/missing data | **READY/PARTIAL** | Explain admission-level reconstruction, duplicate diagnosis rows, range checks, and structural missingness. |

## Missing-data rules to report

1. No imputation for structurally absent EHR modules.
2. `insufficient_or_uncertain` state excluded from state-based clinical comparison.
3. Procedure relevance `no/uncertain` excluded from treatment-composition denominator.
4. A procedure component labelled `uncertain` is excluded from that component’s evaluable denominator and is not coded `no`.
5. BMI/sex/other structured variables report explicit available denominators.
6. Missing duration excludes the record only from the duration secondary analysis, not from the primary treatment-composition analysis.

---

# Results — participant flow

| Guideline item | Requirement | Current status | Manuscript action |
|---|---|---|---|
| STROBE 13a/b | Numbers at each stage and reasons for exclusion | **BLOCKED** | Complete after physician Gold. |
| STROBE 13c | Consider a flow diagram | **BLOCKED** | Final Figure 1 generator already exists. |
| RECORD 13.1 | Detailed person selection including data-quality/availability filters | **BLOCKED/PARTIAL** | Final Figure 1 plus Methods text must report anatomy, state uncertainty, detailed-note availability, and procedure relevance. |

Final Figure 1 should contain the physician-defined clinical flow only. Deterministic audit flow belongs in Supplementary.

---

# Results — descriptive data and outcomes

| Guideline item | Requirement | Current status | Manuscript action |
|---|---|---|---|
| STROBE 14a | Participant characteristics | **BLOCKED** | Final Table 1 builder ready; requires Gold. |
| STROBE 14b | Missing data for variables | **BLOCKED** | Include evaluable denominators in Table 1/Table 2. |
| STROBE 14c | Follow-up time for cohorts | **NOT APPLICABLE** | No longitudinal outcome analysis. |
| STROBE 15 | Outcome/exposure category data | **BLOCKED** | Table 2 will report graft/fixation n/N. |
| STROBE 16a | Effect estimates and precision | **BLOCKED** | Conditional OR + 95% CI + Fisher P after Gold. |
| STROBE 16b | Boundaries for categorized continuous variables | **READY** | No locally derived duration category used in primary analysis. |
| STROBE 17 | Other analyses | **BLOCKED** | Leave-one-out and duration results inserted after Gold. |

---

# Discussion

| Guideline item | Requirement | Current status | Manuscript action |
|---|---|---|---|
| STROBE 18 | Summarize key results relative to objectives | **BLOCKED** | Final language depends on Gold effect. |
| STROBE 19 | Discuss limitations and direction/magnitude of bias | **PARTIAL** | v0.4 has limitations; strengthen directionality where possible. |
| RECORD 19.1 | Discuss use of data not created for the research question | **PARTIAL** | Add explicit paragraph on routine EHR documentation, structural missingness, misclassification and unmeasured severity. |
| STROBE 20 | Cautious overall interpretation | **READY/PARTIAL** | Current claim boundaries are appropriately non-causal. |
| STROBE 21 | Generalizability | **PARTIAL** | State that single-centre, documentation-specific and 2023-2025 operative concentration limit transportability. |

### Direction-of-bias examples worth stating

- Incomplete documentation of graft or state could attenuate or distort group differences rather than simply reduce precision.
- Exclusion of records without detailed disease-concordant operative notes creates a selected operative subset and limits inference to documented operations, not all wrist-scaphoid patients.
- Missing standardized severity variables can create confounding by indication; a larger observed graft association cannot be interpreted as an independent effect of chronicity.

---

# Other information

| Guideline item | Requirement | Current status | Manuscript action |
|---|---|---|---|
| STROBE 22 | Funding and funder role | **BLOCKED** | Add actual funding/source information before submission. Do not leave generic wording. |
| RECORD data/code transparency | Explain availability of codes/algorithms/data | **PARTIAL** | Public code and aggregate artifacts are available in GitHub; raw clinical data cannot be public because of privacy/ethics. Add final Data Availability statement consistent with ethics approval. |
| Ethics | Approval/waiver and governance | **BLOCKED** | v0.4 still has an ethics placeholder. Insert actual IRB/ethics committee name, approval number and consent/waiver status. Never infer or invent these. |
| Conflicts | Journal-required disclosure | **BLOCKED** | Complete at submission. |

---

# Submission-critical blockers

The manuscript should **not** be submitted until the following are complete:

1. physician Stage-1 anatomy review, Reviewer-2 review and adjudication;
2. Stage-1 Gold freeze;
3. Stage-2 state/duration/procedure review and adjudication;
4. final reference-standard SHA-256 freeze;
5. final post-Gold analysis using `analyze_scaph_gold_v0_2.py`;
6. final Figure 1-3 generation;
7. final Table 1, Table 2 and duration supplementary table generation;
8. actual ethics/IRB information;
9. actual funding/conflict statements;
10. final target-journal author-instruction check;
11. final STROBE/RECORD checklist with manuscript page numbers.

---

# Items that can be completed now, before Gold

1. strengthen Methods wording for routine EHR data access and cleaning;
2. explicitly describe admission-level deterministic linkage across export modules;
3. add fixed-data study-size rationale;
4. add the structural 2019-2022 data-availability discontinuity to Methods/Limitations;
5. write the final missing-data policy into the manuscript;
6. prepare Data Availability wording subject to ethics approval;
7. prepare STROBE/RECORD submission checklist shell;
8. keep all deterministic audit results clearly labeled pre-validation or move them to Supplementary.

---

# Recommended reporting identity of the paper

The cleanest reporting identity is:

> **A retrospective observational study using routinely collected hospital EHR data, with a two-stage physician reference standard and a focused analysis of operative treatment composition across wrist-scaphoid presentation states.**

Do not label the main article as an AI framework paper, a predictive-model study, a comparative-effectiveness trial, or a longitudinal nonunion-outcome study.
