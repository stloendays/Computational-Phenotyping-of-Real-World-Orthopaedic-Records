# Scaphoid Main-Paper Analysis Changelog

This file records substantive analysis-design changes so that the final manuscript does not conceal protocol evolution.

## Invariant primary question

Once the focused scaphoid paper was selected, the primary clinical outcome has remained:

> **bone-graft augmentation** in established chronic/nonunion versus the appropriate non-established wrist-scaphoid comparison.

Internal fixation has remained the prespecified key contrast.

No physician-adjudicated treatment effect has been inspected because Stage-2 physician Gold is not yet complete.

---

## v0.1 — Focused scaphoid question selected

**Timing:** before scaphoid physician Gold.

Changes:

- abandoned the earlier three-disease `framework-first` manuscript concept;
- selected scaphoid treatment composition as the focused scientific problem;
- froze bone graft as primary outcome;
- froze internal fixation as key contrast;
- prohibited operative text from assigning chronic/nonunion exposure state;
- recognized that all disease-concordant detailed scaphoid operations in the supplied export occur in 2023-2025, so this period is the operative study population rather than an independent sensitivity cohort.

Reason:

The fixed data support operative-composition analysis but not postoperative healing, incident nonunion prediction, or treatment efficacy.

Primary outcome changed? **No subsequent change.**

---

## Two-stage physician cohort correction

**Timing:** before Stage-1 physician annotation was completed; all Stage-1 Gold fields blank.

Change:

- replaced downstream review restricted to deterministic wrist-scaphoid positives with a two-stage design:
  1. all 88 broad candidates receive physician anatomy adjudication;
  2. downstream state/procedure review is generated from physician-confirmed wrist scaphoid.

Reason:

Reviewing state/procedure only inside deterministic positives would create verification bias and allow the rule system to predefine the clinical cohort.

Primary outcome changed? **No.**

---

## Duration secondary hypothesis added

**Timing:** after the primary question/outcome were fixed, before Stage-2 physician Gold completion.

Change:

- added an exploratory secondary analysis of physician-adjudicated wrist-related duration within established chronic/nonunion operative records;
- duration remains continuous;
- no locally optimized threshold is allowed;
- automated duration parsing is hidden from reviewers.

Reason:

A separate pre-validation audit showed a substantial deterministic duration gradient between graft-positive and graft-negative chronic/nonunion records.

Primary outcome changed? **No.**

Can duration replace the primary result based on P value? **No.**

---

## v0.3 — Comparison-group logical correction

**Timing:** before Stage-2 physician Gold completion and before any physician-adjudicated treatment effect was inspected.

Problem identified:

The physician state vocabulary contains:

- acute/new;
- established chronic;
- established nonunion;
- chronic/nonunion not distinguishable;
- insufficient/uncertain.

Therefore, after adjudication, every sufficiently classifiable record outside the established chronic/nonunion group is necessarily `acute/new`. The previous wording of a broad classifiable comparison plus an `acute-only` sensitivity analysis would yield the same group twice.

Correction:

- primary comparison is explicitly **established chronic/nonunion vs physician-confirmed acute/new fracture**;
- insufficient/uncertain states are excluded from state-based clinical inference;
- the redundant acute-only sensitivity analysis is removed.

Reason:

Logical consistency with the physician label vocabulary, not treatment-effect optimization.

Primary outcome changed? **No.**

---

## Public-release privacy tightening

**Timing:** before final Gold analysis.

Change:

- post-Gold analysis separates exact private manuscript output from public-safe aggregate output;
- public release suppresses nonzero cells and denominators of 1-4;
- duration distributions are not released when a subgroup contains 1-4 records.

Reason:

Prevent reverse engineering of patient-level information after physician adjudication potentially changes group sizes.

Primary outcome changed? **No.**

---

## Current locked hierarchy

1. **Primary:** established chronic/nonunion vs acute/new -> bone-graft augmentation.
2. **Key contrast:** internal fixation.
3. **Secondary:** augmentation composite and major procedure-component count.
4. **Exploratory secondary mechanism:** documented duration within established chronic/nonunion -> graft augmentation.
5. **Robustness:** leave-one-out primary analysis, competing-procedure exclusion, deterministic-vs-physician measurement comparison, injury-duration-only secondary analysis when feasible.

No high-capacity predictive model, LLM performance result, composite endpoint, or secondary P value may displace this hierarchy.
