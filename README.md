# Real-World Scaphoid Treatment Composition Study

This repository supports a **problem-first retrospective study** of wrist-scaphoid presentations in a fixed hospital EHR dataset.

## Primary scientific question

> **Among physician-confirmed wrist-scaphoid admissions with disease-concordant detailed operative documentation, is established chronic/nonunion disease associated with greater use of bone-graft augmentation while internal fixation remains common across phenotype groups?**

Computational text processing is used only to recover and validate the clinical variables required to answer this question. It is **not** the scientific objective of the paper.

## Data-derived signal motivating the study

The current deterministic pre-validation analysis shows a specific treatment-composition pattern:

| Operative component | Established chronic/nonunion | Comparison phenotype |
|---|---:|---:|
| Internal fixation | 14/15 (93.3%) | 12/13 (92.3%) |
| Bone graft | 8/15 (53.3%) | `<5/13` |
| Graft/reconstruction/fusion augmentation | 9/15 (60.0%) | `<5/13` |

The hypothesis is therefore narrower than “chronic cases receive more complex surgery.” The proposed signal is that **the base fixation construct remains common while biological/reconstructive augmentation increases**.

These values are algorithm-derived and provisional until physician adjudication.

## Secondary mechanistic hypothesis

A separate pre-validation audit performed after the primary question was selected identified a possible duration gradient **within established chronic/nonunion operative records**:

- deterministic graft-positive records with explicit duration: 7/8, median **182.6 days**;
- deterministic graft-negative records with explicit duration: 6/7, median **15.0 days**.

This does **not** replace the primary endpoint. It is frozen as an exploratory secondary hypothesis:

> Within physician-confirmed established chronic/nonunion wrist-scaphoid operative records, is graft augmentation associated with a longer explicitly documented wrist-related injury or symptom duration?

The final duration variable is physician adjudicated. Automated duration-parser outputs are hidden from reviewers. No locally optimized duration cutoff will be used.

See `docs/SCAPHOID_DURATION_SECONDARY_HYPOTHESIS_V0_1.md` and `data/aggregate/scaphoid_duration_signal_v0_1.csv`.

## Pre-validation cohort audit

The supplied broad scaphoid retrieval contains 88 candidate admission episodes. Phenotype v0.3 currently partitions them into:

- **68** deterministic wrist-scaphoid admissions;
- **13** explicit foot-navicular admissions;
- **7** anatomically ambiguous admissions.

Within the 68 deterministic wrist-scaphoid records:

- **23** have an established chronic/nonunion phenotype;
- **45** form the comparison phenotype.

The current deterministic operative audit identifies 31 detailed-note module records and 28 disease-concordant detailed operative records (15 chronic/nonunion; 13 comparison). All 28 occur in **2023-2025**.

These counts are audit outputs, not the final physician-defined cohort.

## Two-stage physician reference standard

The final cohort is deliberately **not restricted to deterministic wrist-scaphoid positives**.

### Stage 1 — anatomy

All **88 broad scaphoid candidates** are independently reviewed for:

- wrist scaphoid;
- foot navicular;
- other;
- uncertain.

The Stage-1 anatomy Gold is adjudicated and frozen first.

The 88-row Stage-1 input and 18-row prespecified double-review selection were cryptographically frozen while every anatomy Gold field was blank.

### Stage 2 — generated from physician anatomy

Only after Stage 1 is frozen does `make_scaph_physician_packet_v0_1.py downstream` generate:

- clinical-state review for every **physician-confirmed wrist-scaphoid** record;
- physician-adjudicated relevant duration value/unit/basis;
- procedure relevance/components for physician-confirmed wrist records with detailed operative documentation;
- independent Reviewer-2 subset packets containing no Reviewer-1 labels.

Therefore the final state/procedure sample sizes are **not assumed in advance** to equal the deterministic 68 and 31. This design avoids verification bias from allowing the rule system to predefine the clinical study population.

## Comparison-group caution

The comparison group is not automatically described as acute.

A conservative pre-gold audit of the current 13 deterministic comparison operative records finds explicit acute/new or recent-injury wording in only **7/13**. The remaining records contain postoperative-history wording, longer-duration wording, or insufficient explicit state evidence.

Therefore:

- the main analysis retains a neutral comparison group based on physician state;
- a prespecified sensitivity analysis compares chronic/nonunion records with **physician-confirmed acute/new fractures only**.

See `data/aggregate/scaphoid_comparison_state_audit_v0_1.csv`.

## Outcomes and hierarchy

### Primary outcome

**Bone-graft augmentation**.

### Key contrast

**Internal fixation**.

### Secondary outcomes

- graft/reconstruction/fusion augmentation composite;
- number of major operative components;
- individual reconstruction/fusion components when sample size permits;
- physician-adjudicated relevant duration within established chronic/nonunion records.

The primary outcome is not replaced by a composite or the duration analysis simply because another analysis yields a smaller P value.

## Main manuscript files

- `docs/SCAPHOID_SCIENTIFIC_QUESTION_V0_1.md` — primary scientific question and claim boundaries;
- `docs/SCAPHOID_ANALYSIS_PLAN_V0_3.md` — current two-stage statistical analysis plan including the duration secondary hypothesis;
- `docs/SCAPHOID_DURATION_SECONDARY_HYPOTHESIS_V0_1.md` — frozen duration hypothesis and analysis boundary;
- `docs/DATA_DRIVEN_QUESTION_SELECTION_V0_1.md` — why this question was selected over other signals in the fixed dataset;
- `docs/SCAPHOID_PHYSICIAN_REVIEW_GUIDE_ZH.md` — current Chinese physician review instructions;
- `docs/MANUSCRIPT_PLAN_SCAPHOID_V0_1.md` — article structure and figure plan;
- `manuscript/SCAPHOID_MANUSCRIPT_DRAFT_V0_3.md` — current English manuscript draft;
- `figures/scaphoid/Figure1_cohort_flow_pre_gold.svg` — current article-style pre-validation cohort-flow figure.

## Analysis and validation code

- `src/ortho_pheno/scaphoid_augmentation_analysis_v0_1.py` — focused deterministic pre-validation analysis;
- `src/ortho_pheno/scaphoid_comparison_state_audit_v0_1.py` — comparison-state evidence audit;
- `src/ortho_pheno/scaphoid_duration_audit_v0_1.py` — secondary duration audit;
- `src/ortho_pheno/duration_rules.py` — dependency-free Chinese duration parser with regression tests;
- `src/ortho_pheno/make_scaph_physician_packet_v0_1.py` — local-only two-stage primary/Reviewer-2 packet generator;
- `src/ortho_pheno/freeze_scaph_reference_v0_1.py` — controlled-vocabulary validation and final SHA-256 reference-standard freeze;
- `src/ortho_pheno/rules.py` — deterministic anatomy/state measurement rules;
- `src/ortho_pheno/procedure_rules.py` — procedure-relevance and component rules.

Public-safe aggregate outputs:

- `data/aggregate/scaphoid_augmentation_signal_v0_1.csv`;
- `data/aggregate/scaphoid_comparison_state_audit_v0_1.csv`;
- `data/aggregate/scaphoid_duration_signal_v0_1.csv`.

## Interpretation boundary

This study can test associations between established chronic/nonunion presentation, documented wrist-related duration, and **documented operative composition**.

It cannot establish:

- risk of future nonunion;
- postoperative union or healing time;
- treatment efficacy;
- causal treatment selection;
- superiority of one graft or fixation strategy;
- a clinical duration threshold at which grafting should be performed.

## Secondary data domains

The fixed archive also contains hallux-valgus and first-CMC OA records. Those analyses are retained as secondary/supplementary work and do not define the current main manuscript.

## Privacy

The source archive contains direct identifiers and protected clinical text. **No raw patient data, pseudonymized row-level data, admission identifiers, patient-level dates, clinical free text, Reviewer-1/Reviewer-2 packets, or pseudonym salts are committed to this public repository.**

Public artifacts use small-cell suppression (`<5`) when necessary to prevent reverse engineering of patient-level counts.
