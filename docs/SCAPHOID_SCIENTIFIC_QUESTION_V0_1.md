# Scaphoid Scientific Question v0.1

**Status:** data-driven question freeze before physician-reference scoring  
**Dataset boundary:** fixed local archive; no additional hospital data assumed  
**Phenotype dependency:** scaphoid anatomy v0.3  
**Interpretation class:** exploratory / hypothesis-generating clinical association

## 1. Scientific problem

The current dataset does not support longitudinal prediction of incident scaphoid nonunion or long-term postoperative healing. It does, however, contain a clinically coherent cross-sectional contrast between patients documented with an **established chronic/nonunion wrist-scaphoid phenotype** and other wrist-scaphoid presentations, together with detailed operative records for a subset.

The data-driven observation motivating this study is that internal fixation appears common in both groups, whereas bone-graft augmentation is concentrated in the established chronic/nonunion group.

The primary scientific question is therefore:

> **Among wrist-scaphoid admissions with disease-concordant detailed operative documentation, is established chronic/nonunion disease associated with a shift from fixation-dominant surgery toward bone-graft augmentation?**

This is a treatment-composition question. It is not a prediction-of-future-nonunion study and it is not an evaluation of postoperative union.

## 2. Clinical rationale

Modern scaphoid-nonunion treatment commonly combines stable fixation with biologic augmentation when healing biology, vascularity, bone loss or deformity are concerning. Contemporary reviews emphasize that graft choice and reconstruction depend on factors such as proximal-pole viability, avascular necrosis, substance defect and deformity, while surgeon practice remains heterogeneous.

The local data allow a narrower real-world question: whether the transition from other wrist-scaphoid presentations to established chronic/nonunion is reflected mainly in **additional biologic/reconstructive components**, rather than a large change in the use of fixation itself.

This distinction is clinically meaningful because it separates the base mechanical construct from added biologic/reconstructive treatment intensity.

## 3. Exposure definition

### Established chronic/nonunion phenotype

Assigned only from non-operative clinical text:

- diagnosis;
- complaint;
- physical examination.

Qualifying concepts include documented chronic/old fracture, nonunion, non-healing or equivalent established states.

Operative names and operative-note contents are prohibited from assigning the exposure because operative treatment is the downstream variable of interest.

### Comparison phenotype

Other high-specificity wrist-scaphoid admissions that do not meet the established chronic/nonunion rule.

The comparison group is not described uniformly as acute because the fixed records do not establish acute status for every episode.

## 4. Analysis population

### Cohort level

Phenotype v0.3 identifies:

- 68 high-specificity wrist-scaphoid admissions;
- 23 established chronic/nonunion phenotypes;
- 45 comparison phenotypes.

### Operative analysis level

Detailed operative-note module availability is not sufficient for treatment attribution. Only notes whose operative body is attributable to the wrist-scaphoid disease contribute to the treatment-composition analysis.

Current deterministic audit:

- established chronic/nonunion: 15 disease-concordant detailed operative admissions;
- comparison phenotype: 13 disease-concordant detailed operative admissions;
- total analytic operative sample: 28.

**All 28 disease-concordant detailed operative admissions occur in 2023-2025.** Therefore 2023-2025 is the primary operative-analysis era, not an independent sensitivity subset. Historical years may contribute to cohort/state description but cannot provide an independent detailed-procedure replication under the supplied exports.

## 5. Primary and secondary outcomes

### Primary clinical outcome

**Bone-graft augmentation**, defined as a target-disease operative record containing a validated bone-graft component.

Rationale: this is a clinically specific biologic augmentation step and avoids constructing a composite solely because it improves statistical significance.

### Key contrast outcome

**Internal fixation**.

This is included to test the specific pattern suggested by the data: fixation remains common in both groups while graft augmentation changes.

### Secondary outcomes

- any graft/reconstruction/fusion augmentation composite;
- procedure-component count across fixation, graft, reconstruction and fusion;
- fusion/salvage component;
- other prespecified procedure components, interpreted descriptively when sparse.

## 6. Statistical analysis

Because the operative sample is small, inference is intentionally simple.

### Descriptive comparison

Report:

- n and percentage for categorical variables;
- median and IQR for age and BMI;
- missingness denominators explicitly.

### Primary unadjusted analysis

- Fisher exact test for bone-graft augmentation;
- odds ratio with 95% confidence interval in the internal/manuscript analysis;
- public GitHub outputs suppress inferential statistics when a 1-4 cell could be reverse-engineered.

### Key contrast analysis

Repeat the same comparison for internal fixation.

### Secondary treatment-intensity analysis

Procedure-component count may be compared with a Mann-Whitney U test and reported descriptively. This is secondary and cannot replace the prespecified bone-graft outcome merely because it yields a smaller P value.

### Covariate adjustment

The 28-record operative sample does not justify a high-dimensional model. Age, sex and BMI are reported as baseline descriptors. Multivariable adjustment is omitted unless physician adjudication materially increases the evaluable sample or a prespecified sparse-data model is justified.

No stepwise selection, random forest, XGBoost or neural-network model is used for this clinical question.

## 7. Current deterministic observation

Before physician adjudication, deterministic extraction shows:

- internal fixation is present in nearly all disease-concordant operative records in both phenotype groups;
- bone grafting is substantially more frequent in established chronic/nonunion records;
- the same pattern is reflected in a higher procedure-component burden in the chronic/nonunion group.

These are **algorithm-derived exploratory observations**, not final clinical estimates. Final manuscript values require physician validation of anatomy, disease state, procedure relevance and procedure components.

## 8. Validation requirement

The association analysis is blocked from final clinical interpretation until the physician reference standard confirms:

1. wrist-scaphoid anatomy;
2. established chronic/nonunion state;
3. target-disease procedure relevance;
4. bone-graft and fixation labels.

The deterministic baseline was cryptographically frozen before gold annotation, so physician review cannot be used to retroactively tune the baseline system.

## 9. Interpretation boundaries

Allowed interpretation after successful validation:

> Established chronic/nonunion wrist-scaphoid presentations were associated with greater use of bone-graft augmentation among surgically treated records, while internal fixation remained common in both groups.

Prohibited interpretations:

- chronic/nonunion caused the surgeon to graft;
- the identified treatment strategy improved union;
- the model predicts which acute fracture will become a nonunion;
- grafting is recommended for an individual patient;
- the data establish superiority of one graft or fixation technique.

## 10. Literature context

Relevant contemporary sources include:

- Ayalon O, Rettig SA, Tedesco LJ. *Bone Graft and Fixation Options in the Surgical Management of Scaphoid Nonunion*. J Am Acad Orthop Surg. 2024. PMID: 39531592. doi:10.5435/JAAOS-D-24-00510.
- Miller EA, Huang JI. *Traditional Bone Grafting in Scaphoid Nonunion*. Hand Clin. 2024;40(1):105-116. PMID: 37979982. doi:10.1016/j.hcl.2023.08.001.
- Scaphoid Fractures and Nonunion: A Survey-based Review of Hand Surgeon's Practice and the Evidence. 2024. PMID: 39703594.

These sources support the clinical plausibility of graft augmentation and the heterogeneity of nonunion treatment. They do not by themselves establish the local association.

## 11. Paper-level role of computation

Computational phenotyping is a **measurement method** for recovering the exposure and operative components from existing free text. It is not the scientific objective of the paper.

The scientific sequence is:

`observed treatment-composition signal -> clinical question -> physician-validated measurement -> association analysis -> cautious interpretation`
