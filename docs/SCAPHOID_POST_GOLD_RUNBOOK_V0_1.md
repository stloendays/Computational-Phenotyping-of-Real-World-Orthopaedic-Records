# Scaphoid Post-Gold Runbook v0.1

This runbook defines the **only supported execution order** from physician review to final manuscript statistics and figures.

It is intentionally procedural. It does not redefine the scientific question or statistical plan.

## 0. Private paths

Use local paths outside the public repository for raw clinical data, physician review files, pseudonym salt, exact manuscript results, and final unsuppressed figures.

Example shell variables:

```bash
RAW_DIR="/secure/path/to/手足外科"
REVIEW_DIR="/secure/path/to/scaphoid_review"
SALT_FILE="/secure/path/to/scaphoid_salt.txt"
PRIVATE_OUT="outputs/private/scaphoid"
```

`annotations/private/` and `outputs/private/` are ignored by Git and must remain private.

---

# Stage 1 — anatomy

## 1. Generate the frozen Stage-1 review packet

```bash
python src/ortho_pheno/make_scaph_physician_packet_v0_1.py \
  --raw-dir "$RAW_DIR" \
  --output-dir "$REVIEW_DIR" \
  --salt-file "$SALT_FILE" \
  anatomy
```

Expected primary review population under the frozen source package: **88 broad scaphoid candidates**.

Reviewer 1 completes:

`scaphoid_anatomy_review.csv`

Reviewer 2 independently completes:

`scaphoid_anatomy_review_reviewer2.csv`

Reviewer 2 must not see Reviewer-1 labels, deterministic predictions, model outputs, or clinical effect estimates.

## 2. Build the anatomy adjudication template

```bash
python src/ortho_pheno/make_scaph_adjudication_templates_v0_1.py \
  --review-dir "$REVIEW_DIR" \
  --layer anatomy
```

This creates:

`scaphoid_anatomy_adjudicated.csv`

Rules:

- non-double-reviewed records inherit Reviewer 1;
- double-reviewed exact agreements inherit the agreed label;
- disagreements remain blank;
- blank disagreements require explicit adjudicator/consensus resolution.

Do not overwrite Reviewer-1 or Reviewer-2 files.

## 3. Freeze Stage-1 anatomy Gold

After all `gold_anatomy_label` values in the adjudicated file are complete:

```bash
mkdir -p "$PRIVATE_OUT"

python src/ortho_pheno/freeze_scaph_reference_v0_2.py \
  --review-dir "$REVIEW_DIR" \
  --stage stage1 \
  --output "$PRIVATE_OUT/scaphoid_stage1_reference_manifest.json"
```

Do not generate Stage 2 before this command passes.

---

# Stage 2 — state, duration, and procedure

## 4. Generate Stage-2 review packets from physician anatomy Gold

```bash
python src/ortho_pheno/make_scaph_physician_packet_v0_1.py \
  --raw-dir "$RAW_DIR" \
  --output-dir "$REVIEW_DIR" \
  --salt-file "$SALT_FILE" \
  downstream \
  --anatomy-gold "$REVIEW_DIR/scaphoid_anatomy_adjudicated.csv"
```

The generated state population is defined by physician-confirmed `wrist_scaphoid`, not by the deterministic 68-record rule cohort.

Reviewer 1 completes:

- `scaphoid_state_review.csv`
- `scaphoid_procedure_review.csv`

Reviewer 2 independently completes:

- `scaphoid_state_review_reviewer2.csv`
- `scaphoid_procedure_review_reviewer2.csv`

The state review includes physician-defined duration fields. Automated duration-parser values must remain hidden from reviewers.

## 5. Build Stage-2 adjudication templates

```bash
python src/ortho_pheno/make_scaph_adjudication_templates_v0_1.py \
  --review-dir "$REVIEW_DIR" \
  --layer state

python src/ortho_pheno/make_scaph_adjudication_templates_v0_1.py \
  --review-dir "$REVIEW_DIR" \
  --layer procedure
```

This creates:

- `scaphoid_state_adjudicated.csv`
- `scaphoid_procedure_adjudicated.csv`

Resolve all blank disagreement rows explicitly.

Do not convert `uncertain` to `no` merely to increase sample size.

---

# Final Gold freeze

## 6. Freeze the final two-stage physician reference standard

```bash
python src/ortho_pheno/freeze_scaph_reference_v0_2.py \
  --review-dir "$REVIEW_DIR" \
  --stage final \
  --output "$PRIVATE_OUT/scaphoid_final_reference_manifest.json"
```

This command validates:

- all 88 Stage-1 candidate IDs;
- physician-confirmed wrist-scaphoid downstream population;
- state controlled vocabulary;
- duration value/unit/basis consistency;
- procedure relevance/component consistency;
- Reviewer-2 ID sets against frozen manifests;
- final adjudicated state/procedure ID populations;
- SHA-256 hashes of the frozen files.

The final manifest records `SCAPHOID_ANALYSIS_PLAN_V0_3`, the primary comparison, and the primary outcome.

No final clinical analysis should be run before this stage passes.

---

# Final manuscript statistics

## 7. Run the current post-Gold analysis entrypoint

```bash
python src/ortho_pheno/analyze_scaph_gold_v0_2.py \
  --review-dir "$REVIEW_DIR" \
  --raw-dir "$RAW_DIR" \
  --salt-file "$SALT_FILE" \
  --private-output "$PRIVATE_OUT/scaphoid_manuscript_analysis.json" \
  --public-output "$PRIVATE_OUT/scaphoid_public_safe_summary.csv"
```

The current analysis is fixed as:

### Primary comparison

`established chronic/nonunion` vs physician-confirmed `acute/new fracture`.

### Primary outcome

Bone-graft augmentation.

### Primary statistics

- 2x2 table;
- two-sided Fisher exact test;
- conditional odds ratio;
- 95% confidence interval.

### Key contrast

Internal fixation.

### Secondary analyses

- graft/reconstruction/fusion augmentation composite;
- major procedure-component count;
- leave-one-out influence analysis;
- physician-adjudicated duration within established chronic/nonunion;
- injury-basis-only duration analysis when evaluable.

`uncertain` procedure-component labels are excluded from the corresponding binary denominator; they are never silently recoded to `no`.

The exact JSON is private. Public release requires small-cell and small-denominator suppression.

---

# Final manuscript figures

## 8. Generate final article-style figures

```bash
python src/ortho_pheno/build_scaph_final_figures_v0_2.py \
  --review-dir "$REVIEW_DIR" \
  --private-analysis-json "$PRIVATE_OUT/scaphoid_manuscript_analysis.json" \
  --output-dir "$PRIVATE_OUT/figures"
```

Expected private outputs:

- `Figure1_physician_cohort_flow.svg`
- `Figure2_operative_composition.svg`
- `Figure3_duration_by_graft.svg`

These figures may contain exact small-group counts or individual duration points and therefore remain private until manuscript/privacy review is complete.

---

# Manuscript update order

After the exact post-Gold analysis is generated:

1. replace `[pending]` physician cohort counts in `SCAPHOID_MANUSCRIPT_DRAFT_V0_4.md`;
2. insert the primary bone-graft OR, 95% CI, and Fisher P;
3. insert internal-fixation key-contrast estimates;
4. insert secondary component-count results;
5. insert physician-adjudicated duration results;
6. review leave-one-out influence before finalizing strength-of-claim language;
7. update Figure 1-3 and table captions;
8. reverify every literature citation and journal formatting requirement;
9. keep deterministic pre-validation values explicitly labelled as hypothesis-generating or move them to Supplementary material if the final journal structure is cleaner without them.

---

# Prohibited post-Gold changes

After physician Gold is frozen, do **not**:

- redefine the primary comparison;
- replace bone graft with a more significant composite as the primary outcome;
- search for a duration cutoff that maximizes significance;
- add high-dimensional ML because the clinical association is weak;
- recode uncertain labels as negative to improve precision;
- remove an influential patient merely because leave-one-out changes the result;
- claim postoperative efficacy, future nonunion risk, or causal treatment selection.

Any unavoidable post-Gold deviation must be added to `SCAPHOID_ANALYSIS_CHANGELOG_V0_1.md` with the reason, timing, and whether outcome estimates were visible when the change was made.
