# Operative Composition Across Acute and Established Chronic/Nonunion Wrist-Scaphoid Presentations: A Retrospective Study of Fixation and Bone-Graft Augmentation

**Draft:** v0.4, before completion of the physician reference standard  
**Design:** retrospective, fixed-data, exploratory observational study  
**Primary outcome:** bone-graft augmentation  
**Key contrast:** internal fixation  
**Secondary hypothesis:** documented wrist-related duration within established chronic/nonunion

> Deterministic values reported below are pre-validation observations that motivated the study. Final cohort sizes and effect estimates will be regenerated from adjudicated physician Gold using `SCAPHOID_ANALYSIS_PLAN_V0_3.md`.

---

## Abstract

### Background

Scaphoid nonunion surgery must address mechanical stability and, in selected cases, the biological or structural deficits that justify bone-graft augmentation. Internal fixation is widely used, whereas graft selection varies with nonunion characteristics and surgeon practice. Most published studies evaluate graft technique or outcome within cohorts already defined as nonunion.

### Purpose

To determine whether the **composition of documented surgery** differs between physician-confirmed acute/new wrist-scaphoid fractures and established chronic/nonunion presentations, specifically whether bone-graft augmentation increases while internal fixation remains common in both groups. A prespecified exploratory secondary analysis evaluates whether graft use within established chronic/nonunion is associated with longer documented wrist-related disease duration.

### Methods

We performed a retrospective study using a fixed set of hospital electronic health record exports. All 88 records retrieved under broad scaphoid terminology undergo physician anatomy adjudication before the final wrist-scaphoid cohort is defined. Downstream clinical-state and operative review is generated only after anatomy Gold is frozen. Clinical state is adjudicated from diagnosis, presenting complaint, and physical examination; operative text is excluded from state assignment. The primary comparison is physician-confirmed established chronic/nonunion versus physician-confirmed acute/new fracture. Detailed operative records contribute to analysis only when the documented operation is adjudicated as treating the wrist scaphoid. The primary outcome is bone-graft augmentation and the key contrast is internal fixation. Sparse binary comparisons use Fisher exact tests and conditional odds ratios. Relevant wrist-related duration is physician adjudicated and analyzed continuously within established chronic/nonunion records.

### Results

The deterministic pre-validation audit identified 88 broad scaphoid candidates, including 68 high-specificity wrist-scaphoid records, 13 foot-navicular records, and 7 anatomically ambiguous records. Within the deterministic wrist cohort, 23 records carried established chronic/nonunion terminology. Twenty-eight records had disease-concordant detailed operative documentation, all from 2023-2025. In the pre-validation operative audit, internal fixation was identified in 14/15 established chronic/nonunion records and 12/13 keyword-negative comparison records, whereas bone grafting was identified in 8/15 established chronic/nonunion records and fewer than five comparison records. Within the deterministic chronic/nonunion subgroup, explicit wrist-related duration was recoverable in 13/15 records; median duration was 182.6 days among graft-positive records and 15.0 days among graft-negative records. These values are provisional and do not define the final physician-adjudicated comparison.

### Conclusions

To be completed after physician-reference adjudication. Final interpretation will be limited to associations between clinical presentation, documented duration, and operative composition. The study does not evaluate postoperative union, treatment efficacy, causal treatment selection, or future nonunion risk.

---

# Introduction

Scaphoid nonunion remains a reconstructive challenge because successful treatment depends on both mechanical stability and a biological environment capable of supporting healing. The vascular anatomy of the scaphoid, particularly around the proximal pole, can make delayed healing consequential, while bone loss, deformity, avascular necrosis, and prior treatment may further increase reconstructive complexity. Contemporary reviews therefore describe internal fixation as a common mechanical foundation of nonunion treatment and bone graft as an adjunct selected according to lesion-specific biological and structural features.[1,2]

Bone grafting is nevertheless not obligatory in every nonunion. Selected stable, well-aligned lesions can unite after rigid fixation without grafting, while graft augmentation may be more relevant in cystic, long-standing, biologically compromised, or structurally deficient nonunions.[3-6] Treatment algorithms also explicitly recognize time from injury as one factor that can increase reconstructive complexity.[7] These observations suggest that the clinically informative transition across presentation states may not be a binary shift from no fixation to fixation. Instead, fixation may remain the common mechanical base while additional biological or reconstructive components are added as disease becomes established.

The literature already documents substantial heterogeneity in nonunion management. A survey of hand surgeons reported near-unanimous use of headless compression screws in many scaphoid settings but marked variation in graft choice for nonunion, revision surgery, and avascular necrosis.[8] An umbrella review found no single graft strategy to be universally superior across nonunion contexts.[9] Claims-based work has also demonstrated variation in imaging utilization and subsequent vascularized graft use among patients undergoing nonunion surgery.[10] Therefore, neither the use of bone graft in scaphoid nonunion nor the clinical relevance of chronicity is novel in itself.

Most prior studies, however, begin with a cohort already defined as scaphoid nonunion and compare graft techniques, fixation methods, union outcomes, or prognostic factors. A complementary question is whether routine clinical records reveal a measurable **change in treatment composition across presentation states**: does the mechanical fixation component remain relatively stable while biological augmentation increases when the presentation is established as chronic/nonunion?

During structured review of a fixed hospital dataset, we observed a preliminary pattern consistent with this dissociation. Internal fixation was frequent across operative wrist-scaphoid records, whereas bone grafting appeared concentrated among records with established chronic/nonunion terminology. We therefore formulated the primary exploratory question before physician-reference scoring: **among physician-confirmed wrist-scaphoid operations, is established chronic/nonunion associated with greater bone-graft augmentation than physician-confirmed acute/new fracture while internal fixation remains common in both groups?**

After the primary outcome was fixed, a separate pre-validation audit suggested heterogeneity within established chronic/nonunion: graft-positive records contained longer documented wrist-related disease duration than graft-negative records. We therefore froze duration as an exploratory secondary hypothesis before Stage-2 physician adjudication. This analysis is intended to characterize heterogeneity in real-world treatment composition, not to derive a grafting threshold or treatment rule.

---

# Methods

## Study design and data source

We conducted a retrospective, fixed-data observational study using hospital electronic health record exports spanning 2015-2025. The source package contained structured demographic and diagnostic data, free-text presenting complaints and specialist physical examinations, operation names, and detailed operative notes. Examination/imaging-report and laboratory exports were also available, but the fixed dataset did not contain sufficiently complete longitudinal postoperative outcomes for a study of union or treatment efficacy.

No additional local clinical data are assumed to become available. Raw patient-level records, identifiers, dates, physician-review files, and clinical free text remain within the private analytic environment. The public repository contains code, protocol documents, and privacy-preserving aggregate outputs only.

**Ethics:** [Institutional review board / ethics approval, waiver, and data-governance information to be inserted from the approved study documentation.]

## Broad scaphoid retrieval

The hospital extraction returned 88 candidate admission episodes under broad scaphoid terminology. In Chinese clinical documentation, terminology corresponding to scaphoid/navicular can refer to either the wrist scaphoid or the foot navicular. Anatomical adjudication was therefore required before disease-state or treatment comparisons.

The deterministic v0.3 audit, retained only as pre-validation engineering evidence, classified 68 candidates as high-specificity wrist scaphoid, 13 as explicit foot navicular, and 7 as anatomically ambiguous.

## Two-stage physician reference standard

To prevent verification bias, deterministic-rule positivity does not define the final clinical cohort.

### Stage 1: anatomy adjudication

All 88 broad candidates are reviewed by a physician blinded to deterministic predictions and clinical effect estimates. Each record is assigned one anatomy category:

- wrist scaphoid;
- foot navicular;
- other;
- uncertain.

An approximately 20% hash-selected subset undergoes independent second review. Reviewer-1 and Reviewer-2 labels are retained separately. Records with complete agreement inherit the agreed label; non-double-reviewed records inherit the Reviewer-1 label; disagreements remain blank in a separate adjudication file until resolved by a prespecified adjudicator. The Stage-1 anatomy Gold file is then cryptographically frozen.

The 88-record Stage-1 input and its prespecified 18-record double-review selection were frozen before annotation while all anatomy Gold fields were blank.

### Stage 2: state, duration, and procedure adjudication

Only after Stage-1 Gold is frozen are downstream review packets generated for **physician-confirmed wrist-scaphoid records**. Consequently, Stage-2 sample sizes are determined by physician anatomy rather than by the deterministic 68-record wrist cohort.

Approximately 20% of state/duration and procedure records undergo independent second review using the same separation of Reviewer-1, Reviewer-2, and adjudicated Gold.

## Clinical-state definition

Clinical state is adjudicated using diagnosis, presenting complaint, and specialist physical examination only. Operation names and detailed operative notes are excluded from state assignment because treatment is the downstream variable of interest.

State categories are:

1. `acute_or_new_fracture`;
2. `established_chronic_fracture`;
3. `established_nonunion`;
4. `chronic_nonunion_not_distinguishable`;
5. `insufficient_or_uncertain`.

The **established chronic/nonunion** group combines categories 2-4. The primary comparison group consists only of physician-confirmed `acute_or_new_fracture` records. Records labelled `insufficient_or_uncertain` are retained for measurement accounting but excluded from state-based clinical inference.

This comparison definition was finalized before Stage-2 physician Gold. An earlier draft plan described a broad classifiable comparison plus an acute-only sensitivity analysis; because the final physician vocabulary makes every classifiable non-chronic record acute/new, those two analyses would be identical. The redundant sensitivity analysis was removed before any physician-adjudicated treatment effect was inspected.

## Operative-record attribution

The presence of a detailed operative-note module does not by itself establish that the documented procedure treated the wrist scaphoid. The same admission may contain surgery for another orthopaedic problem.

For each physician-confirmed wrist-scaphoid record with detailed operative documentation, reviewers first assign:

`target_disease_procedure_present = yes / no / uncertain`.

Only records adjudicated `yes` contribute to the clinical treatment-composition analysis. Notes for another anatomical problem remain available as hard negatives for measurement validation but do not enter procedure prevalence estimates.

## Primary outcome: bone-graft augmentation

Bone-graft augmentation is defined as explicit documentation of bone graft or bone harvest used as part of the wrist-scaphoid operation.

This outcome was selected before Stage-2 physician scoring and cannot be replaced by a composite according to the final P value.

## Key contrast: internal fixation

Internal fixation includes screw, headless/cannulated screw, wire, or other explicitly documented fixation used in the target wrist-scaphoid operation.

The prespecified scientific contrast tests whether fixation remains a common mechanical base in both acute/new and established chronic/nonunion states while graft augmentation changes.

## Secondary operative outcomes

Secondary variables include:

- reconstruction;
- fusion/arthrodesis;
- an augmentation composite of bone graft, reconstruction, or fusion;
- the number of major operative components among fixation, graft, reconstruction, and fusion.

Secondary outcomes remain secondary regardless of statistical significance.

## Physician-adjudicated duration variable

A prespecified exploratory secondary analysis evaluates disease-duration heterogeneity within established chronic/nonunion operative records.

During Stage-2 state review, physicians record:

- whether a clearly wrist-related duration is present (`yes/no/uncertain`);
- numeric duration value;
- unit (`hours/days/weeks/months/years`);
- basis (`injury_since_event`, `wrist_symptom_duration`, `both`, or `uncertain`).

If more than one duration is documented, the reviewer records the longest clearly wrist-scaphoid-related index injury or symptom duration present at admission. A recent flare is not substituted for a clearly documented longer disease history. Automated duration-parser output is not displayed to reviewers.

Duration is converted to days after adjudication using fixed unit conversions and analyzed continuously. No local cutoff is selected to optimize P value, AUROC, Youden index, or classification performance.

## Operative analysis population

A record enters the primary operative analysis if all of the following are satisfied:

1. physician-confirmed wrist scaphoid;
2. physician-confirmed established chronic/nonunion or acute/new state;
3. detailed operative-note module available;
4. physician-adjudicated target-disease procedure relevance = yes.

For any specific procedure component, an `uncertain` component label is excluded from that component's denominator rather than coded as no.

## Statistical analysis

Categorical variables are summarized as n (%), with explicit evaluable denominators. Continuous variables are summarized as median and interquartile range unless their distribution justifies mean and standard deviation.

### Primary analysis

Bone-graft augmentation is compared between established chronic/nonunion and acute/new operative records using a two-sided Fisher exact test. The manuscript analysis reports the conditional odds ratio and 95% confidence interval when estimable. No continuity correction is silently applied to zero-cell tables.

### Key contrast

Internal fixation is analyzed using the same sparse-table approach.

### Secondary treatment intensity

The major procedure-component count is summarized as median (IQR) and compared using the Mann-Whitney U test.

### Duration analysis

Within established chronic/nonunion operative records, physician-valid duration is compared between graft-positive and graft-negative records using median (IQR) and the Mann-Whitney U test. An injury-basis-only analysis may be reported if both graft groups retain interpretable data.

### Robustness

Prespecified robustness checks include:

1. primary bone-graft outcome versus the broader augmentation composite;
2. leave-one-out influence analysis of the primary 2×2 table;
3. exclusion of records with competing same-admission orthopaedic procedures;
4. comparison of deterministic pre-validation versus physician-adjudicated effect estimates as a measurement-robustness analysis;
5. injury-duration-only secondary analysis when feasible.

There is no separate acute-only sensitivity analysis because physician-confirmed acute/new fracture is the primary comparison definition.

No high-capacity predictive model or automated model-selection procedure is used for the primary clinical analysis.

## Reference-standard freeze and reproducibility

Stage-1 and final reference standards undergo controlled-vocabulary, ID-population, double-review-manifest, and duration-consistency validation before SHA-256 freezing. Final analysis is executed by the versioned post-Gold analysis script only after the reference standard passes these checks.

Exact manuscript results are written to a private analysis artifact. Public repository outputs apply small-cell and small-denominator suppression.

---

# Results

## Pre-validation cohort audit

The broad retrieval contained 88 candidate admissions. Deterministic anatomy rules classified 68 as wrist scaphoid, 13 as foot navicular, and 7 as ambiguous. Within the deterministic wrist group, 23 records contained established chronic/nonunion terminology.

Thirty-one deterministic wrist-scaphoid records contained a detailed operative-note module. After deterministic target-disease attribution, 28 detailed operative records were considered wrist-scaphoid-concordant. All 28 occurred in 2023-2025.

These values describe the engineering audit and do not define the final physician cohort.

**Final physician-defined anatomy and state flow: [pending].**

## Pre-validation treatment-composition signal

In the deterministic operative audit, internal fixation was identified in 14/15 (93.3%) established chronic/nonunion records and 12/13 (92.3%) keyword-negative comparison records. Bone grafting was identified in 8/15 (53.3%) established chronic/nonunion records and fewer than five comparison records.

The comparison records in this pre-validation audit were not uniformly proven acute; the physician-adjudicated primary analysis will therefore use only records explicitly classified as acute/new.

### Final primary bone-graft result

**Established chronic/nonunion: [pending] / [pending]**  
**Acute/new: [pending] / [pending]**  
**Conditional OR [pending], 95% CI [pending], Fisher P [pending].**

### Final internal-fixation contrast

**Established chronic/nonunion: [pending] / [pending]**  
**Acute/new: [pending] / [pending]**  
**Conditional OR [pending], 95% CI [pending], Fisher P [pending].**

## Secondary operative composition

**Augmentation composite and major component count: [pending].**

## Duration-related heterogeneity within established chronic/nonunion

The corrected deterministic audit identified an explicit wrist-related duration in 13/15 chronic/nonunion operative records. Duration was recoverable in 7/8 graft-positive records, with a median of 182.6 days (IQR 167.4-1004.4), and in 6/7 graft-negative records, with a median of 15.0 days (IQR 2.3-41.0).

These values motivated the frozen secondary hypothesis but are not final clinical estimates.

**Physician-adjudicated duration result: [pending].**

## Robustness analyses

**Leave-one-out, competing-procedure exclusion, deterministic-versus-Gold comparison, and injury-basis duration analysis: [pending].**

---

# Discussion

## Principal finding

The principal finding will be finalized after physician adjudication. The central hypothesis is that the transition from acute/new wrist-scaphoid fracture to established chronic/nonunion is reflected more strongly in the addition of biological augmentation than in the use of mechanical fixation itself.

If the physician-adjudicated results preserve the preliminary pattern, the principal interpretation will be:

> Internal fixation remained common across acute/new and established chronic/nonunion wrist-scaphoid operations, whereas bone-graft augmentation was substantially more frequent in established disease.

This statement describes treatment composition and does not imply that chronicity causes graft use or that grafting improves outcome.

## Relation to existing evidence

The observation that bone graft is used in scaphoid nonunion is established and is not presented as novel. Contemporary reviews describe internal fixation plus supplemental graft as common in nonunion reconstruction, with graft strategy tailored to vascularity, proximal-pole viability, deformity, defect geometry, and prior treatment.[1,2] Systematic and umbrella reviews have not established one universally superior graft strategy.[9] Practice surveys and utilization studies also demonstrate substantial heterogeneity in graft selection.[8,10]

The present study instead uses a different analytical contrast: it decomposes documented surgery across presentation states into a **mechanical fixation component** and **additional biological augmentation**. This framing tests which component changes in routine care rather than comparing graft techniques within an already-selected nonunion cohort.

## Duration-related heterogeneity

If physician review preserves the duration signal, the secondary finding would indicate that established chronic/nonunion itself is heterogeneous: graft augmentation may be concentrated among records with longer documented disease duration. This would be compatible with published treatment concepts in which increasing chronicity, bone loss, cystic change, deformity, or compromised biology can increase reconstructive requirements.[6,7]

Duration cannot be treated as an independent causal determinant in this dataset. It may proxy unmeasured imaging severity, sclerosis, cystic change, avascular necrosis, prior treatment, or surgeon preference. The study therefore does not derive a grafting threshold from the local duration data.

## Strengths

The study is deliberately constrained to what the fixed data can support. Physician state is assigned without operative-text leakage, target-disease procedure relevance is adjudicated before procedure components are counted, and the final cohort is defined by a two-stage physician process rather than by deterministic-rule positivity. Primary and secondary hypotheses, comparison definitions, and analysis hierarchy are versioned before Stage-2 Gold completion. Reviewer-1, Reviewer-2, and adjudicated labels are preserved separately.

## Limitations

The hypothesis was generated from the same fixed dataset and is therefore exploratory. The final operative sample is expected to be small, and the available detailed operative records are concentrated in 2023-2025. The dataset does not support consistent postoperative union, pain, function, or recurrence outcomes. Standardized imaging features that strongly influence graft selection—including displacement, proximal-pole vascularity, humpback deformity, defect size, and cystic change—are incompletely available in a form suitable for systematic analysis. Consequently, observed associations may reflect unmeasured disease severity and surgeon preference. Duration derived from routine clinical documentation may represent injury age, symptom duration, or both, even after physician adjudication. The study is single-center and may not generalize to other practice settings.

## Conclusion

**Pending physician adjudication.** If validated, the study will support a limited descriptive conclusion about real-world operative composition: internal fixation may remain the common mechanical base across presentation states, whereas established chronic/nonunion is associated with greater biological augmentation. Any duration-related heterogeneity will remain exploratory and non-causal.

---

# References

1. Ayalon O, Rettig SA, Tedesco LJ. Bone Graft and Fixation Options in the Surgical Management of Scaphoid Nonunion. *J Am Acad Orthop Surg*. 2024. PMID: 39531592. doi:10.5435/JAAOS-D-24-00510.
2. Miller EA, Huang JI. Traditional Bone Grafting in Scaphoid Nonunion. *Hand Clin*. 2024;40(1):105-116. PMID: 37979982. doi:10.1016/j.hcl.2023.08.001.
3. A systematic review of mechanical stabilization by screw fixation without bone grafting in the management of stable scaphoid non-union. 2021. PMID: 33816106.
4. Bone grafting for scaphoid nonunion surgery: a systematic review and meta-analysis. 2022. PMID: 35491585.
5. Higgins JP. When to Use Vascularized Bone? An Algorithm for Scaphoid Nonunion Surgery. *J Wrist Surg*. 2025. PMID: 41574159. doi:10.1055/a-2640-4238.
6. Necessity of grafting in scaphoid nonunion fixation: A comparative outcome analysis. 2026. PMID: 41695733.
7. Scaphoid Reconstruction. 2019. PMID: 31739880.
8. Strelzow JA, et al. Scaphoid Fractures and Nonunion: A Survey-based Review of Hand Surgeon's Practice and the Evidence. 2024. PMID: 39703594. doi:10.1016/j.jhsg.2024.06.013.
9. Graft choice for managing scaphoid non-union: umbrella review. 2024. PMID: 39122186.
10. Shapiro LM, et al. MRI for Scaphoid Nonunion: Utilization Rates, Factors Associated With Utilization, and Subsequent Vascularized Bone Graft Use. *J Hand Surg Am*. 2025;50(2):182-187. PMID: 39614839. doi:10.1016/j.jhsa.2024.10.008.
11. Compression screw fixation without bone grafting for scaphoid fracture nonunion. 2015. PMID: 26330777.
