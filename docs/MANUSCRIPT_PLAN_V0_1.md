# Manuscript Plan v0.1

**Status:** preregistered narrative scaffold before physician-gold results  
**Dataset:** fixed 18-file local archive  
**Current phenotype:** v0.3  
**Current procedure context:** audit v0.1

## 1. Proposed manuscript positioning

### Preferred title direction

**From Noisy Orthopaedic EHR Exports to Auditable Clinical Phenotypes: A Validation-First Study Across Deformity, Trauma and Degenerative Hand Disease**

Alternative:

**Computational Phenotyping of Real-World Orthopaedic Records: Anatomy-Aware Cohort Reconstruction and Procedure Attribution in Chinese EHR Data**

The manuscript should be positioned primarily as a **clinical informatics / computational phenotyping** study, not as a small-sample prediction paper.

## 2. Central scientific argument

Real-world orthopaedic EHR exports contain several distinct sources of label error that are invisible in a conventional spreadsheet analysis:

1. repeated diagnosis rows create pseudoreplication if raw rows are treated as independent patients;
2. anatomically ambiguous Chinese terminology can mix clinically distinct structures, as in wrist scaphoid versus foot navicular retrieval;
3. character-level lexical shortcuts can create false anatomy evidence;
4. an operative-note module can contain a procedure for an anatomical problem unrelated to the study disease;
5. missing documentation modules and negative clinical findings are not equivalent;
6. calendar-era changes in source-system coverage can masquerade as clinical differences.

The project therefore develops an auditable, versioned phenotyping architecture in which:

`raw EHR exports -> admission reconstruction -> anatomy/state phenotypes -> procedure attribution -> procedure components -> physician reference standard -> locked algorithm comparison`

The three orthopaedic domains provide complementary stress tests:

- hallux valgus: dense multi-label procedure phenotyping and baseline disease descriptors;
- scaphoid retrieval: difficult anatomical disambiguation plus established chronic/nonunion state;
- first-CMC OA: high-specificity thumb-base disease identification against hard wrist-disease negatives.

## 3. Manuscript claims frozen before model scoring

### Claims that can be made from source/audit evidence

- raw diagnosis rows are not valid independent analytical units;
- the fixed export has a substantial 2019-2022 documentation-era discontinuity;
- the deterministic v0.3 pipeline explicitly separates wrist scaphoid, foot navicular and ambiguous scaphoid candidates;
- the v0.3 revision removed explicit anatomical contamination rather than increasing the wrist cohort;
- operative-note module availability is distinct from target-disease procedure attribution;
- privacy-preserving aggregate reproducibility is possible without publishing patient-level clinical text.

### Claims blocked until physician validation

- clinical accuracy of disease/anatomy rules;
- accuracy of chronic/nonunion state assignment;
- accuracy of procedure relevance and procedure-component extraction;
- validated prevalence of the current deterministic procedure phenotypes;
- robustness of the hallux bilateral/Chevron association to physician-adjudicated labels;
- robustness of the scaphoid treatment-complexity signal to physician-adjudicated labels;
- superiority of deterministic, dictionary, LLM-assisted or hybrid methods.

### Claims prohibited under the fixed-data design

- prediction of future incident scaphoid nonunion;
- long-term postoperative efficacy, recurrence or functional-outcome prediction;
- causal recommendation of a surgical strategy;
- clinical external validation using a public NLP benchmark.

## 4. Proposed main-text structure

## Introduction

### Paragraph 1 - real-world orthopaedic EHR problem

Introduce the increasing use of routine EHR data in orthopaedic research and the gap between administrative export structure and clinically valid phenotypes.

### Paragraph 2 - why orthopaedics is unusually vulnerable

Emphasize anatomy-specific terminology, multi-site trauma, synonymous Chinese diagnosis strings, free-text operative records and multi-component procedures.

### Paragraph 3 - limitation of conventional keyword/AI approaches

Explain that high apparent extraction accuracy can conceal pseudoreplication, anatomical leakage, source-scope leakage and procedure-attribution errors.

### Paragraph 4 - study objective

State the objective as developing and validating an auditable computational-phenotyping framework across three distinct orthopaedic domains, with physician adjudication and preregistered deterministic baselines.

## Methods

### 2.1 Study design and fixed-data boundary

Retrospective clinical-informatics study using the 18 supplied hospital exports. No future local data are assumed.

### 2.2 Source modules and privacy architecture

Describe the 12 modern XLSX + 6 legacy XLS exports, local-only raw data, public aggregate release and small-cell suppression.

### 2.3 Admission-level reconstruction

Define admission episode as the analytical unit and quantify why row-level analysis would be pseudoreplicated.

### 2.4 Phenotype v0.3 disease/anatomy rules

Describe hallux, scaphoid three-state anatomy and strict first-CMC definitions. Include rule-version auditing.

### 2.5 Scaphoid clinical-state source restriction

State that chronic/nonunion state is assigned from diagnosis/complaint/examination only; operative text is prohibited.

### 2.6 Procedure attribution and multi-label taxonomy

Separate module availability, target-disease relevance and procedure-component extraction.

### 2.7 Physician reference standard

Describe 367 disease/anatomy reviews, 68 scaphoid-state reviews, 163 procedure reviews and ~20% independent repeat review.

### 2.8 Baseline preregistration and cryptographic freeze

Report that deterministic predictions were generated while every gold field was blank and frozen by SHA-256 before physician annotation.

### 2.9 Evaluation metrics

Disease/anatomy metrics; hallux baseline phenotypes; scaphoid state; procedure relevance; conditional procedure components; end-to-end procedure components; inter-rater reliability.

### 2.10 Clinical exploratory analyses

Hallux procedure-pattern heterogeneity and bilateral/Chevron contrast; scaphoid treatment-pattern comparison; calendar-era sensitivity.

### 2.11 External public benchmark

If used, describe CBLUE only as an auxiliary Chinese biomedical NLP competence benchmark, separate from local clinical validity.

## Results

### 3.1 Reconstruction changes the analytical denominator

Report source duplication/inflation and strict cohort counts.

### 3.2 Anatomy-aware phenotyping exposes cohort contamination

Report scaphoid 68/13/7 anatomy partition and v0.2 -> v0.3 transition; first-CMC broad versus strict retrieval.

### 3.3 Procedure attribution exposes a second hidden EHR error mode

Report module-available versus disease-concordant operative records (114->113, 31->28, 18->18) and give non-identifying error categories.

### 3.4 Physician reference-standard performance

**Blocked until Issue #3 is complete.**

Report inter-rater agreement first, then deterministic disease/anatomy/state/relevance/component metrics. Compare later semantic systems only on the identical frozen gold labels.

### 3.5 Hallux-valgus treatment phenotype

After validation, report validated procedure prevalence, common multi-label combinations and the bilateral/Chevron exploratory association with uncertainty.

### 3.6 Scaphoid established-phenotype treatment pattern

After validation, compare established chronic/nonunion versus other wrist-scaphoid treatment patterns. Maintain explicit language that this is not incident-nonunion prediction.

### 3.7 Cross-domain error taxonomy

Summarize anatomy confusion, procedure-attribution errors, missingness errors, source-scope violations and semantic extraction errors across domains.

## Discussion

### 4.1 Main contribution

The main contribution is not a single classifier. It is a reproducible evidence architecture for converting heterogeneous orthopaedic EHR exports into auditable clinical phenotypes.

### 4.2 Why anatomy-aware uncertainty matters

Discuss why explicit `ambiguous/uncertain` states are preferable to forced binary assignment.

### 4.3 Procedure attribution as a distinct clinical NLP problem

Highlight the difference between recognizing a procedure phrase and correctly assigning that procedure to the target disease in multi-problem admissions.

### 4.4 Clinical signals

Interpret hallux and scaphoid treatment-pattern findings conservatively as real-world associations, conditional on successful physician validation.

### 4.5 Generalizability

Separate architectural portability from validated clinical generalization. Three local disease domains demonstrate cross-domain implementation; external public NLP benchmarks provide language-task context rather than clinical external validation.

### 4.6 Limitations

Fixed single-center retrospective data, incomplete historical modules, no consistent long-term outcome data, modest disease-specific sample sizes, free-text documentation variability and physician-reference-standard subjectivity.

### 4.7 Conclusion

Conclude around validated and auditable phenotype reconstruction, not treatment recommendation or long-term prediction.

## 5. Proposed main figures

### Figure 1 - Validation-first computational phenotyping framework

Show:

`18 raw exports -> admission reconstruction -> disease/anatomy -> state -> procedure relevance -> procedure components -> physician gold -> frozen baseline/LLM comparison`

Include the public/private data boundary.

**Can be prepared now.**

### Figure 2 - Cohort reconstruction and anatomy disambiguation

Panel A: raw-row inflation by domain.  
Panel B: broad candidate -> strict phenotype.  
Panel C: scaphoid 88 -> 68 wrist / 13 foot / 7 ambiguous.  
Panel D: prior heuristic 72 -> v0.3 transition showing four foot-navicular removals and zero additions.

**Can be prepared now.**

### Figure 3 - Procedure attribution failure mode

Panel A: schematic of a multi-problem admission where a generic procedure term belongs to another anatomy.  
Panel B: module-available versus disease-concordant operative admissions across domains.  
Panel C: hierarchical relevance -> procedure-component evaluation.

**Can be prepared now.**

### Figure 4 - Physician validation benchmark

Panel A: disease/anatomy macro-F1 by domain/system.  
Panel B: scaphoid state sensitivity/specificity.  
Panel C: procedure-relevance F1/specificity.  
Panel D: conditional versus end-to-end component micro-F1.

**Blocked until physician gold is frozen.**

### Figure 5 - Hallux-valgus procedure phenotype

Panel A: validated procedure-component prevalence.  
Panel B: common procedure combinations / co-occurrence.  
Panel C: bilateral-disease phenotype by Chevron status with effect estimate.

**Provisional data exist; final figure blocked until validation.**

### Figure 6 - Scaphoid phenotype and treatment complexity

Panel A: 23 established chronic/nonunion vs 45 comparison group.  
Panel B: disease-concordant treatment components.  
Panel C: 2023-2025 sensitivity analysis.

**Provisional data exist; final figure blocked until validation.**

## 6. Proposed main tables

### Table 1 - Source architecture and cohort reconstruction

Current aggregate data sufficient.

### Table 2 - Physician reference-standard and system performance

Blocked until gold freeze.

### Table 3 - Hallux-valgus validated clinical/procedure phenotype

Final values blocked until gold validation.

### Table 4 - Scaphoid established-phenotype comparison

Final procedure labels blocked until gold validation.

## 7. Supplementary material

Suggested supplements:

- full source-file inventory;
- phenotype definitions v0.3;
- rule-version transition table;
- procedure-context audit;
- complete error taxonomy;
- inter-rater reliability details;
- rare procedure-label metrics;
- public CBLUE task-native benchmark if performed;
- claim-to-evidence matrix;
- reproducibility manifest and software versions.

## 8. Narrative freeze rule

The main scientific narrative should not be changed merely because a later model performs better or worse than expected.

A new result can alter the manuscript claim hierarchy only if it:

1. is generated from a versioned method;
2. uses the frozen physician reference standard where a clinical label is involved;
3. passes the prespecified leakage and source-scope rules;
4. is added to the claim-to-evidence matrix with an explicit evidence class.

This preserves a validation-first study rather than a result-first AI story.
