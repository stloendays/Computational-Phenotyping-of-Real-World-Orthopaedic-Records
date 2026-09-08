# Focused Scaphoid Analysis Plan v0.3

**Current analysis plan for the main manuscript.**  
**Frozen before completion of physician Stage-2 Gold.**  
**Primary outcome unchanged: bone-graft augmentation.**

## 1. Study question

Among physician-confirmed wrist-scaphoid admissions with disease-concordant detailed operative documentation, is an **established chronic/nonunion** presentation associated with greater use of **bone-graft augmentation** than a **physician-confirmed acute/new fracture** presentation, while internal fixation remains common in both groups?

The study is retrospective, fixed-data, exploratory, and problem-first. Computational text processing is a measurement aid rather than the scientific objective.

## 2. Comparison-definition correction before Gold scoring

The physician state vocabulary is:

1. `acute_or_new_fracture`;
2. `established_chronic_fracture`;
3. `established_nonunion`;
4. `chronic_nonunion_not_distinguishable`;
5. `insufficient_or_uncertain`.

The earlier draft plan described a broad sufficiently classifiable comparison group plus a separate `acute-only` sensitivity analysis. Under this physician vocabulary, every sufficiently classifiable state outside the established chronic/nonunion group is necessarily `acute_or_new_fracture`. Therefore the two planned comparison sets would be identical after Gold adjudication.

This logical redundancy was identified **before Stage-2 physician Gold was completed and before any physician-adjudicated treatment effect was inspected**.

Accordingly:

- the primary comparison is now **established chronic/nonunion versus physician-confirmed acute/new fracture**;
- `insufficient_or_uncertain` state records are excluded from state-based clinical inference;
- there is no separate acute-only sensitivity analysis.

The primary endpoint itself has not changed.

## 3. Cohort construction

### Stage 1 — physician anatomy

All 88 broad scaphoid candidates undergo blinded physician anatomy adjudication:

- wrist scaphoid;
- foot navicular;
- other;
- uncertain.

The final wrist-scaphoid cohort is defined by adjudicated physician anatomy Gold, not deterministic-rule positivity. The Stage-1 input population was frozen before annotation by SHA-256 while all anatomy Gold fields were blank.

### Stage 2 — generated after anatomy freeze

After Stage-1 anatomy adjudication, downstream review packets are generated only for physician-confirmed wrist-scaphoid records.

Stage 2 contains:

- clinical-state review for every physician-confirmed wrist record;
- physician-adjudicated wrist-related duration fields;
- procedure relevance/components for physician-confirmed wrist records with detailed operative documentation.

Final Stage-2 sample sizes are therefore not prespecified to equal the deterministic 68/31 counts.

Reviewer-1, Reviewer-2 and final adjudicated Gold files remain separate so inter-rater agreement can be reconstructed after adjudication.

## 4. Clinical-state groups

State is adjudicated from diagnosis, complaint, and physical examination only. Operative text is prohibited from assigning clinical state.

### Established chronic/nonunion exposure group

Combine:

- established chronic fracture;
- established nonunion;
- chronic/nonunion not distinguishable.

### Acute/new comparison group

Use only:

- acute/new fracture.

### Excluded from state-based inference

- insufficient/uncertain.

These records remain available for measurement-validation summaries but do not enter the primary clinical 2x2 analysis.

## 5. Operative attribution

A record enters the operative analysis only when:

1. physician-confirmed wrist scaphoid;
2. physician-confirmed established chronic/nonunion or acute/new fracture state;
3. a detailed operative-note module exists;
4. adjudicated `target_disease_procedure_present = yes`.

Missing detailed note is not coded as no surgery. A detailed note concerning another anatomical problem is not coded as target-disease surgery.

## 6. Primary outcome

### Bone-graft augmentation

Physician-adjudicated binary outcome indicating explicit bone graft or bone harvest used as part of the wrist-scaphoid operation.

This outcome was frozen before physician-reference scoring and cannot be replaced by a composite because another analysis yields a smaller P value.

## 7. Key contrast outcome

### Internal fixation

Physician-adjudicated target-disease fixation including screw, headless/cannulated screw, wire, or other explicit internal fixation.

The scientific pattern under test is:

- fixation remains a common mechanical base in both presentation states;
- graft augmentation is the component that increases in established chronic/nonunion presentations.

## 8. Secondary treatment outcomes

1. graft/reconstruction/fusion augmentation composite;
2. number of major components among fixation, graft, reconstruction, and fusion;
3. individual reconstruction/fusion components when sample size permits descriptive reporting.

These remain secondary regardless of P value.

## 9. Secondary mechanistic hypothesis: documented duration

A pre-validation audit performed after the primary question was selected identified a duration gradient within deterministic chronic/nonunion operative records.

Current deterministic signal:

- graft present: duration available 7/8, median 182.6 days [Q1 167.4, Q3 1004.4];
- graft absent: duration available 6/7, median 15.0 days [Q1 2.3, Q3 41.0].

This is explicitly post-primary, exploratory, and secondary. It does not change the primary endpoint.

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
- distribution plot on a log-scaled duration axis when useful.

No locally optimized duration cutoff is permitted. A `>=1 year` split may be shown only as a literature-anchored descriptive sensitivity analysis retained independently of the local effect.

## 10. Baseline descriptors

Report by adjudicated operative presentation group:

- age;
- sex;
- BMI;
- clearly documented preoperative severity descriptors when sufficiently complete.

Missing denominators are explicit.

## 11. Primary statistical analysis

For bone graft, construct:

| | Bone graft yes | Bone graft no |
|---|---:|---:|
| Established chronic/nonunion | a | b |
| Acute/new fracture | c | d |

Report:

- n/N (%);
- Fisher exact two-sided P value;
- crude odds ratio;
- 95% confidence interval when estimable without an unplanned correction.

Internal fixation is analyzed with the same sparse-table approach as the prespecified key contrast.

No continuity correction is silently applied to zero-cell tables. If a finite crude OR/CI is unavailable, the sparse table and Fisher P value are reported rather than introducing an unplanned correction.

No routine high-dimensional multivariable model is prespecified for the small operative sample.

## 12. Secondary statistical analyses

### Major procedure-component count

- median (IQR);
- Mann-Whitney U.

### Duration within established chronic/nonunion

Compare graft-positive versus graft-negative records with valid physician duration:

- available-duration denominator;
- median (IQR);
- Mann-Whitney U;
- log-scale display if useful.

An injury-duration-only analysis may be reported as a sensitivity check if both graft groups retain interpretable data.

## 13. Robustness analyses

1. exclusion of uncertain procedure relevance, with exclusion flow reported explicitly;
2. primary bone-graft outcome versus broader augmentation composite;
3. leave-one-out influence analysis for the primary 2x2 table;
4. exclusion of records with competing same-admission orthopaedic procedures;
5. deterministic pre-validation effect versus physician-adjudicated effect as measurement robustness;
6. secondary duration analysis restricted to injury-based durations when feasible.

There is **no separate acute-only sensitivity analysis**, because physician-confirmed acute/new fracture is now the primary comparison definition.

No secondary or robustness analysis can replace the primary result solely because it yields a smaller P value.

## 14. Inter-rater reliability and adjudication

Approximately 20% of each review layer is independently reviewed by Reviewer 2 using a prespecified hash-based sample.

Reviewer-1 and Reviewer-2 labels remain unchanged. Separate adjudication templates are generated:

- agreement -> agreed label copied to Gold;
- no second review -> Reviewer-1 copied to Gold;
- disagreement -> Gold blank until adjudicator review.

Agreement statistics are calculated before final adjudication. Final clinical analysis uses adjudicated Gold only.

## 15. Reference-standard freezing

`freeze_scaph_reference_v0_1.py` validates Stage-1 and final two-stage Gold, including:

- all 88 Stage-1 candidate IDs retained;
- Reviewer-2 IDs matching prespecified manifests;
- Stage-2 state IDs exactly matching physician-confirmed wrist IDs;
- procedure IDs restricted to physician-confirmed wrist IDs;
- controlled vocabulary and duration consistency;
- adjudicated state/procedure population consistency;
- SHA-256 hashes for private reference files.

## 16. Interpretation boundary

The strongest permitted primary statement after successful validation is:

> Established chronic/nonunion wrist-scaphoid presentations were associated with greater use of bone-graft augmentation than physician-confirmed acute/new fracture presentations among documented target-disease operations, while internal fixation remained common in both groups.

If the duration signal persists:

> Within established chronic/nonunion operative presentations, graft augmentation was concentrated among records with longer documented wrist-related disease duration.

Neither statement establishes causality, treatment benefit, or a clinical graft threshold.
