# Problem-First Scaphoid Manuscript Plan v0.1

## Working title

**Bone-Graft Augmentation in Established Chronic and Nonunion Scaphoid Disease: A Real-World Operative-Record Study**

Alternative, more conservative:

**Treatment Composition in Established Chronic/Nonunion Versus Other Wrist-Scaphoid Presentations: A Retrospective Real-World Study**

## Central question

Does established chronic/nonunion wrist-scaphoid disease correspond to a change in the **composition of surgery**, specifically increased bone-graft augmentation, while internal fixation remains common in both phenotype groups?

## One-sentence result target

> Among disease-concordant scaphoid operative records, internal fixation was similarly common across phenotype groups, whereas established chronic/nonunion presentations showed substantially greater use of bone-graft augmentation.

This sentence remains provisional until physician validation.

## Introduction structure

### Paragraph 1 — clinical problem

Scaphoid nonunion is difficult to treat because mechanical stability alone may be insufficient when biology, vascularity, bone loss or deformity are compromised.

### Paragraph 2 — current treatment uncertainty

Fixation is common, but the need for bone graft and more reconstructive strategies varies according to nonunion characteristics. Contemporary reviews and surgeon surveys show persistent heterogeneity in graft choice and operative strategy.

### Paragraph 3 — gap

Most published studies compare outcomes of specific nonunion techniques. Fewer describe how treatment composition differs across real-world scaphoid presentations before long-term outcome selection, particularly in routine clinical records.

### Paragraph 4 — objective

To compare the operative composition of established chronic/nonunion wrist-scaphoid presentations with other wrist-scaphoid presentations, focusing on bone-graft augmentation versus internal fixation.

## Methods structure

### 2.1 Study design and data source

Retrospective study of the fixed hospital exports. No additional local data are assumed.

### 2.2 Wrist-scaphoid cohort definition

Start from 88 broad scaphoid candidates; restrict to high-specificity wrist-scaphoid anatomy.

### 2.3 Exposure definition

Established chronic/nonunion state from diagnosis/complaint/examination text only. Operative text excluded.

### 2.4 Operative-record attribution

Detailed operative records must be attributable to the wrist-scaphoid disease; operations for another anatomical problem are excluded from the procedure denominator.

### 2.5 Procedure components

Primary: bone graft.  
Key contrast: internal fixation.  
Secondary: graft/reconstruction/fusion composite and component count.

### 2.6 Physician reference standard

Physician validation of anatomy, state, procedure relevance, fixation and graft labels.

### 2.7 Statistical analysis

Fisher exact tests for sparse binary outcomes; median/IQR for age and BMI; Mann-Whitney U for secondary component count. No high-capacity ML.

## Results structure

### 3.1 Cohort derivation

- 88 broad candidates;
- 68 high-specificity wrist-scaphoid;
- 23 established chronic/nonunion;
- 45 comparison phenotype;
- 28 disease-concordant detailed operative admissions.

### 3.2 Operative analysis period

All 28 disease-concordant detailed operative admissions occur in 2023-2025. This is the actual operative study period, not an independent sensitivity subgroup.

### 3.3 Baseline operative-subset characteristics

Report age, sex, BMI and missingness. Current deterministic extraction shows similar age/BMI distributions between groups.

### 3.4 Primary treatment-composition result

Report bone-graft augmentation by phenotype group with OR, 95% CI and Fisher exact P value after physician validation.

### 3.5 Key contrast

Report internal fixation by phenotype group. The intended scientific interpretation is whether the main difference is biologic augmentation rather than the base fixation construct.

### 3.6 Secondary treatment intensity

Report augmentation composite and major procedure-component count. Keep these secondary regardless of P value.

### 3.7 Robustness

- physician-adjudicated labels;
- uncertain-label exclusion;
- leave-one-out influence analysis;
- exclusion of competing same-admission procedures.

## Main figures

### Figure 1 — Study population and analytic denominator

A compact flow diagram only:

`88 broad scaphoid candidates`

→ `68 wrist scaphoid`

→ `23 established chronic/nonunion | 45 comparison`

→ `15 | 13 disease-concordant detailed operative records`

No framework boxes, public/private architecture or repository workflow in the main figure.

### Figure 2 — Treatment composition by scaphoid phenotype

Primary results figure.

Panel A: internal fixation proportion.  
Panel B: bone-graft augmentation proportion.  
Panel C: OR with 95% CI for the prespecified binary outcomes after physician validation.

Visual emphasis should be on the contrast:

`fixation: similar`  
`bone graft: different`

### Figure 3 — Physician validation of the variables used in the clinical analysis

Only metrics directly required for the scientific conclusion:

- wrist-scaphoid anatomy;
- chronic/nonunion state;
- target-disease procedure relevance;
- internal fixation;
- bone graft.

Do not show unrelated NLP benchmark tasks in the main paper.

### Figure 4 — Robustness / influence

Potential panels:

- deterministic vs physician-adjudicated effect estimate;
- leave-one-out OR range;
- primary bone-graft outcome vs broader augmentation composite.

Only include if it improves interpretation; otherwise move to Supplementary.

## Main tables

### Table 1 — Operative analytic cohort

Columns:

- chronic/nonunion;
- comparison.

Rows:

- n;
- age;
- sex;
- BMI;
- procedure-documentation completeness.

### Table 2 — Treatment composition

Rows:

- internal fixation;
- bone graft;
- reconstruction;
- fusion;
- augmentation composite;
- major component count.

Primary effect estimate is attached to bone graft.

## Supplementary material

The following are supplementary/methodological, not central scientific figures:

- full anatomy-disambiguation audit;
- broad-to-strict cohort rules;
- procedure-attribution audit;
- deterministic baseline freeze;
- complete NLP/LLM comparison, if performed;
- hallux-valgus and first-CMC exploratory analyses;
- repository reproducibility architecture.

## Computation boundary

The manuscript does not claim to develop a general-purpose framework.

Computational extraction is described only where necessary to measure the clinical variables used in the study.

If physician review shows that simple chart abstraction is sufficient and LLMs add no value, the LLM analysis can remain supplementary or be omitted entirely.
