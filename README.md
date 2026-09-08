# Real-World Scaphoid Treatment Composition Study

This repository supports a **problem-first retrospective study** of wrist-scaphoid presentations in a fixed hospital EHR dataset.

## Primary scientific question

> **Among physician-confirmed wrist-scaphoid admissions with disease-concordant detailed operative documentation, is established chronic/nonunion associated with greater bone-graft augmentation than physician-confirmed acute/new fracture while internal fixation remains common in both groups?**

Computational text processing is used only to recover and validate the clinical variables needed to answer this question. It is not the scientific objective of the paper.

## Data-derived signal motivating the study

The deterministic pre-validation audit showed a treatment-composition pattern in which internal fixation was frequent across operative wrist-scaphoid records, whereas bone grafting was concentrated in records with established chronic/nonunion terminology.

Current pre-validation values include:

| Operative component | Established chronic/nonunion | Deterministic non-chronic comparison* |
|---|---:|---:|
| Internal fixation | 14/15 (93.3%) | 12/13 (92.3%) |
| Bone graft | 8/15 (53.3%) | `<5/13` |
| Graft/reconstruction/fusion augmentation | 9/15 (60.0%) | `<5/13` |

\*The 13 deterministic comparison records are **not** assumed to be acute. Final clinical inference uses only physician-confirmed `acute_or_new_fracture` records.

The hypothesis is narrower than “chronic cases receive more complex surgery.” The proposed signal is that a mechanical fixation base remains common while biological/reconstructive augmentation changes with presentation state.

These values are provisional until physician adjudication.

## Secondary mechanistic hypothesis

A separate pre-validation audit performed after the primary question was selected identified a possible duration gradient within established chronic/nonunion operative records:

- graft-positive records with explicit duration: 7/8, median **182.6 days**;
- graft-negative records with explicit duration: 6/7, median **15.0 days**.

This does not replace the primary endpoint. It is frozen as an exploratory secondary hypothesis:

> Within physician-confirmed established chronic/nonunion wrist-scaphoid operative records, is graft augmentation associated with longer explicitly documented wrist-related injury or symptom duration?

The final duration variable is physician adjudicated. Automated duration-parser output is hidden from reviewers. No locally optimized duration cutoff is used.

## Pre-validation cohort audit

The supplied broad scaphoid retrieval contains **88** candidate admission episodes. Phenotype v0.3 partitions them into:

- **68** deterministic wrist-scaphoid admissions;
- **13** explicit foot-navicular admissions;
- **7** anatomically ambiguous admissions.

Within the deterministic wrist group, **23** have established chronic/nonunion terminology.

The deterministic operative audit identifies 31 detailed-note module records and 28 disease-concordant detailed operative records. All 28 occur in **2023-2025**.

These are engineering audit counts, not the final physician-defined cohort.

## Two-stage physician reference standard

The final cohort is deliberately not restricted to deterministic wrist-scaphoid positives.

### Stage 1 — anatomy

All 88 broad candidates undergo blinded physician review for:

- wrist scaphoid;
- foot navicular;
- other;
- uncertain.

The 88-row Stage-1 packet and 18-row prespecified Reviewer-2 subset were cryptographically frozen before annotation while all Gold fields were blank.

Reviewer-1 and Reviewer-2 labels are preserved separately. Discordant records require explicit adjudication. Stage-1 anatomy Gold is frozen before downstream review is generated.

### Stage 2 — state, duration, and procedure

Only physician-confirmed wrist-scaphoid records enter downstream review.

State categories are:

- `acute_or_new_fracture`;
- `established_chronic_fracture`;
- `established_nonunion`;
- `chronic_nonunion_not_distinguishable`;
- `insufficient_or_uncertain`.

The primary clinical comparison is fixed as:

- **established chronic/nonunion** = the three established categories above;
- **acute/new** = physician-confirmed `acute_or_new_fracture` only.

`insufficient_or_uncertain` is excluded from state-based inference.

There is no separate acute-only sensitivity analysis because acute/new is already the primary comparison group. This correction was made before physician Gold completion and does not change the primary outcome.

For physician-confirmed wrist records with detailed operative documentation, reviewers first determine whether the note actually documents a wrist-scaphoid procedure before labeling fixation, graft, reconstruction, and fusion.

## Outcomes and hierarchy

### Primary outcome

**Bone-graft augmentation**.

### Key contrast

**Internal fixation**.

### Secondary outcomes

- graft/reconstruction/fusion augmentation composite;
- major procedure-component count;
- individual reconstruction/fusion components when informative;
- physician-adjudicated relevant duration within established chronic/nonunion records.

The primary outcome cannot be replaced because another analysis yields a smaller P value.

## Final post-Gold analysis

After the physician reference standard is adjudicated and SHA-256 frozen, the current manuscript analysis entrypoint is:

`src/ortho_pheno/analyze_scaph_gold_v0_2.py`

It executes the prespecified analysis only:

1. physician-defined chronic/nonunion vs acute/new operative groups;
2. primary bone-graft 2×2 table;
3. two-sided Fisher exact test;
4. conditional odds ratio and 95% CI;
5. internal-fixation key contrast;
6. augmentation composite and component-count secondary analyses;
7. leave-one-out influence analysis;
8. physician-adjudicated duration analysis within chronic/nonunion;
9. private exact manuscript JSON + privacy-suppressed public CSV.

Uncertain procedure-component labels are excluded from the corresponding denominator rather than silently coded as negative.

Final article-style figures are generated from the frozen Gold plus the private exact analysis by:

`src/ortho_pheno/build_scaph_final_figures_v0_2.py`

## Current manuscript chain

- `docs/SCAPHOID_SCIENTIFIC_QUESTION_V0_1.md` — scientific question and claim boundaries;
- `docs/SCAPHOID_ANALYSIS_PLAN_V0_3.md` — current statistical plan;
- `docs/SCAPHOID_ANALYSIS_CHANGELOG_V0_1.md` — transparent pre-Gold analysis changes;
- `docs/SCAPHOID_DURATION_SECONDARY_HYPOTHESIS_V0_1.md` — frozen secondary duration hypothesis;
- `docs/SCAPHOID_PHYSICIAN_REVIEW_GUIDE_ZH.md` — current physician review guide;
- `docs/SCAPHOID_NOVELTY_AUDIT_V0_1.md` — novelty/claim boundary audit;
- `manuscript/SCAPHOID_MANUSCRIPT_DRAFT_V0_4.md` — current English manuscript draft;
- `figures/scaphoid/Figure1_cohort_flow_pre_gold.svg` — pre-validation article-style cohort flow.

## Validation and analysis code

- `src/ortho_pheno/make_scaph_physician_packet_v0_1.py` — two-stage Reviewer-1/Reviewer-2 packet generator;
- `src/ortho_pheno/make_scaph_adjudication_templates_v0_1.py` — preserves independent labels and creates separate adjudicated Gold templates;
- `src/ortho_pheno/freeze_scaph_reference_v0_2.py` — current Stage-1/final SHA-256 freeze entrypoint with analysis-plan v0.3 metadata;
- `src/ortho_pheno/freeze_scaph_reference_v0_1.py` — tested underlying vocabulary/ID/hash validator;
- `src/ortho_pheno/analyze_scaph_gold_v0_2.py` — current post-Gold manuscript analysis entrypoint;
- `src/ortho_pheno/build_scaph_final_figures_v0_2.py` — current private final-figure entrypoint;
- `src/ortho_pheno/scaphoid_duration_audit_v0_1.py` — pre-validation duration audit;
- `src/ortho_pheno/duration_rules.py` — Chinese duration parser used only for engineering audit;
- `src/ortho_pheno/rules.py` — deterministic anatomy/state audit rules;
- `src/ortho_pheno/procedure_rules.py` — procedure attribution/component audit rules.

Synthetic regression tests protect anatomy disambiguation, procedure attribution, Chinese duration parsing, Reviewer-1/Reviewer-2 separation, two-stage Gold ID dependencies, post-Gold statistics, and public privacy suppression.

## Interpretation boundary

This study can test associations between physician-confirmed presentation state, documented duration, and **documented operative composition**.

It cannot establish:

- future nonunion risk;
- postoperative union or healing time;
- treatment efficacy;
- causal treatment selection;
- superiority of one graft/fixation strategy;
- a clinical duration threshold at which grafting should be performed.

## Secondary data domains

The fixed archive also contains hallux-valgus and first-CMC OA records. Those analyses are retained as secondary/supplementary work and do not define the current manuscript.

## Privacy

The source archive contains direct identifiers and protected clinical text. **No raw patient data, pseudonymized row-level data, admission identifiers, patient-level dates, clinical free text, Reviewer-1/Reviewer-2 packets, adjudication files, exact private manuscript outputs, or pseudonym salts are committed to this public repository.**

Public artifacts apply small-cell and small-denominator suppression when necessary to prevent reverse engineering of patient-level counts.
