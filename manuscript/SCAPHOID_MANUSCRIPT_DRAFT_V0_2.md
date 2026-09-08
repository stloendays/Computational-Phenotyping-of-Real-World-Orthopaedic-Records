# Bone-Graft Augmentation in Established Chronic/Nonunion Versus Other Wrist-Scaphoid Presentations: A Retrospective Operative-Record Study

**Draft:** v0.2, before physician-reference completion  
**Design:** retrospective, fixed-data, exploratory observational study  
**Primary hypothesis:** data-derived and hypothesis-generating

> All deterministic counts below are explicitly pre-validation observations. Final clinical cohort sizes, effect estimates, and conclusions will be regenerated from the frozen physician reference standard.

---

## Abstract

### Background

Scaphoid nonunion surgery often combines mechanical stabilization with bone-graft augmentation, but grafting is not universally required and operative strategy varies according to biological and structural features of the nonunion.

### Purpose

To examine whether established chronic/nonunion wrist-scaphoid presentations are associated with greater use of bone-graft augmentation than other wrist-scaphoid presentations, while testing whether internal fixation remains common across both groups.

### Methods

We performed a retrospective study using a fixed set of hospital electronic health record exports. All 88 records retrieved under a broad scaphoid search undergo physician anatomy adjudication before the final wrist-scaphoid cohort is defined. Only after anatomy adjudication is frozen are downstream state and operative review packets generated for physician-confirmed wrist-scaphoid cases, preventing deterministic-rule positivity from predefining the clinical cohort. Clinical state is adjudicated from diagnosis, complaint, and physical-examination text only; operative text is excluded from exposure assignment. Detailed operative records contribute to the clinical analysis only when the documented procedure is attributable to the wrist scaphoid. The prespecified primary outcome is bone-graft augmentation, with internal fixation as the key contrast outcome. Sparse binary comparisons use Fisher exact tests.

### Results

The deterministic pre-validation audit identified 88 broad scaphoid candidates and classified 68 as high-specificity wrist scaphoid, 13 as foot navicular, and 7 as anatomically ambiguous. Within the deterministic wrist cohort, 23 records were classified as established chronic/nonunion and 45 as comparison presentations. Twenty-eight records had disease-concordant detailed operative documentation, all from 2023-2025 (15 chronic/nonunion; 13 comparison). Internal fixation was identified in 14/15 and 12/13 operative records, respectively, whereas bone grafting was identified in 8/15 chronic/nonunion records and fewer than five comparison records. These values are provisional and will be replaced by physician-adjudicated estimates.

### Conclusions

To be completed after physician-reference adjudication. Interpretation will be restricted to the association between clinical presentation and operative composition; postoperative union, treatment efficacy, and future nonunion risk are outside the scope of the available data.

---

# Introduction

Scaphoid nonunion remains difficult to manage because successful reconstruction requires both mechanical stability and a biological environment capable of supporting fracture healing. The scaphoid's vascular anatomy, particularly around the proximal pole, can make delayed healing especially consequential, while bone loss, deformity, and avascular necrosis may further complicate reconstruction. Contemporary reviews therefore describe stable fixation as a common mechanical foundation of nonunion treatment and bone graft as a supplemental strategy selected according to factors such as proximal-pole viability, vascularity, defect geometry, and deformity.[1,2]

Bone grafting, however, is not uniformly required in every scaphoid nonunion. Recent treatment algorithms stratify graft choice according to risk factors for surgical failure, and systematic reviews have not established one graft strategy as universally superior across clinical scenarios.[3,4] Selected stable, well-aligned nonunions have also been treated successfully with rigid fixation without grafting, whereas graft augmentation appears more relevant in cystic, long-standing, biologically compromised, or structurally deficient lesions.[5,6] This distinction suggests that the clinically informative change across disease states may be the addition of biological or reconstructive augmentation to a fixation construct rather than a simple switch from no fixation to fixation.

Practice variation remains substantial. A recent survey of hand surgeons found broad agreement on headless compression screw fixation in many scaphoid settings but considerable variation in graft selection for nonunion, revision surgery, and avascular necrosis.[7] Population-level studies have likewise documented variation in nonunion treatment and use of vascularized grafting.[8,9] Much of the published literature nevertheless evaluates graft choice, fixation technique, or union outcomes within cohorts already defined as scaphoid nonunion.[4,6,10] A complementary question is how the **composition of surgery itself** differs across real-world wrist-scaphoid presentations before postoperative outcome selection.

During structured review of a fixed hospital dataset, we observed a preliminary pattern in which internal fixation was common across operative wrist-scaphoid presentations, whereas bone grafting appeared concentrated among records with an established chronic/nonunion phenotype. We therefore asked a focused, data-driven question: **among wrist-scaphoid admissions with disease-concordant detailed operative documentation, is established chronic/nonunion disease associated with greater use of bone-graft augmentation while internal fixation remains common across groups?** Because the hypothesis was generated from the same dataset, the study is explicitly exploratory and hypothesis-generating. Computational text processing is used only to recover measurable variables from the available records; it is not the scientific endpoint of the study.

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

To avoid verification bias, the final clinical cohort is **not** defined by deterministic-rule positivity.

### Stage 1: anatomy adjudication

All 88 broad candidates are reviewed by a physician blinded to deterministic predictions and study effect estimates. Each candidate is assigned one anatomy label:

- wrist scaphoid;
- foot navicular;
- other;
- uncertain.

Approximately 20% of records undergo independent second review. Disagreements are resolved by consensus or a prespecified senior reviewer. The Stage-1 anatomy file is then frozen.

### Stage 2: downstream adjudication generated from physician anatomy

Only after Stage 1 is frozen are downstream review packets generated for **physician-confirmed wrist-scaphoid records**. Thus, the number of state-review records and the number of wrist-scaphoid records with detailed operative notes are determined by physician anatomy Gold rather than by the current deterministic counts of 68 and 31.

Approximately 20% of each Stage-2 layer undergoes independent blinded second review, followed by adjudication.

## Clinical-state definition

For physician-confirmed wrist-scaphoid records, clinical state is adjudicated using only:

- diagnosis text;
- presenting complaint;
- specialist physical examination.

Operation names and operative-note contents are excluded from state adjudication because operative treatment is the downstream variable of interest.

Physician state categories are:

1. acute/new fracture;
2. established chronic fracture;
3. established nonunion;
4. chronic/nonunion not distinguishable from the available record;
5. insufficient/uncertain.

For the primary analysis, categories 2-4 comprise the **established chronic/nonunion** group. Other sufficiently classifiable physician-confirmed wrist-scaphoid records form the main comparison group. Records with uncertain state are excluded from the relevant inferential comparison.

## Acute-only sensitivity definition

The comparison group is not assumed to be uniformly acute. In the deterministic pre-validation operative comparison set, a conservative text audit found explicit acute/new or recent-injury wording in only 7 of 13 records. Other records contained postoperative-history wording, longer-duration wording without a specific chronic keyword, or insufficient explicit state evidence.

Accordingly, a sensitivity analysis was prespecified before physician adjudication that restricts the comparison group to records labelled **acute/new fracture** by physicians. The main analysis retains the broader classifiable non-established comparison group to avoid post-hoc exclusion based on the final effect estimate.

## Operative-record attribution

The presence of a detailed operative-note module is not considered proof that the documented operation treated the wrist scaphoid. The same admission can contain treatment for more than one orthopaedic problem, and generic terms such as screw fixation or internal fixation can otherwise be misattributed.

For each physician-confirmed wrist-scaphoid record with a detailed operative-note module, reviewers first assign:

`target-disease procedure present = yes / no / uncertain`.

Only disease-concordant wrist-scaphoid operative records contribute to the treatment-composition analysis. Notes documenting only another anatomical procedure remain in measurement validation as hard negatives but are excluded from clinical procedure prevalence estimates.

## Operative treatment components

### Primary outcome: bone-graft augmentation

Bone-graft augmentation is defined as explicit use of bone graft or bone harvest as part of the wrist-scaphoid operation.

This outcome was selected before physician-reference scoring because it represents a specific biological augmentation step and avoids defining the main result through a composite chosen after seeing significance.

### Key contrast: internal fixation

Internal fixation includes screw, headless/cannulated screw, wire, or other explicitly documented fixation used for the wrist-scaphoid procedure.

### Secondary treatment variables

Secondary variables are:

- reconstruction;
- fusion/arthrodesis;
- an augmentation composite consisting of bone graft, reconstruction, or fusion;
- number of major operative components among fixation, graft, reconstruction, and fusion.

Secondary outcomes remain secondary regardless of their P values.

## Baseline variables

Age, sex, and BMI are summarized for the physician-defined operative analysis groups. Other preoperative severity descriptors are reported only if physician review establishes adequate documentation and clear interpretation. Missing denominators are reported explicitly.

## Statistical analysis

Categorical variables are summarized as n (%). Continuous variables are summarized as median (interquartile range) unless their distribution and scale justify mean (standard deviation).

The primary comparison of bone-graft augmentation between established chronic/nonunion and comparison operative records uses Fisher's exact test because of sparse cell counts. A crude odds ratio and 95% confidence interval will be reported.

Internal fixation is analyzed using the same sparse-table approach as the prespecified key contrast.

The number of major operative components is compared with the Mann-Whitney U test as a secondary analysis.

No routine high-dimensional multivariable model is prespecified for the small operative sample. Stepwise selection, random forests, gradient boosting, and neural networks are not used to answer the clinical question.

## Prespecified robustness analyses

Robustness analyses include:

1. primary physician-defined chronic/nonunion versus full classifiable comparison group;
2. chronic/nonunion versus physician-confirmed acute/new records only;
3. exclusion of uncertain procedure relevance;
4. bone-graft primary outcome versus the broader augmentation composite;
5. leave-one-out influence analysis for the primary 2×2 association;
6. exclusion of records with competing same-admission orthopaedic procedures;
7. comparison of the deterministic pre-validation effect with the physician-adjudicated effect as a measurement-robustness analysis.

Because all currently identified disease-concordant detailed scaphoid operative records occur in 2023-2025, earlier years do not constitute an independent detailed-procedure validation cohort under the supplied exports.

---

# Results

## Deterministic pre-validation cohort audit

The broad scaphoid retrieval contained 88 admission episodes. Before physician review, deterministic anatomy rules classified 68 as wrist scaphoid, 13 as foot navicular, and 7 as ambiguous. Within the 68 deterministic wrist records, 23 met the pre-validation established chronic/nonunion rule and 45 formed the comparison group.

Thirty-one deterministic wrist-scaphoid records contained a detailed operative-note module. After rule-based target-disease attribution, 28 were considered disease-concordant detailed operative records: 15 chronic/nonunion and 13 comparison. All 28 occurred in 2023-2025.

These values describe the pre-validation audit only. **Final physician-defined cohort counts will be inserted after Stage-1 and Stage-2 adjudication.**

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

In the deterministic pre-validation audit, the major procedure-component count had a median of 2.0 (IQR 1.0-2.0) in chronic/nonunion records and 1.0 (IQR 1.0-1.0) in comparison records. Final secondary estimates will be regenerated from physician labels.

## Acute-only sensitivity analysis

The deterministic audit found explicit acute/recent-injury wording in 7/13 current operative comparison records. The prespecified acute-only analysis will use physician-confirmed acute/new records after Stage-2 adjudication.

**Acute-only effect estimate: [pending].**

---

# Discussion

## Principal finding

The principal finding will be finalized after the physician-defined clinical cohort is frozen. The central hypothesis is that established chronic/nonunion wrist-scaphoid disease is associated with **additional biological augmentation**, rather than a large difference in whether fixation is used at all.

If the physician-adjudicated result preserves the current signal, the main interpretation will be:

> Internal fixation remained common across surgically treated wrist-scaphoid presentations, whereas established chronic/nonunion disease was associated with substantially greater use of bone-graft augmentation.

This formulation does not imply that chronicity causes graft use or that grafting improves postoperative outcome.

## Clinical interpretation

The proposed pattern is biologically plausible. Fixation primarily provides mechanical stability, whereas grafting can contribute osteogenic/osteoconductive material, restore bone stock, and support reconstruction in biologically or structurally compromised nonunion. Contemporary reviews and algorithms recommend tailoring graft strategy to vascularity, proximal-pole viability, defect size, deformity, and prior treatment rather than applying a single approach to all nonunions.[1-6]

The contribution of the present study is therefore not the generic observation that bone graft can be used in scaphoid nonunion. It tests whether routine operative records reveal a measurable **change in treatment composition** across presentation states: fixation as a common mechanical base with greater graft augmentation in established chronic/nonunion disease.

## Relationship to prior literature

Systematic reviews and comparative studies have largely evaluated union, function, or complications across graft and fixation techniques within established nonunion cohorts.[4-6,10] Survey and population studies demonstrate persistent variation in graft selection and nonunion management.[7-9] The present study uses a different clinical contrast by examining operative composition across wrist-scaphoid presentation states within routine care records.

## Limitations

The study is exploratory because the treatment-composition hypothesis was generated from the same fixed dataset. The operative sample is small and concentrated in 2023-2025 because of the supplied export structure. Long-term union, pain, function, and recurrence are not consistently available and cannot be inferred. Important treatment-selection variables such as standardized displacement, proximal-pole vascularity, humpback deformity, defect size, and quantitative CT geometry are incompletely captured. Clinical state and procedure components depend on physician interpretation of routine documentation. The single-center retrospective design limits generalizability.

The two-stage physician-reference design reduces one potential source of bias by ensuring that deterministic anatomy rules do not predefine the downstream clinical cohort. It does not eliminate confounding by unmeasured disease severity or surgeon preference.

## Conclusion

**Pending physician adjudication.** Final conclusions will remain limited to the association between presentation state and documented operative composition and will not make claims about treatment efficacy or prediction of future nonunion.

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
