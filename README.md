# Real-World Scaphoid Treatment Composition Study

This repository supports a **problem-first retrospective study** of wrist-scaphoid presentations using a fixed export of routinely collected hospital EHR data.

## Primary scientific question

> **Among physician-confirmed wrist-scaphoid admissions with disease-concordant detailed operative documentation, is established chronic/nonunion associated with greater bone-graft augmentation than physician-confirmed acute/new fracture while internal fixation remains common in both groups?**

Computational text processing is used only to recover and validate the clinical variables needed to answer this question. It is not the scientific objective of the paper.

## Data-derived signal motivating the study

The deterministic pre-validation audit showed a treatment-composition pattern in which internal fixation was frequent across operative wrist-scaphoid records, whereas bone grafting was concentrated in records with established chronic/nonunion terminology.

| Operative component | Established chronic/nonunion | Deterministic non-chronic comparison* |
|---|---:|---:|
| Internal fixation | 14/15 (93.3%) | 12/13 (92.3%) |
| Bone graft | 8/15 (53.3%) | `<5/13` |
| Graft/reconstruction/fusion augmentation | 9/15 (60.0%) | `<5/13` |

\*The 13 deterministic comparison records are **not** assumed to be acute. Final clinical inference uses only physician-confirmed `acute_or_new_fracture` records.

The proposed signal is therefore narrower than “chronic cases receive more complex surgery”: a mechanical fixation base may remain common while biological/reconstructive augmentation changes with presentation state.

All deterministic values are provisional until physician adjudication.

## Secondary mechanistic hypothesis

A separate pre-validation audit performed after the primary question was selected identified a possible duration gradient within established chronic/nonunion operative records:

- graft-positive with explicit duration: 7/8, median **182.6 days**;
- graft-negative with explicit duration: 6/7, median **15.0 days**.

This does not replace the primary endpoint. Final duration is physician adjudicated, automated parser output is hidden from reviewers, and no locally optimized duration cutoff is permitted.

## Pre-validation cohort audit

The supplied broad scaphoid retrieval contains **88** candidate admission episodes. Phenotype v0.3 partitions them into:

- **68** deterministic wrist-scaphoid admissions;
- **13** explicit foot-navicular admissions;
- **7** anatomically ambiguous admissions.

Within the deterministic wrist group, **23** contain established chronic/nonunion terminology.

The deterministic operative audit identifies 31 detailed-note module records and 28 disease-concordant detailed operative records. All 28 occur in **2023-2025**.

These are engineering audit counts, not the final physician-defined clinical cohort.

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

The primary comparison is fixed as:

- **established chronic/nonunion** = the three established categories;
- **acute/new** = physician-confirmed `acute_or_new_fracture` only.

`insufficient_or_uncertain` is excluded from state-based inference.

There is no separate acute-only sensitivity analysis because acute/new is already the primary comparison group. This correction was made before physician Gold completion and did not change the primary outcome.

For physician-confirmed wrist records with detailed operative documentation, reviewers first determine whether the note actually documents a wrist-scaphoid procedure before labeling fixation, graft, reconstruction, and fusion.

## Outcome hierarchy

### Primary

**Bone-graft augmentation**.

### Key contrast

**Internal fixation**.

### Secondary

- graft/reconstruction/fusion augmentation composite;
- major procedure-component count;
- individual reconstruction/fusion components when informative;
- physician-adjudicated relevant duration within established chronic/nonunion.

The primary outcome cannot be replaced because another analysis yields a smaller P value.

## Final post-Gold pipeline

After physician Gold is adjudicated and SHA-256 frozen:

1. `freeze_scaph_reference_v0_2.py` freezes the current reference standard and analysis-plan metadata;
2. `analyze_scaph_gold_v0_2.py` produces the exact private manuscript analysis and privacy-suppressed public summary;
3. `build_scaph_final_tables_v0_1.py` creates manuscript-ready Table 1, Table 2, and duration Supplementary Table S1;
4. `build_scaph_final_figures_v0_2.py` creates final article-style Figure 1-3.

The current analysis includes Fisher exact tests, conditional OR/95% CI, internal-fixation contrast, augmentation/component-count secondary analyses, leave-one-out influence analysis, and physician-adjudicated duration analysis.

Uncertain procedure-component labels are excluded from the corresponding denominator rather than silently coded as negative.

Detailed execution order: `docs/SCAPHOID_POST_GOLD_RUNBOOK_V0_1.md`.

## Current manuscript and submission-preparation files

- `manuscript/SCAPHOID_MANUSCRIPT_DRAFT_V0_5.md` — **current English manuscript draft**, strengthened for routine-EHR reporting;
- `docs/MANUSCRIPT_PLAN_SCAPHOID_V0_2.md` — focused article structure and clinical figure plan;
- `docs/SCAPHOID_SCIENTIFIC_QUESTION_V0_1.md` — scientific question and claim boundaries;
- `docs/SCAPHOID_ANALYSIS_PLAN_V0_3.md` — current statistical plan;
- `docs/SCAPHOID_ANALYSIS_CHANGELOG_V0_1.md` — transparent pre-Gold analysis changes;
- `docs/SCAPHOID_DURATION_SECONDARY_HYPOTHESIS_V0_1.md` — frozen duration hypothesis;
- `docs/SCAPHOID_PHYSICIAN_REVIEW_GUIDE_ZH.md` — physician review guide;
- `docs/SCAPHOID_NOVELTY_AUDIT_V0_1.md` — novelty/claim boundary audit;
- `docs/STROBE_RECORD_MAPPING_V0_1.md` — STROBE + RECORD reporting audit tailored to this dataset;
- `docs/JWS_SUBMISSION_PREP_V0_1.md` — Journal of Wrist Surgery submission preparation;
- `docs/TARGET_JOURNAL_SHORTLIST_V0_1.md` — target-journal shortlist.

## Validation and analysis code

- `src/ortho_pheno/make_scaph_physician_packet_v0_1.py`
- `src/ortho_pheno/make_scaph_adjudication_templates_v0_1.py`
- `src/ortho_pheno/freeze_scaph_reference_v0_2.py`
- `src/ortho_pheno/analyze_scaph_gold_v0_2.py`
- `src/ortho_pheno/build_scaph_final_tables_v0_1.py`
- `src/ortho_pheno/build_scaph_final_figures_v0_2.py`
- `src/ortho_pheno/scaphoid_duration_audit_v0_1.py`
- `src/ortho_pheno/duration_rules.py`
- `src/ortho_pheno/rules.py`
- `src/ortho_pheno/procedure_rules.py`

Synthetic regression tests protect anatomy disambiguation, procedure attribution, Chinese duration parsing, Reviewer-1/Reviewer-2 separation, two-stage Gold ID dependencies, freeze metadata, post-Gold statistics, final table formatting, and public privacy suppression.

## Interpretation boundary

This study can test associations between physician-confirmed presentation state, documented duration, and **documented operative composition**.

It cannot establish:

- future nonunion risk;
- postoperative union or healing time;
- treatment efficacy;
- causal treatment selection;
- superiority of one graft/fixation strategy;
- a clinical duration threshold at which grafting should be performed.

## Current blockers before submission

The main scientific blocker remains physician Gold (Issue #3).

Administrative submission blockers also remain:

- actual ethics/IRB committee name and approval/reference number;
- whether informed consent was obtained or waived;
- funding statement;
- author conflict-of-interest disclosures;
- final journal-format reference verification.

These details must come from authoritative study/author records and will not be inferred.

## Privacy

The source archive contains direct identifiers and protected clinical text. **No raw patient data, pseudonymized row-level data, admission identifiers, patient-level dates, clinical free text, Reviewer-1/Reviewer-2 packets, adjudication files, exact private manuscript outputs, or pseudonym salts are committed to this public repository.**

Public artifacts apply small-cell and small-denominator suppression when necessary to prevent reverse engineering of patient-level counts.
