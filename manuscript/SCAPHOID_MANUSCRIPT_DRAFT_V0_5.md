# Operative Composition Across Acute and Established Chronic/Nonunion Wrist-Scaphoid Presentations: A Retrospective Study of Fixation and Bone-Graft Augmentation

**Draft:** v0.5, before completion of the physician reference standard  
**Design:** retrospective observational study using routinely collected hospital EHR data  
**Primary outcome:** bone-graft augmentation  
**Key contrast:** internal fixation  
**Exploratory secondary hypothesis:** documented wrist-related duration within established chronic/nonunion

> Deterministic values reported below are pre-validation observations that motivated the study. Final cohort sizes, effect estimates, tables, figures, and conclusions will be regenerated from the frozen two-stage physician reference standard under `SCAPHOID_ANALYSIS_PLAN_V0_3.md`.

---

## Abstract

### Background

Scaphoid nonunion surgery must provide mechanical stability and, in selected lesions, biological or structural augmentation. Internal fixation is widely used, whereas bone-graft selection varies with lesion characteristics and surgeon practice. Most published studies evaluate graft technique or outcome within cohorts already defined as nonunion rather than comparing the composition of operative treatment across presentation states.

### Purpose

To determine whether documented operative composition differs between physician-confirmed acute/new wrist-scaphoid fractures and established chronic/nonunion presentations, specifically whether bone-graft augmentation increases while internal fixation remains common in both groups. A prespecified exploratory secondary analysis evaluates whether graft use within established chronic/nonunion is associated with longer documented wrist-related disease duration.

### Methods

We conducted a retrospective observational study using a fixed export of routinely collected hospital electronic health-record data. Records from diagnostic, presenting-complaint/physical-examination, and operative modules were linked at the admission-episode level. All 88 records retrieved under broad scaphoid terminology undergo physician anatomy adjudication before the final wrist-scaphoid cohort is defined. Downstream clinical-state and operative review is generated only after anatomy Gold is frozen. State is adjudicated from diagnosis, presenting complaint, and physical examination; operative text is excluded from state assignment. The primary comparison is physician-confirmed established chronic/nonunion versus physician-confirmed acute/new fracture. Detailed operative records contribute only when the documented procedure is adjudicated as treating the wrist scaphoid. The primary outcome is bone-graft augmentation and the key contrast is internal fixation. Sparse binary comparisons use two-sided Fisher exact tests and conditional odds ratios with 95% confidence intervals. Physician-adjudicated wrist-related duration is analyzed continuously within established chronic/nonunion records.

### Results

The deterministic pre-validation audit identified 88 broad scaphoid candidates, including 68 high-specificity wrist-scaphoid records, 13 foot-navicular records, and 7 anatomically ambiguous records. Twenty-eight deterministic records had disease-concordant detailed operative documentation, all from 2023-2025. In this pre-validation audit, internal fixation was identified in 14/15 established chronic/nonunion operative records and 12/13 keyword-negative comparison records, whereas bone grafting was identified in 8/15 chronic/nonunion records and fewer than five comparison records. The comparison records were not uniformly proven acute and therefore do not define the final clinical comparison. Within the deterministic chronic/nonunion subgroup, explicit wrist-related duration was recoverable in 13/15 records; median duration was 182.6 days among graft-positive records and 15.0 days among graft-negative records. All values remain provisional pending physician adjudication.

### Conclusions

To be completed after physician-reference adjudication. Final interpretation will be restricted to associations between physician-confirmed presentation state, documented duration, and operative composition. The study does not evaluate postoperative union, treatment efficacy, causal treatment selection, or future nonunion risk.

---

# Introduction

Scaphoid nonunion remains a reconstructive challenge because successful treatment depends on both mechanical stability and a biological environment capable of supporting healing. The vascular anatomy of the scaphoid, particularly around the proximal pole, can make delayed healing consequential, while bone loss, deformity, avascular necrosis, and prior treatment may further increase reconstructive complexity. Contemporary reviews therefore describe internal fixation as a common mechanical foundation of nonunion treatment and bone graft as an adjunct selected according to lesion-specific biological and structural features.[1,2]

Bone grafting is nevertheless not obligatory in every nonunion. Selected stable, well-aligned lesions can unite after rigid fixation without grafting, while graft augmentation may be more relevant in cystic, long-standing, biologically compromised, or structurally deficient nonunions.[3-6] Treatment algorithms also recognize disease duration as one factor that may accompany increasing reconstructive complexity.[7] These observations suggest that the clinically informative transition across presentation states may not be a binary shift from no fixation to fixation. Instead, fixation may remain the common mechanical base while biological or reconstructive components are added as disease becomes established.

The literature already documents substantial heterogeneity in nonunion management. A survey of hand surgeons reported broad agreement on headless compression screw fixation in common scaphoid settings but marked variation in graft choice for nonunion, revision surgery, and avascular necrosis.[8] An umbrella review found no single graft strategy to be universally superior across nonunion contexts.[9] Accordingly, neither the use of bone graft in scaphoid nonunion nor the clinical relevance of chronicity is novel in itself.

Most prior studies, however, begin with a cohort already defined as scaphoid nonunion and compare graft techniques, fixation methods, union outcomes, or prognostic factors. A complementary observational question is whether routine clinical records reveal a measurable **change in treatment composition across presentation states**: does the mechanical fixation component remain common while biological augmentation increases when the presentation is established as chronic/nonunion?

During structured review of a fixed hospital dataset, we observed a preliminary pattern consistent with this dissociation. Internal fixation was frequent across operative wrist-scaphoid records, whereas bone grafting appeared concentrated among records with established chronic/nonunion terminology. We therefore formulated the primary exploratory question before physician-reference scoring: **among physician-confirmed wrist-scaphoid operations, is established chronic/nonunion associated with greater bone-graft augmentation than physician-confirmed acute/new fracture while internal fixation remains common in both groups?**

After the primary outcome was fixed, a separate pre-validation audit suggested heterogeneity within established chronic/nonunion: graft-positive records contained longer documented wrist-related disease duration than graft-negative records. Duration was therefore frozen as an exploratory secondary hypothesis before Stage-2 physician adjudication. This analysis is intended to characterize treatment heterogeneity, not to derive a grafting threshold or treatment rule.

---

# Methods

## Study design, setting, and data source

We conducted a retrospective, fixed-data observational study using routinely collected hospital electronic health-record exports spanning 2015-2025. The source package was a fixed research export rather than direct unrestricted access to the live hospital information system. It contained structured demographic and diagnostic fields, free-text presenting complaints and specialist physical examinations, operation names, and detailed operative notes. Examination/imaging-report and laboratory exports were also available, but the supplied data did not contain sufficiently complete longitudinal postoperative outcomes for an analysis of union, healing time, pain, function, or treatment efficacy.

The source archive spans 2015-2025, but module availability was not continuous across this interval. The supplied exports show a structural discontinuity in several clinical modules during approximately 2019-2022. In the deterministic pre-validation audit, all disease-concordant detailed wrist-scaphoid operative records occurred in 2023-2025. We therefore distinguish the **source archive period** from the **effective detailed-operative analytic period** and do not treat earlier years as an independent validation cohort.

No additional local clinical data are assumed to become available. Raw patient-level records, identifiers, dates, pseudonymous study IDs, physician-review files, and clinical free text remain within the private analytic environment. Public repository materials contain code, protocol documents, tests, and privacy-preserving aggregate outputs only.

**Ethics:** [Institutional review board / ethics committee name, approval number, consent requirement or waiver, and data-governance information to be inserted from the approved study documentation.]

## Data access, linkage, and cleaning

Records from the diagnostic/basic-information, presenting-complaint/physical-examination, and operative exports were linked deterministically using the supplied admission-episode identifier. The statistical unit is the admission episode, not the source-table row. Because the routine exports contain one-to-many diagnostic, laboratory, imaging, and operative rows, repeated source rows were retained as child records or aggregated to episode-level variables rather than counted as independent patients.

The pre-validation data audit demonstrated substantial row inflation in the raw diagnostic/basic-information exports, including approximately 13.4 source rows per unique scaphoid admission. This finding motivated explicit episode-level reconstruction before any clinical comparison. Data cleaning additionally included normalization of admission identifiers, range checks for structured variables such as body mass index, preservation of missingness, anatomical disambiguation of broad scaphoid/navicular terminology, and separation of operative-module availability from target-disease procedure relevance.

Structural absence of a module was not imputed as clinical absence. Similarly, failure to document a clinical concept in routine free text was not automatically interpreted as evidence that the concept was absent.

## Broad scaphoid retrieval

The hospital extraction returned 88 candidate admission episodes under broad scaphoid terminology. In Chinese clinical documentation, “舟骨” may refer to either the wrist scaphoid or the foot navicular. Anatomical adjudication was therefore required before disease-state or treatment comparisons.

The deterministic v0.3 audit, retained only as pre-validation engineering evidence, classified 68 candidates as high-specificity wrist scaphoid, 13 as explicit foot navicular, and 7 as anatomically ambiguous. These deterministic categories do not define the final clinical cohort.

## Two-stage physician reference standard

To reduce verification bias, deterministic-rule positivity does not determine which records can enter the final physician-defined wrist cohort.

### Stage 1: anatomy adjudication

All 88 broad candidates are reviewed by a physician blinded to deterministic predictions and clinical effect estimates. Each record is assigned one anatomy category:

- `wrist_scaphoid`;
- `foot_navicular`;
- `other`;
- `uncertain`.

An approximately 20% hash-selected subset undergoes independent second review. Reviewer-1 and Reviewer-2 labels are retained separately. For non-double-reviewed records, Reviewer-1 provides the provisional label; for double-reviewed records with complete agreement, the agreed label is carried forward. Disagreements remain unresolved in a separate adjudication file until explicit review by the prespecified adjudicator or consensus process. The Stage-1 anatomy Gold file is then cryptographically frozen.

The 88-record Stage-1 input population and its prespecified 18-record second-review selection were frozen before annotation while all anatomy Gold fields were blank.

### Stage 2: state, duration, and procedure adjudication

Only after Stage-1 anatomy Gold is frozen are downstream review packets generated for **physician-confirmed wrist-scaphoid records**. Thus, the final state-review population is determined by physician anatomy rather than by the deterministic 68-record wrist cohort.

Approximately 20% of state/duration and procedure records undergo independent second review using the same separation of Reviewer-1, Reviewer-2, and final adjudicated Gold. Inter-rater agreement is assessed before adjudication; disagreements are not resolved by silent majority voting.

## Clinical-state definition

Clinical state is adjudicated using diagnosis, presenting complaint, and specialist physical examination only. Operation names and detailed operative notes are excluded from state assignment because operative treatment is the downstream variable of interest.

State categories are:

1. `acute_or_new_fracture`;
2. `established_chronic_fracture`;
3. `established_nonunion`;
4. `chronic_nonunion_not_distinguishable`;
5. `insufficient_or_uncertain`.

The **established chronic/nonunion** group combines categories 2-4. The primary comparison group consists only of physician-confirmed `acute_or_new_fracture` records. Records labelled `insufficient_or_uncertain` are retained for reporting of measurement completeness but excluded from state-based clinical inference.

This comparison definition was finalized before Stage-2 physician Gold was completed. An earlier draft described a broader classifiable comparison plus an acute-only sensitivity analysis; because the final physician vocabulary makes the clean classifiable non-established comparator the acute/new category, the redundant sensitivity analysis was removed before any physician-adjudicated treatment effect was inspected.

## Operative-record attribution

The presence of a detailed operative-note module does not establish that the documented procedure treated the wrist scaphoid. A single admission may include surgery for another orthopaedic problem.

For each physician-confirmed wrist-scaphoid record with detailed operative documentation, reviewers first assign:

`target_disease_procedure_present = yes / no / uncertain`.

Only records adjudicated `yes` contribute to the clinical treatment-composition analysis. Notes documenting another anatomical procedure remain informative for measurement validation but do not enter wrist-scaphoid procedure prevalence estimates.

## Primary outcome: bone-graft augmentation

Bone-graft augmentation is defined as explicit documentation of bone graft or bone harvest used as part of the target wrist-scaphoid operation.

This outcome was selected before Stage-2 physician scoring and cannot be replaced by a broader composite according to the final P value.

## Key contrast: internal fixation

Internal fixation includes screw, headless or cannulated screw, wire, or another explicitly documented fixation construct used in the target wrist-scaphoid operation.

The prespecified clinical contrast tests whether internal fixation remains a common mechanical base in both acute/new and established chronic/nonunion states while bone-graft augmentation differs.

## Secondary operative outcomes

Secondary variables include:

- reconstruction;
- fusion/arthrodesis;
- an augmentation composite of bone graft, reconstruction, or fusion;
- number of major operative components among fixation, graft, reconstruction, and fusion.

These outcomes remain secondary irrespective of statistical significance.

## Physician-adjudicated duration variable

A prespecified exploratory secondary analysis evaluates disease-duration heterogeneity within established chronic/nonunion operative records.

During Stage-2 state review, physicians record:

- whether a clearly wrist-scaphoid-related duration is present (`yes/no/uncertain`);
- numeric duration value;
- unit (`hours/days/weeks/months/years`);
- basis (`injury_since_event`, `wrist_symptom_duration`, `both`, or `uncertain`).

If more than one duration is documented, the reviewer records the longest duration clearly attributable to the index wrist-scaphoid injury or related wrist symptoms. A recent flare is not substituted for a clearly documented longer index history. Automated duration-parser output is not displayed to physician reviewers.

After adjudication, duration is converted to days using fixed unit conversions and analyzed continuously. No local cut point is selected by optimizing P value, area under the receiver-operating-characteristic curve, Youden index, or classification accuracy. Any literature-anchored one-year split, if shown, is descriptive only and cannot replace the continuous analysis.

## Operative analysis population

A record enters the primary operative analysis only if all of the following are satisfied:

1. physician-confirmed wrist scaphoid;
2. physician-confirmed established chronic/nonunion or acute/new state;
3. detailed operative-note module available;
4. physician-adjudicated target-disease procedure relevance = `yes`.

For any specific procedure component, an `uncertain` component label is excluded from that component's evaluable denominator rather than coded as `no`.

## Study size

Study size was determined by the complete fixed hospital export available for the prespecified broad scaphoid retrieval. No prospective sample-size target, post-hoc power-based inclusion criterion, or sample-size expansion based on the observed effect was used. The final operative denominator is determined solely by the two-stage physician anatomy, state, and procedure-relevance definitions.

## Missing data

Missingness is handled according to the data-generating mechanism rather than by a single imputation rule.

1. Structurally absent EHR modules are not imputed.
2. `insufficient_or_uncertain` state is excluded from the state-based comparison and reported as such.
3. Target-disease procedure relevance of `no` or `uncertain` does not enter clinical treatment-composition denominators.
4. A procedure component labelled `uncertain` is excluded only from that component's evaluable denominator and is not recoded as negative.
5. Missing BMI or other structured baseline variables are summarized with explicit available denominators and are not imputed.
6. Missing or uninterpretable relevant duration excludes the record only from the duration secondary analysis; it remains eligible for the primary treatment-composition analysis if all primary criteria are met.

## Statistical analysis

Categorical variables are summarized as n/N (%), with explicit evaluable denominators. Continuous variables are summarized as median and interquartile range unless their scale and distribution justify alternative summaries.

### Primary analysis

Bone-graft augmentation is compared between established chronic/nonunion and acute/new operative records using a two-sided Fisher exact test. The manuscript reports the conditional odds ratio and 95% confidence interval when estimable. No continuity correction is silently applied to zero-cell tables.

### Key contrast

Internal fixation is analyzed using the same sparse-table approach.

### Secondary treatment intensity

The major procedure-component count is summarized as median (IQR) and compared using the two-sided Mann-Whitney U test.

### Duration analysis

Within established chronic/nonunion operative records, physician-valid duration is compared between graft-positive and graft-negative records using median (IQR) and the two-sided Mann-Whitney U test. An injury-basis-only analysis may be shown when both groups retain interpretable data.

### Robustness analyses

Prespecified robustness analyses include:

1. primary bone-graft outcome versus the broader augmentation composite;
2. leave-one-out influence analysis of the primary 2×2 association;
3. exclusion of records with competing same-admission orthopaedic procedures when this status can be defined independently of the observed treatment effect;
4. comparison of deterministic pre-validation versus physician-adjudicated estimates as measurement robustness;
5. injury-basis-only duration analysis when feasible.

There is no separate acute-only sensitivity analysis because physician-confirmed acute/new fracture is the primary comparison definition.

No stepwise selection, high-dimensional multivariable model, random forest, gradient-boosting model, neural network, or automated model-selection procedure is used to answer the primary clinical question. Given the expected small operative sample and incompletely measured lesion severity, a multivariable model would not be used to imply control of unmeasured confounding.

## Bias-control strategy

Several sources of bias are anticipated because the data were collected for routine care rather than for this research question.

**Anatomical misclassification:** broad “舟骨” terminology includes wrist and foot anatomy. This is addressed by physician review of all 88 broad candidates before downstream selection.

**Verification bias:** restricting physician review to deterministic wrist-rule positives could cause the algorithm to predefine the clinical population. This is addressed by Stage-1 physician review of the complete broad candidate set, with Stage 2 generated only from physician anatomy Gold.

**Procedure-attribution bias:** a detailed operative note may document treatment of another anatomical problem. This is addressed by independent target-disease procedure-relevance adjudication before component labels are used clinically.

**Documentation/information bias:** absence of a phrase in routine text does not necessarily indicate absence of the clinical feature. Explicit `uncertain` categories are therefore retained and are not converted to negative values.

**Temporal data-availability bias:** the supplied export has a structural module discontinuity, and disease-concordant detailed operative documentation is concentrated in the later period. This is reported directly; missing modules are not imputed, and earlier years are not treated as an independent replication cohort.

**Confounding by indication:** lesion severity, vascularity, displacement, humpback deformity, bone defect size, cystic change, prior treatment, and surgeon preference are not fully standardized in the fixed data. Consequently, observed associations between presentation state and graft use cannot be interpreted as independent causal effects of chronicity.

**Hypothesis-generation bias:** the primary bone-graft question arose from deterministic exploration of the same fixed dataset. The work is therefore explicitly exploratory. The physician-reference workflow, primary outcome, comparison definition, and analysis hierarchy were frozen before physician-adjudicated effect scoring, but final P values do not constitute independent external confirmation.

## Reference-standard freeze and reproducibility

Stage-1 and final physician reference standards undergo controlled-vocabulary, population-ID, second-review-manifest, and duration-consistency validation before SHA-256 freezing. Final analysis is executed only after these checks pass using the versioned post-Gold analysis entrypoint.

Exact manuscript results and unsuppressed figures are written to private analysis paths. Public repository outputs apply small-cell and small-denominator suppression. The public repository provides the cohort logic, validation scripts, statistical code, tests, and aggregate audit outputs required to reproduce the analytic workflow without exposing protected clinical records.

---

# Results

## Pre-validation cohort audit

The broad retrieval contained 88 candidate admissions. Deterministic anatomy rules classified 68 as wrist scaphoid, 13 as foot navicular, and 7 as ambiguous. Within the deterministic wrist group, 23 records contained established chronic/nonunion terminology.

Thirty-one deterministic wrist-scaphoid records contained a detailed operative-note module. After deterministic target-disease attribution, 28 detailed operative records were considered wrist-scaphoid-concordant. All 28 occurred in 2023-2025.

These values describe the engineering audit and do not define the final physician cohort.

**Final physician-defined anatomy/state/operative flow: [pending].**

## Final operative cohort characteristics

**Established chronic/nonunion operative records: [pending].**  
**Acute/new operative records: [pending].**

Age, sex, BMI, and variable-specific available denominators will be reported in Table 1 generated from the frozen physician Gold.

## Pre-validation treatment-composition signal

In the deterministic operative audit, internal fixation was identified in 14/15 (93.3%) established chronic/nonunion records and 12/13 (92.3%) keyword-negative comparison records. Bone grafting was identified in 8/15 (53.3%) established chronic/nonunion records and fewer than five comparison records.

The keyword-negative comparison records were not uniformly proven acute and therefore do not define the final clinical comparison. They are retained only as the hypothesis-generating pre-validation audit.

### Final primary bone-graft result

**Established chronic/nonunion: [pending] / [pending] ([pending]%).**  
**Acute/new: [pending] / [pending] ([pending]%).**  
**Conditional OR [pending], 95% CI [pending], Fisher P [pending].**

### Final internal-fixation contrast

**Established chronic/nonunion: [pending] / [pending] ([pending]%).**  
**Acute/new: [pending] / [pending] ([pending]%).**  
**Conditional OR [pending], 95% CI [pending], Fisher P [pending].**

## Secondary operative composition

**Augmentation composite: [pending].**  
**Major procedure-component count: [pending].**

## Duration-related heterogeneity within established chronic/nonunion

The corrected deterministic audit identified an explicit wrist-related duration in 13/15 chronic/nonunion operative records. Duration was recoverable in 7/8 graft-positive records, with a median of 182.6 days (IQR 167.4-1004.4), and in 6/7 graft-negative records, with a median of 15.0 days (IQR 2.3-41.0).

These values motivated the frozen secondary hypothesis but are not final clinical estimates.

**Physician-adjudicated graft-positive duration: [pending].**  
**Physician-adjudicated graft-negative duration: [pending].**  
**Mann-Whitney P [pending].**

## Robustness analyses

**Leave-one-out influence range: [pending].**  
**Augmentation-composite comparison: [pending].**  
**Deterministic-versus-physician measurement robustness: [pending].**  
**Injury-basis-only duration analysis: [pending if evaluable].**

---

# Discussion

## Principal finding

The principal finding will be finalized after physician adjudication. The central hypothesis is that the transition from acute/new wrist-scaphoid fracture to established chronic/nonunion is reflected more strongly in the addition of biological augmentation than in whether mechanical fixation is used at all.

If the physician-adjudicated results preserve the preliminary pattern, the principal interpretation will be:

> Internal fixation remained common across acute/new and established chronic/nonunion wrist-scaphoid operations, whereas established disease was associated with greater documented bone-graft augmentation.

This statement describes operative composition. It does not imply that chronicity independently causes graft selection or that grafting improves outcome.

## Clinical interpretation

The proposed dissociation is consistent with established reconstructive principles. Internal fixation addresses mechanical stability, while grafting may restore bone stock and provide biological or structural support in lesions with greater biological compromise or deformity. Existing reviews and treatment algorithms already recognize heterogeneity in graft selection. The contribution of this study is therefore not to establish grafting as a treatment for nonunion, but to quantify whether routine operative records show a relatively stable mechanical component and a changing augmentation component across physician-confirmed presentation states.

## Duration as a secondary marker of heterogeneity

If physician adjudication preserves the duration gradient, longer documented wrist-related disease duration would identify a subgroup of established chronic/nonunion records in which graft augmentation was more frequent. This would be biologically plausible but not causal. Duration may co-vary with bone loss, cystic change, deformity, vascularity, prior treatment, and surgeon preference. The study therefore does not derive or validate a duration threshold for grafting.

## Strengths

The study uses a two-stage physician reference standard that prevents deterministic anatomy rules from defining the final clinical cohort. Exposure assignment is separated from operative text, reducing circular classification of treatment and disease state. Operative-note availability is also separated from target-disease procedure relevance, preventing same-admission surgery for another anatomical problem from entering wrist-scaphoid procedure denominators. Finally, the primary outcome, comparison definition, secondary hierarchy, and post-Gold analysis pipeline are versioned and frozen before physician-adjudicated effect scoring.

## Limitations

Several limitations arise directly from the routinely collected nature of the data. First, the study is exploratory because the primary treatment-composition hypothesis was generated from deterministic review of the same fixed dataset. Physician adjudication improves measurement validity but does not provide an independent external confirmation sample.

Second, the operative sample is expected to be small and is concentrated in 2023-2025 because the supplied EHR export has a structural discontinuity in module availability. The analytic cohort therefore represents patients with sufficiently documented target-disease operations rather than all wrist-scaphoid patients treated during the nominal 2015-2025 source period. Selection into the detailed-operative subset may limit generalizability.

Third, routine documentation was not collected specifically to measure the research variables. State, duration, and operative components may be incompletely documented, and missing text may create misclassification. Explicit uncertainty categories reduce forced classification but cannot recover undocumented facts.

Fourth, important determinants of operative choice are incompletely measured. Standardized fracture displacement, proximal-pole viability and vascularity, humpback deformity, bone defect size, cystic change, detailed CT geometry, prior treatment history, and surgeon-specific preference are not consistently available. This creates residual confounding by indication. A larger association between chronic/nonunion presentation and graft use therefore cannot be interpreted as an independent causal effect of chronicity.

Fifth, the fixed dataset lacks sufficiently complete longitudinal union, pain, function, and revision outcomes. The study cannot compare treatment effectiveness, determine whether grafting improves healing, or predict future nonunion.

Finally, the study is single-centre and documentation practices are institution-specific. External transportability should therefore be limited to the descriptive treatment-composition question rather than assumed for treatment recommendations.

## Conclusion

**Pending physician adjudication.** If the final physician-defined analysis preserves the pre-validation pattern, the study will support a restrained conclusion that established chronic/nonunion wrist-scaphoid presentations are characterized by greater documented bone-graft augmentation relative to acute/new fractures while internal fixation remains a common operative component. No conclusion will be made regarding treatment efficacy, optimal graft strategy, or a causal indication for grafting.

---

# Reporting and reproducibility notes for final submission

The final manuscript will be checked against STROBE and the RECORD extension for studies using routinely collected health data. A submission checklist with page/line locations will be completed after physician Gold and final journal formatting.

Final private outputs are generated through:

- `freeze_scaph_reference_v0_2.py` — final reference-standard freeze;
- `analyze_scaph_gold_v0_2.py` — prespecified exact clinical analysis;
- `build_scaph_final_tables_v0_1.py` — Table 1, Table 2, and duration supplementary table;
- `build_scaph_final_figures_v0_2.py` — final article-style figures.

---

# Working references

1. Ayalon O, Rettig SA, Tedesco LJ. Bone Graft and Fixation Options in the Surgical Management of Scaphoid Nonunion. *J Am Acad Orthop Surg*. 2024. PMID: 39531592. doi:10.5435/JAAOS-D-24-00510.
2. Miller EA, Huang JI. Traditional Bone Grafting in Scaphoid Nonunion. *Hand Clin*. 2024;40(1):105-116. PMID: 37979982. doi:10.1016/j.hcl.2023.08.001.
3. A systematic review of mechanical stabilization by screw fixation without bone grafting in stable scaphoid nonunion. 2021. PMID: 33816106.
4. Baamir A, et al. Graft choice for managing scaphoid non-union: umbrella review. *Hand Surg Rehabil*. 2024;43(4):101759. PMID: 39122186. doi:10.1016/j.hansur.2024.101759.
5. Bone grafting for scaphoid nonunion surgery: a systematic review and meta-analysis. 2022. PMID: 35491585.
6. Necessity of grafting in scaphoid nonunion fixation: A comparative outcome analysis. 2026. PMID: 41695733.
7. Higgins JP. When to Use Vascularized Bone? An Algorithm for Scaphoid Nonunion Surgery. *J Wrist Surg*. 2025. PMID: 41574159. doi:10.1055/a-2640-4238.
8. Strelzow JA, et al. Scaphoid Fractures and Nonunion: A Survey-based Review of Hand Surgeon's Practice and the Evidence. *J Hand Surg Glob Online*. 2024;6(6):836-841. PMID: 39703594. doi:10.1016/j.jhsg.2024.06.013.
9. Baamir A, et al. Graft choice for managing scaphoid non-union: umbrella review. *Hand Surg Rehabil*. 2024;43(4):101759. PMID: 39122186.

Reporting guidance:

10. von Elm E, et al. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) Statement: guidelines for reporting observational studies. 2007.
11. Benchimol EI, et al. The REporting of studies Conducted using Observational Routinely-collected health Data (RECORD) Statement. *PLoS Med*. 2015;12:e1001885. PMID: 26440803. doi:10.1371/journal.pmed.1001885.

**Reference note:** the scientific reference list remains working material. Every citation, title, year, pagination, DOI, and statement-to-source mapping must be reverified before submission.
