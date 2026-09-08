# Scaphoid Duration Secondary Hypothesis v0.1

**Status:** exploratory secondary hypothesis frozen after the primary bone-graft question, but before physician Stage-2 adjudication  
**Primary outcome remains unchanged:** bone-graft augmentation by established chronic/nonunion versus comparison presentation

## 1. Rationale

The primary study asks whether established chronic/nonunion wrist-scaphoid presentation is associated with increased bone-graft augmentation while internal fixation remains common across phenotype groups.

A subsequent pre-validation audit identified a potentially more mechanistic signal **within the established chronic/nonunion operative subset**: records with deterministic bone-graft use tended to contain substantially longer explicitly documented wrist injury/symptom durations than records without deterministic graft use.

This secondary hypothesis is intentionally frozen as exploratory. It does **not** replace the primary analysis and is not selected because its preliminary P value is smaller.

## 2. Current deterministic observation

Within the current deterministic established chronic/nonunion disease-concordant operative subset:

- bone graft present: 8 operative records; explicit relevant duration recoverable in 7;
- bone graft absent: 7 operative records; explicit relevant duration recoverable in 6.

Corrected duration parsing gives:

- graft-present duration median: **182.6 days** (Q1 167.4, Q3 1004.4);
- graft-absent duration median: **15.0 days** (Q1 2.3, Q3 41.0).

These are algorithm-derived pre-validation observations. The duration parser was explicitly corrected for Chinese half-unit expressions such as `1个半月`, `半年`, and `1年半`; earlier uncorrected estimates are superseded.

Public aggregate: `data/aggregate/scaphoid_duration_signal_v0_1.csv`.

## 3. Secondary scientific question

> **Within physician-confirmed established chronic/nonunion wrist-scaphoid operative records, is bone-graft augmentation associated with a longer explicitly documented wrist-related injury or symptom duration?**

This question is narrower than the primary chronic/nonunion-versus-comparison analysis and is intended to probe heterogeneity *within* established disease.

## 4. Physician-defined duration variable

Automated duration extraction cannot define the final clinical variable.

During Stage-2 physician state review, reviewers will determine whether the available diagnosis/complaint/examination text contains a duration that can be clearly attributed to the wrist-scaphoid problem.

Required fields:

- `gold_relevant_duration_present = yes / no / uncertain`;
- `gold_relevant_duration_value`;
- `gold_relevant_duration_unit = hours / days / weeks / months / years`;
- `gold_duration_basis = injury_since_event / wrist_symptom_duration / both / uncertain`.

### Selection rule

If multiple durations are documented, the reviewer should record the **longest clearly wrist-scaphoid-related index injury or symptom duration present at admission**, while recording its basis.

If an index injury duration and a shorter recent flare are both documented, the index injury duration is preferred for the chronicity analysis when the text clearly links it to the wrist-scaphoid problem.

If attribution is unclear, the reviewer records `uncertain` rather than inferring a duration from general history.

The automated parser output is not shown to the reviewer.

## 5. Analysis population

This secondary analysis is restricted to records satisfying all of the following after physician adjudication:

1. physician-confirmed wrist scaphoid;
2. established chronic fracture, established nonunion, or chronic/nonunion not distinguishable;
3. disease-concordant detailed operative record;
4. physician-adjudicated bone-graft label;
5. a clearly relevant documented duration.

Records without an interpretable relevant duration are excluded from the duration analysis but remain in the primary treatment-composition analysis.

## 6. Statistical analysis

### Primary secondary-analysis representation

Duration is analyzed as a **continuous variable**, converted to days using fixed unit conversions for descriptive analysis.

Report:

- available-duration denominator by graft group;
- median and IQR;
- full observed range in the private manuscript analysis when disclosure is appropriate;
- Mann-Whitney U test because of the anticipated small and skewed sample.

### Effect representation

Because the sample is small, the manuscript should emphasize the observed distributions and uncertainty rather than a fitted predictive model.

A log-scale visualization may be used because duration can span days to years, but the statistical comparison remains prespecified and simple.

### No data-derived threshold

The local data will **not** be searched for a cut point that maximizes significance or classification performance.

A threshold such as `>=1 year` may be shown only as a **literature-anchored descriptive sensitivity analysis** if retained before physician outcome inspection. It must not replace the continuous-duration analysis.

## 7. Literature context

Contemporary evidence supports biological plausibility for duration-dependent treatment heterogeneity without establishing a universal graft indication.

A 2026 retrospective comparison of stable scaphoid nonunions reported that graft-less fixation remained viable in selected cases, whereas graft augmentation was particularly advantageous in cystic nonunions, lesions with at least 5 mm bone loss, and nonunions of at least 1 year duration. Earlier fixation-without-graft series likewise reported poorer outcomes among patients with more than a 1-year injury-to-surgery interval.

These studies motivate duration as a clinically interpretable severity/chronicity descriptor. They do not validate the local duration association and do not justify changing the primary endpoint.

## 8. Interpretation boundary

If the physician-adjudicated duration signal persists, the strongest allowed interpretation is:

> Within established chronic/nonunion operative presentations, graft augmentation was concentrated among records with longer documented wrist-related disease duration.

The study cannot establish that duration itself caused graft selection because duration is correlated with unmeasured severity, bone loss, deformity, vascularity, prior treatment, and surgeon preference.

## 9. Claim hierarchy

1. **Primary manuscript question:** established chronic/nonunion versus comparison presentation -> bone-graft augmentation.
2. **Key contrast:** internal fixation remains common across groups.
3. **Secondary mechanistic hypothesis:** within established chronic/nonunion, longer documented duration -> greater graft use.
4. **Exploratory robustness:** acute-only comparison, augmentation composite, leave-one-out influence.

This hierarchy is fixed before Stage-2 physician outcomes are scored.
