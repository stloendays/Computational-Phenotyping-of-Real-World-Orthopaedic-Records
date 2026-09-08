# Focused Scaphoid Analysis Plan v0.3

**Current analysis plan for the main manuscript.**  
**Primary question unchanged.**  
**Secondary duration hypothesis added before Stage-2 physician adjudication.**

## 1. Study question

Among physician-confirmed wrist-scaphoid admissions with disease-concordant detailed operative documentation, is an established chronic/nonunion presentation associated with **bone-graft augmentation**, while internal fixation remains common across phenotype groups?

The study is retrospective, fixed-data, exploratory, and problem-first. Computational text processing is a measurement aid rather than the scientific objective.

## 2. Cohort construction

### Stage 1 — physician anatomy

All 88 broad scaphoid candidates undergo blinded physician anatomy adjudication:

- wrist scaphoid;
- foot navicular;
- other;
- uncertain.

The final wrist-scaphoid cohort is defined by physician anatomy Gold, not deterministic-rule positivity.

The Stage-1 input population was frozen before annotation by SHA-256 while all anatomy Gold fields were blank.

### Stage 2 — generated after anatomy freeze

After Stage-1 anatomy adjudication, downstream review packets are generated only for physician-confirmed wrist-scaphoid records.

Stage 2 contains:

- clinical-state review for every physician-confirmed wrist record;
- physician-adjudicated wrist-related duration fields;
- procedure relevance/components for physician-confirmed wrist records with detailed operative documentation.

Final Stage-2 sample sizes are therefore not prespecified to equal the deterministic 68/31 counts.

## 3. Clinical-state exposure

State is adjudicated from diagnosis, complaint, and physical examination only:

1. acute/new fracture;
2. established chronic fracture;
3. established nonunion;
4. chronic/nonunion not distinguishable;
5. insufficient/uncertain.

Primary exposure group:

- established chronic fracture;
- established nonunion;
- chronic/nonunion not distinguishable.

The main comparison group contains other sufficiently classifiable physician-confirmed wrist-scaphoid records. Uncertain state is excluded from the relevant inferential comparison.

A prespecified sensitivity analysis restricts the comparison group to physician-confirmed acute/new fractures only.

## 4. Operative attribution

For each physician-confirmed wrist-scaphoid record with a detailed operative module, reviewers first assign:

`target_disease_procedure_present = yes / no / uncertain`.

Only disease-concordant wrist-scaphoid operative records contribute to treatment-composition inference.

## 5. Primary outcome

### Bone-graft augmentation

Physician-adjudicated binary outcome indicating explicit bone graft/harvest used as part of the wrist-scaphoid operation.

This outcome was frozen before physician-reference scoring and cannot be replaced by a composite because another analysis yields a smaller P value.

## 6. Key contrast outcome

### Internal fixation

Physician-adjudicated target-disease fixation including screw, headless/cannulated screw, wire, or other explicit internal fixation.

The scientific pattern being tested is:

- fixation remains common across phenotype groups;
- graft augmentation increases in established chronic/nonunion presentations.

## 7. Secondary treatment outcomes

1. graft/reconstruction/fusion augmentation composite;
2. number of major components among fixation, graft, reconstruction, and fusion;
3. individual reconstruction/fusion components when sample size permits descriptive reporting.

These remain secondary regardless of their P values.

## 8. Secondary mechanistic hypothesis: documented duration

A pre-validation audit performed after the primary question was selected identified a duration gradient within deterministic chronic/nonunion operative records.

Current deterministic signal:

- graft present: duration available 7/8, median 182.6 days [Q1 167.4, Q3 1004.4];
- graft absent: duration available 6/7, median 15.0 days [Q1 2.3, Q3 41.0].

This is explicitly **post-primary, exploratory, and secondary**. It does not change the primary endpoint.

### Physician duration fields

Stage-2 state review collects:

- `gold_relevant_duration_present = yes / no / uncertain`;
- `gold_relevant_duration_value`;
- `gold_relevant_duration_unit = hours / days / weeks / months / years`;
- `gold_duration_basis = injury_since_event / wrist_symptom_duration / both / uncertain`.

Reviewers record the longest clearly wrist-scaphoid-related index injury or symptom duration documented at admission. Automated parser output is hidden from reviewers.

### Duration analysis population

Restricted to records meeting all of the following:

1. physician-confirmed wrist scaphoid;
2. physician-confirmed established chronic/nonunion;
3. disease-concordant detailed operative record;
4. physician-adjudicated bone-graft yes/no;
5. physician-confirmed relevant duration.

Records missing a relevant duration remain in the primary treatment-composition analysis but are excluded from this secondary duration analysis.

### Duration statistics

Duration is converted to days after physician adjudication using fixed unit conversions and analyzed continuously.

Report:

- available-duration denominator by graft group;
- median and IQR;
- Mann-Whitney U test;
- distribution plot on a log-scaled duration axis when graphically useful.

No multivariable or predictive model is prespecified for the duration analysis because the sample is expected to be very small.

### No local threshold optimization

No cutoff is selected by maximizing local significance, AUROC, Youden index, or classification accuracy.

A `>=1 year` split may be shown only as a literature-anchored descriptive sensitivity analysis if retained before physician outcome inspection. The continuous-duration comparison remains primary for this secondary hypothesis.

## 9. Baseline descriptors

Report by physician-adjudicated operative phenotype group:

- age;
- sex;
- BMI;
- clearly documented preoperative severity descriptors when sufficiently complete.

Missing denominators are explicit.

## 10. Primary statistical analysis

### Bone graft

- 2x2 table;
- Fisher exact test;
- crude odds ratio;
- 95% confidence interval.

### Internal fixation

- Fisher exact test;
- crude odds ratio;
- 95% confidence interval.

No routine high-dimensional multivariable model is prespecified for the small operative sample.

## 11. Robustness analyses

1. primary physician-defined chronic/nonunion vs full classifiable comparison group;
2. chronic/nonunion vs physician-confirmed acute/new fractures only;
3. exclusion of uncertain procedure relevance;
4. primary bone-graft outcome vs broader augmentation composite;
5. leave-one-out influence analysis for the primary 2x2 association;
6. exclusion of records with competing same-admission orthopaedic procedures;
7. deterministic pre-validation effect vs physician-adjudicated effect as measurement robustness;
8. secondary duration analysis using physician-adjudicated duration only.

Because the supplied detailed operative records are concentrated in 2023-2025, historical detailed-procedure replication is unavailable.

## 12. Multiplicity and claim hierarchy

The hierarchy is fixed as:

1. primary: chronic/nonunion presentation -> bone-graft augmentation;
2. key contrast: internal fixation;
3. secondary: augmentation composite/component count;
4. secondary mechanistic: duration within chronic/nonunion -> graft augmentation;
5. sensitivity: acute-only, leave-one-out, competing-procedure exclusion.

The duration analysis cannot become the primary endpoint based on its P value.

## 13. Interpretation boundary

The study may establish associations between presentation state, documented disease duration, and operative composition.

It cannot establish:

- future nonunion risk;
- postoperative union or healing time;
- treatment efficacy;
- causal treatment selection;
- a clinical duration threshold at which grafting should be performed;
- superiority of any graft technique.
