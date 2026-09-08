# Bone-Graft Augmentation in Established Chronic/Nonunion Versus Other Wrist-Scaphoid Presentations: A Retrospective Operative-Record Study

**Draft:** v0.3, before physician-reference completion  
**Design:** retrospective, fixed-data, exploratory observational study  
**Primary hypothesis:** data-derived and hypothesis-generating  
**Secondary duration hypothesis:** frozen after primary-question selection and before Stage-2 physician adjudication

> Deterministic values in this draft are pre-validation observations. Final cohort sizes, effect estimates, and conclusions will be regenerated from the frozen two-stage physician reference standard.

---

## Abstract

### Background

Scaphoid nonunion surgery often combines mechanical stabilization with bone-graft augmentation, but grafting is not universally required. Operative strategy varies with biological and structural characteristics of the nonunion, and disease duration may contribute to this heterogeneity.

### Purpose

To examine whether established chronic/nonunion wrist-scaphoid presentations are associated with greater use of bone-graft augmentation than other wrist-scaphoid presentations while internal fixation remains common across groups. A prespecified exploratory secondary analysis examines whether, within established chronic/nonunion records, graft augmentation is associated with longer documented wrist-related injury or symptom duration.

### Methods

We performed a retrospective study using a fixed set of hospital electronic health record exports. All 88 records retrieved under a broad scaphoid search undergo physician anatomy adjudication before the final wrist-scaphoid cohort is defined. Only after anatomy adjudication is frozen are downstream state and operative review packets generated for physician-confirmed wrist-scaphoid records. Clinical state and clinically relevant duration are adjudicated from diagnosis, complaint, and physical-examination text; operative text is excluded from exposure assignment. Detailed operative records contribute to the clinical analysis only when the procedure is attributable to the wrist scaphoid. The prespecified primary outcome is bone-graft augmentation, with internal fixation as the key contrast. Fisher exact tests are used for sparse binary comparisons. Relevant duration is analyzed continuously within established chronic/nonunion records as a secondary hypothesis.

### Results

The deterministic pre-validation audit identified 88 broad scaphoid candidates and classified 68 as wrist scaphoid, 13 as foot navicular, and 7 as anatomically ambiguous. Within the deterministic wrist cohort, 23 records were classified as established chronic/nonunion and 45 as comparison presentations. Twenty-eight records had disease-concordant detailed operative documentation, all from 2023-2025 (15 chronic/nonunion; 13 comparison). Internal fixation was identified in 14/15 and 12/13 operative records, respectively, whereas bone grafting was identified in 8/15 chronic/nonunion records and fewer than five comparison records. Within the 15 deterministic chronic/nonunion operative records, explicit relevant duration was recoverable in 13; median duration was 182.6 days among graft-positive records and 15.0 days among graft-negative records. All values remain provisional pending physician adjudication.

### Conclusions

To be completed after physician-reference adjudication. Interpretation will be restricted to associations between presentation state, documented chronicity, and operative composition; postoperative union, treatment efficacy, and future nonunion risk are outside the scope of the available data.

---

# Introduction

Scaphoid nonunion remains difficult to manage because successful reconstruction requires both mechanical stability and a biological environment capable of supporting fracture healing. The scaphoid's vascular anatomy, particularly around the proximal pole, can make delayed healing consequential, while bone loss, deformity, and avascular necrosis may further complicate reconstruction. Contemporary reviews therefore describe stable fixation as a common mechanical foundation of nonunion treatment and bone graft as a supplemental strategy selected according to proximal-pole viability, vascularity, defect geometry, deformity, and prior treatment.[1,2]

Bone grafting is not uniformly required in every scaphoid nonunion. Selected stable, well-aligned nonunions can unite after rigid fixation without grafting, whereas graft augmentation appears more relevant in cystic, long-standing, biologically compromised, or structurally deficient lesions.[3-6] A recent retrospective comparison of graft-less and graft-augmented fixation reported particular benefit from graft augmentation in cystic nonunions, defects with at least 5 mm bone loss, and nonunions of at least 1 year duration.[6] Earlier fixation-without-graft experience likewise suggested less favorable outcomes when the interval from injury to surgery exceeded 1 year.[11] These findings support the possibility that disease chronicity contributes to treatment heterogeneity without establishing a universal duration threshold for grafting.

Practice variation remains substantial. A survey of hand surgeons found broad agreement on headless compression screw fixation in many scaphoid settings but considerable variation in graft selection for nonunion, revision surgery, and avascular necrosis.[7] Population-level studies have similarly demonstrated variation in nonunion treatment and use of vascularized grafting.[8,9] Much of the literature nevertheless compares graft choice, fixation technique, or union outcomes within cohorts already defined as scaphoid nonunion.[4,6,10] A complementary question is how the **composition of surgery itself** changes across real-world wrist-scaphoid presentation states and, within established disease, whether greater documented chronicity corresponds to additional biological augmentation.

During structured review of a fixed hospital dataset, we observed a preliminary pattern in which internal fixation was frequent across operative wrist-scaphoid presentations, whereas bone grafting appeared concentrated among records with an established chronic/nonunion phenotype. We therefore asked a focused, data-driven primary question: **among wrist-scaphoid admissions with disease-concordant detailed operative documentation, is established chronic/nonunion disease associated with greater use of bone-graft augmentation while internal fixation remains common across groups?** After this primary question was selected, a separate pre-validation audit identified a possible duration gradient within chronic/nonunion records. We therefore froze duration as an exploratory secondary hypothesis before Stage-2 physician adjudication. Neither hypothesis is used to predict incident nonunion or infer treatment efficacy.

---

# Methods

## Study design and data source

We conducted a retrospective study using a fixed set of hospital electronic health record exports spanning 2015-2025. The source package included structured demographic and diagnostic fields, free-text presenting complaints and specialist physical examinations, operation names, and detailed operative notes. Examination/imaging-report and laboratory exports were also available but were not required to answer the primary treatment-composition question.

No additional local clinical data are assumed to become available. Raw patient-level records, identifiers, dates, and free text remain within the private analytic environment. The public repository contains code, schema documentation, and privacy-preserving aggregate outputs only.

**Ethics:** [Institutional review board / ethics approval, waiver, and data-governance information to be inserted from approved study documentation.]

## Broad scaphoid retrieval

The hospital extraction returned 88 candidate admission episodes under broad scaphoid terminology. In Chinese clinical records, terminology corresponding to scaphoid/navicular can refer to the wrist scaphoid or foot navicular, making anatomical adjudication necessary before disease-state or operative comparisons.

The deterministic v0.3 audit, used only as a pre-validation engineering check, classified 68 candidates as wrist scaphoid, 13 as explicit foot navicular, and 7 as anatomically ambiguous.

## Two-stage physician reference standard

To avoid verification bias, the final clinical cohort is not defined by deterministic-rule positivity.

### Stage 1: anatomy adjudication

All 88 broad candidates are reviewed by a physician blinded to deterministic predictions and study effect estimates. Each candidate is assigned one anatomy label: wrist scaphoid, foot navicular, other, or uncertain. Approximately 20% undergo independent second review. Discordances are adjudicated before the Stage-1 anatomy file is frozen.

The 88-record Stage-1 review population and its prespecified 18-record double-review subset were cryptographically frozen while every anatomy Gold field was blank.

### Stage 2: downstream adjudication generated from physician anatomy

Only after Stage 1 is frozen are downstream review packets generated for physician-confirmed wrist-scaphoid records. Thus, the numbers of state-review and procedure-review records are determined by physician anatomy Gold rather than by the deterministic 68/31 counts.

Approximately 20% of each Stage-2 layer undergoes independent blinded second review followed by adjudication.

## Clinical-state definition

Clinical state is adjudicated from diagnosis, presenting complaint, and specialist physical examination only. Operation names and operative-note contents are excluded because operative treatment is the downstream variable of interest.

Physician categories are:

1. acute/new fracture;
2. established chronic fracture;
3. established nonunion;
4. chronic/nonunion not distinguishable from the available record;
5. insufficient/uncertain.

For the primary analysis, categories 2-4 comprise the established chronic/nonunion group. Other sufficiently classifiable physician-confirmed wrist-scaphoid records form the main comparison group. Records with uncertain state are excluded from the relevant inferential comparison.

## Acute-only sensitivity definition

The comparison group is not assumed to be uniformly acute. In the deterministic pre-validation operative comparison set, explicit acute/new or recent-injury wording was found in only 7 of 13 records. Other records contained postoperative-history wording, longer-duration wording without a specific chronic keyword, or insufficient explicit state evidence.

Accordingly, a sensitivity analysis was prespecified before physician adjudication that restricts the comparison group to physician-confirmed acute/new fractures.

## Operative-record attribution

The presence of a detailed operative-note module is not considered proof that the documented operation treated the wrist scaphoid. For each physician-confirmed wrist-scaphoid record with a detailed operative note, reviewers first assign target-disease procedure relevance as yes, no, or uncertain. Only disease-concordant wrist-scaphoid operative records contribute to treatment-composition inference.

## Operative treatment components

### Primary outcome: bone-graft augmentation

Bone-graft augmentation is defined as explicit use of bone graft or bone harvest as part of the wrist-scaphoid operation. This outcome was selected before physician-reference scoring and is not replaced by a broader composite on the basis of statistical significance.

### Key contrast: internal fixation

Internal fixation includes screw, headless/cannulated screw, wire, or other explicitly documented fixation used for the wrist-scaphoid procedure.

### Secondary treatment variables

Secondary variables include reconstruction, fusion/arthrodesis, a graft/reconstruction/fusion augmentation composite, and the number of major components among fixation, graft, reconstruction, and fusion.

## Secondary hypothesis: documented wrist-related duration

After the primary treatment-composition question had been selected, a pre-validation audit suggested that graft-positive chronic/nonunion records had longer documented wrist-related durations than graft-negative chronic/nonunion records. This duration analysis was therefore frozen as a **secondary exploratory hypothesis** before Stage-2 physician adjudication.

Automated parser output does not define the clinical variable and is not shown to physician reviewers. During Stage-2 state review, physicians record:

- whether a clearly wrist-scaphoid-related duration is present;
- the duration value;
- the unit (hours, days, weeks, months, or years);
- whether the duration represents time since the index injury, wrist-symptom duration, both, or is semantically uncertain.

If multiple durations are present, the reviewer records the longest duration clearly attributable to the index wrist-scaphoid injury or related wrist symptoms. A recent flare is not substituted for a longer index-injury duration when both are explicitly documented.

The duration analysis is restricted to physician-confirmed established chronic/nonunion records with disease-concordant operative documentation, physician-adjudicated graft status, and an interpretable relevant duration. Duration is converted to days after adjudication using fixed unit conversions and analyzed continuously. Median and interquartile range are reported by graft group, with a Mann-Whitney U test because the expected sample is small and skewed.

No local duration threshold is selected by maximizing P value, AUROC, Youden index, or classification accuracy. A 1-year split may be shown only as a literature-anchored descriptive sensitivity analysis and cannot replace the continuous-duration analysis.

## Baseline variables

Age, sex, and BMI are summarized for physician-defined operative analysis groups. Other preoperative descriptors are reported only if physician review establishes adequate completeness and clear interpretation.

## Statistical analysis

Categorical variables are summarized as n (%). Continuous variables are summarized as median (interquartile range) unless their distribution and scale justify mean (standard deviation).

The primary comparison of bone-graft augmentation between established chronic/nonunion and comparison operative records uses Fisher's exact test. A crude odds ratio and 95% confidence interval will be reported. Internal fixation is analyzed using the same sparse-table approach as the prespecified key contrast.

The major procedure-component count and physician-adjudicated duration are secondary continuous comparisons analyzed with the Mann-Whitney U test.

No routine high-dimensional multivariable model is prespecified for the small operative sample. Stepwise selection, random forests, gradient boosting, and neural networks are not used to answer the clinical question.

## Prespecified robustness analyses

Robustness analyses include:

1. physician-defined chronic/nonunion versus the full classifiable comparison group;
2. chronic/nonunion versus physician-confirmed acute/new records only;
3. exclusion of uncertain procedure relevance;
4. bone-graft primary outcome versus the broader augmentation composite;
5. leave-one-out influence analysis for the primary 2x2 association;
6. exclusion of records with competing same-admission orthopaedic procedures;
7. deterministic pre-validation effect versus physician-adjudicated effect as measurement robustness;
8. physician-adjudicated duration comparison within established chronic/nonunion records.

Because all currently identified disease-concordant detailed scaphoid operative records occur in 2023-2025, earlier years do not constitute an independent detailed-procedure validation cohort under the supplied exports.

---

# Results

## Deterministic pre-validation cohort audit

The broad scaphoid retrieval contained 88 admission episodes. Before physician review, deterministic anatomy rules classified 68 as wrist scaphoid, 13 as foot navicular, and 7 as ambiguous. Within the 68 deterministic wrist records, 23 met the pre-validation established chronic/nonunion rule and 45 formed the comparison group.

Thirty-one deterministic wrist-scaphoid records contained a detailed operative-note module. After rule-based target-disease attribution, 28 were considered disease-concordant detailed operative records: 15 chronic/nonunion and 13 comparison. All 28 occurred in 2023-2025.

**Final physician-defined cohort counts: [pending].**

## Deterministic pre-validation operative characteristics

In the current 28-record deterministic operative audit, median age was 34.0 years (IQR 28.5-51.0) in the chronic/nonunion group and 37.0 years (IQR 33.0-41.0) in the comparison group. Median BMI was 24.7 kg/m² (IQR 23.1-27.0) and 25.6 kg/m² (IQR 23.2-28.9), respectively; BMI was available in 15 and 12 records.

## Deterministic pre-validation treatment signal

Internal fixation was identified in 14/15 (93.3%) established chronic/nonunion operative records and 12/13 (92.3%) comparison records. Bone grafting was identified in 8/15 (53.3%) chronic/nonunion records and in fewer than five comparison records.

These values motivated the scientific question but are not the final clinical result.

### Final primary result after physician adjudication

Bone-graft augmentation:

**OR [pending], 95% CI [pending], Fisher exact P [pending].**

### Key contrast after physician adjudication

Internal fixation:

**OR [pending], 95% CI [pending], Fisher exact P [pending].**

## Secondary treatment intensity

In the deterministic pre-validation audit, the major procedure-component count had a median of 2.0 (IQR 1.0-2.0) in chronic/nonunion records and 1.0 (IQR 1.0-1.0) in comparison records.

**Physician-adjudicated secondary treatment-intensity result: [pending].**

## Secondary duration signal

Among the 15 deterministic chronic/nonunion operative records, a relevant duration expression was recoverable in 13. Among graft-positive records, duration was available in 7/8 and had a median of 182.6 days (IQR 167.4-1004.4). Among graft-negative records, duration was available in 6/7 and had a median of 15.0 days (IQR 2.3-41.0).

These values are pre-validation and are not interpreted as a final clinical association. The final duration analysis will use physician-adjudicated duration semantics and graft status.

**Physician-adjudicated duration result: [pending].**

## Acute-only sensitivity analysis

The prespecified acute-only analysis will use physician-confirmed acute/new operative records after Stage-2 adjudication.

**Acute-only effect estimate: [pending].**

---

# Discussion

## Principal finding

The principal finding will be finalized after the physician-defined clinical cohort is frozen. The primary hypothesis is that established chronic/nonunion wrist-scaphoid disease is associated with **additional biological augmentation**, rather than a large difference in whether fixation is used at all.

If the physician-adjudicated result preserves the current signal, the main interpretation will be:

> Internal fixation remained common across surgically treated wrist-scaphoid presentations, whereas established chronic/nonunion disease was associated with substantially greater use of bone-graft augmentation.

This formulation does not imply that chronicity causes graft use or that grafting improves postoperative outcome.

## Duration as a secondary marker of treatment heterogeneity

If physician adjudication also preserves the duration gradient, the secondary observation would suggest that established chronic/nonunion disease is itself heterogeneous: graft augmentation may be concentrated in records with longer documented wrist-related disease duration. This is clinically plausible because long-standing nonunion may co-occur with bone resorption, cystic change, deformity, vascular compromise, and prior treatment history. Recent comparative evidence has reported greater benefit from graft augmentation in cystic nonunion, defects with at least 5 mm bone loss, and nonunion duration of at least 1 year.[6] Earlier fixation-without-graft data also identified an injury-to-surgery interval beyond 1 year as an adverse prognostic feature.[11]

Duration cannot, however, be interpreted as an independent causal driver of graft selection in the present dataset. It is likely correlated with disease morphology and biological compromise that are incompletely measured here. The duration analysis is therefore secondary and exploratory, and no local threshold for grafting will be derived.

## Clinical interpretation

Fixation primarily provides mechanical stability, whereas grafting can add osteogenic/osteoconductive material, restore bone stock, and support reconstruction in biologically or structurally compromised nonunion. Contemporary reviews and algorithms recommend tailoring graft strategy to vascularity, proximal-pole viability, defect size, deformity, and prior treatment rather than applying a single approach to all nonunions.[1-6]

The contribution of the present study is not the generic observation that bone graft can be used in scaphoid nonunion. It tests whether routine operative records reveal a measurable change in treatment composition across presentation states and whether, within established disease, documented chronicity tracks the use of biological augmentation.

## Relationship to prior literature

Systematic reviews and comparative studies have largely evaluated union, function, or complications across graft and fixation techniques within established nonunion cohorts.[4-6,10] Survey and population studies demonstrate persistent variation in graft selection and nonunion management.[7-9] The present study uses a different clinical contrast by examining operative composition across real-world wrist-scaphoid presentation states and a secondary chronicity gradient within established disease.

## Limitations

The study is exploratory because the primary treatment-composition hypothesis was generated from the same fixed dataset, and the duration hypothesis was identified during subsequent pre-validation exploration. The operative sample is small and concentrated in 2023-2025. Long-term union, pain, function, and recurrence are not consistently available. Important treatment-selection variables such as standardized displacement, proximal-pole vascularity, humpback deformity, defect size, cystic change, and quantitative CT geometry are incompletely captured. Duration is documented opportunistically in routine text rather than through a standardized prospective instrument. Clinical state, duration semantics, and procedure components therefore require physician adjudication. The single-center retrospective design limits generalizability.

The two-stage physician-reference design reduces verification bias by preventing deterministic anatomy rules from defining the downstream clinical cohort. It does not eliminate confounding by unmeasured disease severity or surgeon preference.

## Conclusion

**Pending physician adjudication.** Final conclusions will remain limited to associations among scaphoid presentation state, documented chronicity, and operative composition. The study will not make claims about treatment efficacy, future nonunion prediction, or a duration threshold for grafting.

---

# References

1. Ayalon O, Rettig SA, Tedesco LJ. Bone Graft and Fixation Options in the Surgical Management of Scaphoid Nonunion. *J Am Acad Orthop Surg*. 2024. PMID: 39531592. doi:10.5435/JAAOS-D-24-00510.
2. Miller EA, Huang JI. Traditional Bone Grafting in Scaphoid Nonunion. *Hand Clin*. 2024;40(1):105-116. PMID: 37979982. doi:10.1016/j.hcl.2023.08.001.
3. Higgins JP. When to Use Vascularized Bone? An Algorithm for Scaphoid Nonunion Surgery. *J Wrist Surg*. 2025. PMID: 41574159. doi:10.1055/a-2640-4238.
4. Graft choice for managing scaphoid non-union: umbrella review. 2024. PMID: 39122186.
5. A systematic review of mechanical stabilization by screw fixation without bone grafting in the management of stable scaphoid non-union. 2021. PMID: 33816106.
6. Necessity of grafting in scaphoid nonunion fixation: A comparative outcome analysis. 2026. PMID: 41695733.
7. Scaphoid Fractures and Nonunion: A Survey-based Review of Hand Surgeon's Practice and the Evidence. 2024. PMID: 39703594.
8. An Epidemiologic Perspective on Scaphoid Fracture Treatment and Frequency of Nonunion Surgery in the USA. 2018. PMID: 30258328.
9. MRI for Scaphoid Nonunion: Utilization Rates, Factors Associated With Utilization, and Subsequent Vascularized Bone Graft Use. 2024. PMID: 39614839. doi:10.1016/j.jhsa.2024.10.008.
10. Bone grafting for scaphoid nonunion surgery: a systematic review and meta-analysis. 2022. PMID: 35491585.
11. Compression screw fixation without bone grafting for scaphoid fibrous nonunion. 2015. PMID: 26330777.
