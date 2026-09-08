# Bone-Graft Augmentation in Established Chronic/Nonunion Versus Other Wrist-Scaphoid Presentations: A Retrospective Operative-Record Study

**Draft status:** v0.1, pre-physician-adjudication  
**Primary analysis status:** exploratory, data-derived hypothesis  
**Local dataset:** fixed; no additional hospital data assumed

> Values labelled *deterministic pre-validation* are algorithm-derived screening results and must not be promoted to final clinical estimates until the physician reference standard is frozen.

---

## Abstract

### Background

Scaphoid nonunion surgery commonly combines stable fixation with bone-graft augmentation when healing biology, vascularity, bone loss, or deformity are concerning. However, the operative composition of real-world scaphoid presentations is heterogeneous, and grafting is not universally required even among nonunions.

### Purpose

To determine whether established chronic/nonunion wrist-scaphoid presentations are associated with greater use of bone-graft augmentation than other wrist-scaphoid presentations, while examining whether internal fixation remains common in both groups.

### Methods

We performed a retrospective study using a fixed set of hospital electronic health record exports. Broad scaphoid retrieval was followed by anatomy-specific classification to distinguish wrist scaphoid from foot navicular disease. Established chronic/nonunion status was defined from diagnosis, complaint, and physical-examination text only; operative text was excluded from exposure assignment. Detailed operative records were included in the treatment-composition analysis only when the documented procedure was attributable to the wrist scaphoid. The prespecified primary outcome was bone-graft augmentation; internal fixation was the key contrast outcome. Final clinical estimates require physician adjudication of anatomy, clinical state, operative relevance, fixation, and graft labels. Fisher exact tests were prespecified for sparse binary comparisons.

### Results

The deterministic pre-validation audit identified 88 broad scaphoid candidates, including 68 high-specificity wrist-scaphoid admissions. Of these, 23 were classified as established chronic/nonunion and 45 as comparison presentations. Twenty-eight admissions had disease-concordant detailed operative documentation, all from 2023-2025 (15 chronic/nonunion; 13 comparison). Internal fixation was identified in 14/15 and 12/13 operative records, respectively, whereas bone grafting was identified in 8/15 chronic/nonunion records and fewer than five comparison records. These values remain provisional pending physician adjudication.

### Conclusions

**To be completed after physician-reference validation.** The intended interpretation is limited to the association between clinical presentation and documented operative composition; the study does not evaluate postoperative union, treatment efficacy, or future nonunion risk.

---

# Introduction

Scaphoid nonunion remains a challenging problem in hand and wrist surgery because treatment must address both mechanical stability and the biological environment required for healing. The tenuous vascular supply of the scaphoid, particularly around the proximal pole, together with bone loss, deformity, and delayed presentation, can complicate reconstruction. Contemporary reviews therefore describe internal fixation as a common mechanical foundation of nonunion surgery, with supplemental bone grafting selected according to factors such as proximal-pole viability, vascularity, and deformity.[1,2]

The role of bone grafting is nevertheless not uniform across all nonunions. Recent treatment algorithms stratify graft choice according to established risk factors for surgical failure, and systematic reviews have not shown a single graft strategy to be globally superior across all clinical scenarios.[3,4] In selected stable, well-aligned nonunions, fixation without grafting has also produced high union rates, while graft augmentation appears more relevant in cystic, long-standing, biologically compromised, or structurally deficient lesions.[5,6] These observations suggest that the clinically meaningful distinction may not simply be whether fixation is performed, but whether additional biological or reconstructive augmentation is added to the fixation construct.

At the same time, operative practice remains heterogeneous. A 2024 survey of hand surgeons found near-unanimous agreement on headless compression screw fixation in many scaphoid settings but substantial variation in graft selection for nonunion, revision surgery, and avascular necrosis.[7] Population-level studies have similarly demonstrated variation in nonunion-related treatment and graft use.[8,9] Much of the contemporary literature, however, evaluates technique selection, graft type, or union outcomes within cohorts already defined as scaphoid nonunion. The transition in operative composition across broader real-world wrist-scaphoid presentations is less directly characterized.

Using a fixed set of hospital clinical records, we observed a preliminary pattern in which internal fixation was frequent across wrist-scaphoid operative presentations, whereas bone-graft use appeared concentrated among records with an established chronic/nonunion phenotype. We therefore asked a focused, data-driven question: **among wrist-scaphoid admissions with disease-concordant detailed operative documentation, is established chronic/nonunion disease associated with increased bone-graft augmentation while internal fixation remains common in both phenotype groups?** Because this hypothesis arose from the same dataset, the present study is explicitly exploratory and hypothesis-generating. The objective is to quantify the treatment-composition signal with physician-validated clinical abstraction, not to predict incident nonunion or infer treatment efficacy.

---

# Methods

## Study design and data source

We conducted a retrospective, fixed-data study using hospital electronic health record exports spanning 2015-2025. The source package contained structured demographic and diagnostic fields together with free-text complaint, specialist examination, operative-name, and detailed operative-note records. The dataset also included examination/imaging-report and laboratory modules, although these were not required for the primary treatment-composition question.

No additional local clinical data are assumed to become available. Raw patient-level records, identifiers, dates, and clinical free text remain local and are not released in the public research repository. Publicly released artifacts are limited to code, schema documentation, and privacy-preserving aggregate results.

**Ethics/IRB:** [Institutional review board / ethics approval and waiver information to be inserted from the approved study documentation.]

## Cohort identification and anatomical restriction

The supplied broad scaphoid retrieval produced 88 candidate admission episodes. Because the Chinese term for scaphoid/navicular can refer to either the wrist scaphoid or the foot navicular, candidate records were first classified by anatomical context. High-specificity wrist-scaphoid evidence included explicit wrist/hand scaphoid terminology, wrist context linked to the scaphoid, or scaphoid waist/proximal/distal-pole terminology. Explicit foot-navicular terminology was classified separately, and records with insufficient anatomical evidence were retained as uncertain rather than forced into a binary class.

The deterministic pre-validation anatomy audit classified 68/88 candidates as wrist scaphoid, 13 as foot navicular, and 7 as ambiguous. These algorithm-derived classifications will be evaluated against physician review before final clinical analyses.

## Definition of established chronic/nonunion presentation

Within wrist-scaphoid admissions, clinical state was determined from non-operative clinical sources only:

- diagnosis text;
- presenting complaint;
- specialist physical examination.

Operative names and detailed operative-note contents were explicitly excluded from exposure assignment to prevent circularity because operative treatment components were downstream outcomes.

The physician reference-standard categories are:

1. acute/new fracture;
2. established chronic fracture;
3. established nonunion;
4. chronic/nonunion not distinguishable from the available record;
5. insufficient/uncertain.

For the primary clinical comparison, established chronic fracture, established nonunion, and chronic/nonunion-not-distinguishable categories will form the `established chronic/nonunion` exposure group. Other physician-adjudicated wrist-scaphoid records will form the main comparison group, with uncertain states excluded from the relevant analysis.

A separate prespecified sensitivity analysis will restrict the comparison group to physician-confirmed acute/new fractures only.

## Rationale for the acute-only sensitivity analysis

The deterministic pre-validation operative comparison group contains 13 disease-concordant operative admissions. A conservative source-text audit found explicit acute/new or recent-injury wording in only 7/13 records; the remainder contained postoperative-history wording, longer-duration wording without an explicit chronic keyword, or insufficient explicit state evidence. Therefore, the full comparison group is not assumed to be an acute cohort. The acute-only analysis was prespecified before physician adjudication to assess sensitivity to comparison-state definition.

## Operative-record attribution

The presence of a detailed operative-note module was treated as a documentation variable rather than proof that the documented operation treated the wrist scaphoid. Admissions can contain procedures for multiple orthopaedic problems, and generic terms such as internal fixation or screw placement may refer to a different anatomical site.

For each wrist-scaphoid admission with a detailed operative note, physician reviewers will first assign:

`target-disease procedure present = yes / no / uncertain`.

Only disease-concordant wrist-scaphoid operative records contribute to the treatment-composition analysis. Notes documenting only another anatomical procedure are retained as hard negatives for measurement validation but are excluded from the clinical procedure denominator.

## Operative treatment components

The prespecified **primary outcome** is bone-graft augmentation, defined as explicit documentation of bone grafting or bone harvest used as part of the wrist-scaphoid operation.

The **key contrast outcome** is internal fixation, including screw, headless/cannulated screw, wire, or other explicitly documented target-disease internal fixation.

Secondary treatment variables include:

- reconstruction;
- fusion/arthrodesis;
- a composite of bone graft, reconstruction, or fusion;
- the number of major components among fixation, graft, reconstruction, and fusion.

Bone graft was chosen as the primary outcome before physician-reference scoring because it represents a specific biological augmentation step and avoids defining the main result through a post-hoc composite.

## Physician reference standard

The main-paper reference standard is restricted to the variables required for the scaphoid scientific question. Physicians will review:

- all 88 broad scaphoid candidate admissions for anatomical classification;
- the 68 deterministic wrist-scaphoid admissions for clinical state;
- the 31 wrist-scaphoid admissions with a detailed operative-note module for target-disease procedure relevance and operative components.

Approximately 20% of each layer will undergo independent second review. The second reviewer will remain blinded to the first review and to all deterministic or model predictions. Discordances will be adjudicated by consensus or by a prespecified senior reviewer. The final reference standard will then be cryptographically frozen before formal algorithm scoring.

## Statistical analysis

Continuous baseline variables will be summarized as median and interquartile range unless their distributions justify mean and standard deviation. Categorical variables will be reported as counts and percentages with explicit denominators.

The primary comparison of bone-graft augmentation between established chronic/nonunion and comparison operative records will use Fisher's exact test because of sparse cells. A crude odds ratio and 95% confidence interval will be reported in the manuscript analysis. Internal fixation will be analyzed using the same approach as a prespecified contrast.

The number of major operative components will be summarized as median and interquartile range and compared using the Mann-Whitney U test as a secondary analysis.

No routine high-dimensional multivariable model is prespecified for the small operative sample. In particular, stepwise selection, random forests, gradient boosting, and neural-network models are not used to answer the primary clinical question.

## Prespecified robustness analyses

Robustness analyses will include:

1. deterministic versus physician-adjudicated labels;
2. exclusion of uncertain clinical-state or procedure-relevance records;
3. established chronic/nonunion versus physician-confirmed acute/new fractures only;
4. bone-graft augmentation versus the broader graft/reconstruction/fusion composite;
5. leave-one-out influence analysis for the primary 2×2 association;
6. exclusion of records with competing same-admission orthopaedic procedures.

Because all current disease-concordant detailed scaphoid operative records occur in 2023-2025, earlier years do not provide an independent detailed-procedure replication cohort under the supplied exports.

---

# Results

## Cohort derivation

The broad scaphoid retrieval contained 88 admission episodes. The deterministic pre-validation anatomy audit classified 68 as high-specificity wrist scaphoid, 13 as explicit foot navicular, and 7 as anatomically ambiguous. Within the 68 deterministic wrist-scaphoid episodes, 23 met the pre-validation established chronic/nonunion rule and 45 formed the comparison group.

Thirty-one wrist-scaphoid admissions had a detailed operative-note module. After excluding detailed notes that were not attributable to the wrist-scaphoid problem, 28 disease-concordant operative admissions remained in the deterministic pre-validation analysis: 15 established chronic/nonunion and 13 comparison records. All 28 occurred in 2023-2025.

**Final cohort counts after physician adjudication: [to be inserted].**

## Operative-subset baseline characteristics

In the deterministic pre-validation operative subset, median age was 34.0 years (IQR 28.5-51.0) in the chronic/nonunion group and 37.0 years (IQR 33.0-41.0) in the comparison group. Median BMI was 24.7 kg/m² (IQR 23.1-27.0) and 25.6 kg/m² (IQR 23.2-28.9), respectively; BMI was available in 15 and 12 records.

These descriptive values are provisional because group assignment remains subject to physician adjudication.

## Primary treatment-composition signal

The deterministic pre-validation extraction identified internal fixation in 14/15 (93.3%) established chronic/nonunion operative records and 12/13 (92.3%) comparison operative records. Bone grafting was identified in 8/15 (53.3%) chronic/nonunion records and in fewer than five comparison records.

The intended primary inferential result is the physician-adjudicated odds ratio for bone-graft augmentation:

**OR [to be inserted], 95% CI [to be inserted], Fisher P = [to be inserted].**

Internal fixation will be reported as the key contrast:

**OR [to be inserted], 95% CI [to be inserted], Fisher P = [to be inserted].**

## Secondary treatment intensity

In the deterministic pre-validation analysis, the major procedure-component count had a median of 2.0 (IQR 1.0-2.0) in chronic/nonunion records and 1.0 (IQR 1.0-1.0) in comparison records. The graft/reconstruction/fusion composite was also more frequent in the chronic/nonunion group, but this composite remains secondary regardless of statistical significance.

**Physician-adjudicated secondary results: [to be inserted].**

## Acute-only sensitivity analysis

A conservative pre-validation audit showed explicit acute/recent-injury wording in only 7 of the 13 current operative comparison records. The prespecified acute-only analysis will therefore be performed only after physician state adjudication.

**Acute-only result: [to be inserted].**

---

# Discussion

## Principal finding

**To be finalized after physician adjudication.** The central interpretation will test whether established chronic/nonunion scaphoid presentations differ from other wrist-scaphoid presentations primarily through additional biological augmentation rather than through a large difference in fixation use.

If the physician-adjudicated results preserve the current pattern, the principal finding will be framed as follows:

> Internal fixation remained common across surgically treated wrist-scaphoid presentations, whereas established chronic/nonunion disease was associated with substantially greater use of bone-graft augmentation.

This formulation deliberately avoids implying that chronicity causes graft use or that grafting improves outcome.

## Clinical interpretation

The anticipated pattern is biologically plausible. Internal fixation provides mechanical stabilization, whereas grafting adds osteogenic/osteoconductive material and may restore bone stock or address biologically compromised nonunion. Contemporary treatment reviews and algorithms recommend tailoring graft strategy to viability, vascularity, defect size, deformity, and prior treatment rather than using a single graft approach for all nonunions.[1-6]

The value of the present analysis is therefore not to restate that grafting is used in nonunion. Rather, it tests whether routine clinical records show a measurable **treatment-composition transition**: fixation remains the common mechanical base, while graft augmentation becomes more frequent when the presentation is established as chronic/nonunion.

## Relationship to existing literature

Previous systematic reviews have primarily compared union rates and functional outcomes across grafting and fixation techniques within established nonunion cohorts.[4,6,10] Survey and population studies demonstrate that graft selection and nonunion management vary substantially among surgeons and health systems.[7-9] The present study uses a different contrast: it compares the composition of documented surgery across real-world wrist-scaphoid presentation states rather than comparing outcomes among graft types.

## Limitations

This study has several important limitations. First, the treatment-composition hypothesis was discovered in the same fixed dataset and must therefore be considered exploratory and hypothesis-generating. Second, the disease-concordant operative sample is small and confined to 2023-2025 because of the structure of the supplied exports. Third, long-term union, recurrence, pain, and functional outcomes are not consistently available and cannot be inferred from the operative record. Fourth, important treatment-selection factors such as standardized fracture displacement, proximal-pole vascularity, humpback deformity, and quantitative CT geometry are incompletely documented in the available structured data. Fifth, free-text state and procedure variables require physician validation; the final clinical result depends on the frozen reference-standard analysis. Finally, the single-center retrospective design limits generalizability.

## Conclusion

**To be completed after physician adjudication.** The final conclusion will remain restricted to treatment composition and will not make claims regarding future nonunion prediction or treatment efficacy.

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
