# Focused Scaphoid Analysis Plan v0.2

**Status:** frozen before completion of physician Stage-2 Gold  
**Study type:** retrospective fixed-data exploratory comparative study  
**Scientific orientation:** problem-first; computational text processing is measurement only

## 1. Primary scientific question

Among physician-confirmed wrist-scaphoid admissions with disease-concordant detailed operative documentation, is an **established chronic/nonunion** presentation associated with greater use of **bone-graft augmentation**, while internal fixation remains common across presentation groups?

The study evaluates documented operative composition. It does not evaluate future nonunion risk, postoperative union, treatment efficacy, or causal treatment selection.

## 2. Two-stage physician-defined cohort

### Stage 1 — anatomy

All 88 broad scaphoid candidates undergo blinded physician anatomy review:

- `wrist_scaphoid`;
- `foot_navicular`;
- `other`;
- `uncertain`.

The final wrist-scaphoid cohort is defined from the **adjudicated physician anatomy Gold**, not from deterministic-rule positivity.

### Stage 2 — state and procedure

Only after Stage-1 Gold is frozen are downstream review packets generated for physician-confirmed wrist-scaphoid records.

Clinical state is assigned from diagnosis, complaint and physical examination only:

- `acute_or_new_fracture`;
- `established_chronic_fracture`;
- `established_nonunion`;
- `chronic_nonunion_not_distinguishable`;
- `insufficient_or_uncertain`.

For records with detailed operative documentation, physicians independently assess whether the documented operation treats the wrist scaphoid and, when relevant, label fixation, graft, reconstruction and fusion.

Reviewer-1, Reviewer-2 and final adjudicated Gold files are preserved separately. Final inferential analysis uses only the adjudicated Gold.

## 3. Exposure definition

The primary exposure group combines:

- established chronic fracture;
- established nonunion;
- chronic/nonunion not distinguishable.

The main comparison group comprises other sufficiently classifiable physician-confirmed wrist-scaphoid records. `insufficient_or_uncertain` states are excluded from the relevant inferential comparison.

Operative text is prohibited from assigning exposure state.

## 4. Operative analysis population

A record enters the operative analysis only if all of the following are satisfied:

1. physician-confirmed wrist scaphoid;
2. sufficiently classifiable clinical state;
3. detailed operative-note module available;
4. physician-adjudicated `target_disease_procedure_present = yes`.

A missing detailed note is not coded as no surgery. A detailed note for another anatomical problem is not coded as wrist-scaphoid surgery.

The deterministic pre-validation audit currently contains 28 disease-concordant operative records, all from 2023-2025. Final denominators will be regenerated from physician Gold and are not assumed in advance.

## 5. Primary outcome

### Bone-graft augmentation

Binary physician-adjudicated target-disease operative component.

`yes` requires explicit documentation of bone graft or bone harvest used as part of the wrist-scaphoid operation.

This primary outcome was frozen before Stage-2 physician scoring and is not replaced by a composite based on the eventual P value.

## 6. Key contrast outcome

### Internal fixation

Binary physician-adjudicated target-disease component including screw, headless/cannulated screw, wire, or other explicit fixation.

The intended scientific contrast is a possible dissociation:

- fixation remains a common mechanical base across groups;
- graft augmentation changes with established chronic/nonunion presentation.

## 7. Secondary operative outcomes

1. graft/reconstruction/fusion augmentation composite;
2. number of major procedure components among fixation, graft, reconstruction and fusion;
3. individual reconstruction/fusion components, reported descriptively when sparse.

Secondary outcomes remain secondary regardless of statistical significance.

## 8. Prespecified duration secondary hypothesis

A separate exploratory hypothesis is frozen in `SCAPHOID_DURATION_SECONDARY_HYPOTHESIS_V0_1.md`.

Within physician-confirmed established chronic/nonunion operative records, test whether records receiving bone-graft augmentation have a longer explicitly documented wrist-related injury/symptom duration.

### Physician duration variable

Stage-2 state review records:

- `gold_relevant_duration_present = yes / no / uncertain`;
- numeric duration value;
- unit: hours / days / weeks / months / years;
- basis: `injury_since_event / wrist_symptom_duration / both / uncertain`.

If more than one duration appears, the reviewer records the longest clearly wrist-scaphoid-related index injury or symptom duration present at admission. Automated parser output is not shown to the reviewer.

### Duration analysis

- restricted to established chronic/nonunion records with disease-concordant operative documentation and physician-valid duration;
- duration converted to days using fixed unit conversions;
- summarize median, IQR and available denominator by graft group;
- compare graft-positive versus graft-negative records with Mann-Whitney U;
- visualize on a log time scale if useful;
- no data-derived cutoff search;
- no replacement of the primary bone-graft comparison.

An injury-duration-only sensitivity analysis may exclude symptom-only durations if both groups retain interpretable data.

## 9. Main statistical analysis

### Descriptive variables

Report age, sex and BMI with actual denominators. Continuous variables use median (IQR) unless distribution and scale justify mean (SD).

### Primary bone-graft comparison

Construct a 2×2 table of:

`established chronic/nonunion × bone graft yes/no`.

Report:

- n/N (%);
- Fisher exact P value;
- crude odds ratio;
- 95% confidence interval.

### Internal-fixation contrast

Analyze with the same sparse-table approach.

### Component count

Report median (IQR) and compare with Mann-Whitney U as secondary analysis.

### Multivariable modelling

No routine adjusted model is prespecified for the small operative sample. High-capacity machine learning is excluded from the primary clinical analysis. A sparse-data adjusted model may be considered only if final physician Gold produces a defensible event count and covariate set; it cannot replace the unadjusted primary analysis.

## 10. Prespecified robustness analyses

1. chronic/nonunion versus the full sufficiently classifiable comparison group;
2. **acute-only sensitivity:** chronic/nonunion versus physician-confirmed `acute_or_new_fracture` only;
3. exclusion of uncertain procedure relevance;
4. primary bone-graft outcome versus broader augmentation composite;
5. leave-one-out influence analysis for the primary 2×2 table;
6. exclusion of records with competing same-admission orthopaedic procedures;
7. deterministic pre-validation result versus physician-adjudicated result as a measurement-robustness comparison;
8. duration secondary analysis with injury-only durations when feasible.

No robustness analysis may be promoted to the primary result solely because it yields a smaller P value.

## 11. Inter-rater reliability and adjudication

Approximately 20% of each review layer is independently reviewed by Reviewer 2 using a prespecified hash-based sample.

Reviewer-1 and Reviewer-2 labels are retained unchanged. Separate adjudication templates are generated:

- agreement → agreed label copied to final Gold;
- no second review → Reviewer-1 label copied to final Gold;
- disagreement → final Gold left blank until adjudicator review.

Agreement statistics are calculated before final adjudication. Final clinical analyses use the adjudicated files only.

## 12. Reference-standard freezing

Stage-1 and final physician reference standards are validated with `freeze_scaph_reference_v0_1.py`.

The validator checks:

- all 88 Stage-1 candidate IDs retained;
- Reviewer-2 IDs match prespecified manifests;
- Stage-2 state IDs exactly equal physician-confirmed wrist-scaphoid IDs;
- procedure IDs are a subset of physician-confirmed wrist-scaphoid IDs;
- controlled vocabulary and duration consistency;
- final adjudicated files are complete;
- SHA-256 hashes for all private reference files.

Only hashes and row counts are eligible for the public manifest.

## 13. Missingness and ambiguity

- undocumented state is not coded as acute;
- undocumented duration is not coded as zero;
- missing operative-note module is not coded as no procedure;
- unrelated same-admission operation is not coded as target-disease treatment;
- ambiguous anatomy/state/procedure relevance is retained as uncertainty until physician adjudication.

## 14. Claim boundary

The strongest permitted clinical statement after validation is:

> Established chronic/nonunion wrist-scaphoid presentations were associated with greater use of bone-graft augmentation among documented target-disease operations, while internal fixation remained common across presentation groups.

If the duration secondary signal persists:

> Within established chronic/nonunion operative presentations, graft augmentation was concentrated among records with longer documented wrist-related disease duration.

Neither statement implies causality or treatment benefit.
