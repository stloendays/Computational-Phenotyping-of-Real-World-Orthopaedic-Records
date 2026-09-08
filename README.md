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

### Stage 2 — generated from physician anatomy

Only after Stage 1 is frozen does `make_scaph_physician_packet_v0_1.py downstream` generate:

- clinical-state review for every **physician-confirmed wrist-scaphoid** record;
- procedure relevance/components for physician-confirmed wrist records that have detailed operative documentation.

Therefore the final state/procedure sample sizes are **not assumed in advance** to equal the deterministic 68 and 31. This design avoids verification bias from allowing the rule system to predefine the clinical study population.

A local Stage-1 packet has already been generated with **88 anatomy rows** and **18 prespecified double-review rows**; all Gold fields are blank. Patient-level review files and the pseudonym salt remain private.

## Comparison-group caution

The comparison group is not automatically described as acute.

A conservative pre-gold audit of the current 13 deterministic comparison operative records finds explicit acute/new or recent-injury wording in only **7/13**. The remaining records contain postoperative-history wording, longer-duration wording, or insufficient explicit state evidence.

Therefore:

- the main analysis retains a neutral comparison group based on physician state;
- a prespecified sensitivity analysis compares chronic/nonunion records with **physician-confirmed acute/new fractures only**.

See `data/aggregate/scaphoid_comparison_state_audit_v0_1.csv`.

## Outcomes

### Primary outcome

**Bone-graft augmentation**.

### Key contrast

**Internal fixation**.

### Secondary outcomes

- graft/reconstruction/fusion augmentation composite;
- number of major operative components;
- individual reconstruction/fusion components when sample size permits.

The primary outcome was frozen before physician-reference scoring and is not replaced by a composite simply because another analysis yields a smaller P value.

## Main manuscript files

- `docs/SCAPHOID_SCIENTIFIC_QUESTION_V0_1.md` — scientific question and claim boundaries;
- `docs/SCAPHOID_ANALYSIS_PLAN_V0_1.md` — two-stage focused statistical analysis plan;
- `docs/DATA_DRIVEN_QUESTION_SELECTION_V0_1.md` — why this question was selected over other signals in the fixed dataset;
- `docs/SCAPHOID_PHYSICIAN_REVIEW_GUIDE_ZH.md` — two-stage Chinese physician review instructions;
- `docs/MANUSCRIPT_PLAN_SCAPHOID_V0_1.md` — article structure and figure plan;
- `manuscript/SCAPHOID_MANUSCRIPT_DRAFT_V0_2.md` — current English manuscript draft;
- `figures/scaphoid/Figure1_cohort_flow_pre_gold.svg` — current article-style pre-validation cohort-flow figure.

## Analysis and validation code

- `src/ortho_pheno/scaphoid_augmentation_analysis_v0_1.py` — focused deterministic pre-validation analysis;
- `src/ortho_pheno/scaphoid_comparison_state_audit_v0_1.py` — comparison-state evidence audit;
- `src/ortho_pheno/make_scaph_physician_packet_v0_1.py` — local-only two-stage physician packet generator;
- `src/ortho_pheno/rules.py` — deterministic anatomy/state measurement rules;
- `src/ortho_pheno/procedure_rules.py` — procedure-relevance and component rules.

Public-safe aggregate outputs:

- `data/aggregate/scaphoid_augmentation_signal_v0_1.csv`;
- `data/aggregate/scaphoid_comparison_state_audit_v0_1.csv`.

## Interpretation boundary

This study can test an association between established chronic/nonunion presentation and **documented operative composition**.

It cannot establish:

- risk of future nonunion;
- postoperative union or healing time;
- treatment efficacy;
- causal treatment selection;
- superiority of one graft or fixation strategy.

## Secondary data domains

The fixed archive also contains hallux-valgus and first-CMC OA records. Those analyses are retained as secondary/supplementary work and do not define the current main manuscript.

## Privacy

The source archive contains direct identifiers and protected clinical text. **No raw patient data, pseudonymized row-level data, admission identifiers, patient-level dates, clinical free text, or pseudonym salts are committed to this public repository.**

Public artifacts use small-cell suppression (`<5`) when necessary to prevent reverse engineering of patient-level counts.
