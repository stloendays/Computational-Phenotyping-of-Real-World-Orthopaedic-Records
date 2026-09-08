# Frozen Baseline Benchmark Plan

## Objective

Benchmark the current deterministic extraction system against the physician reference standard before evaluating any LLM-assisted method.

## Evaluation order

The order is fixed to prevent post-hoc baseline weakening:

1. phenotype-v0.3 deterministic rules;
2. terminology/dictionary augmentation, if implemented as a distinct prespecified system;
3. LLM-assisted structured extraction;
4. hybrid extraction.

All systems are evaluated on identical locked gold-standard labels.

`src/ortho_pheno/generate_rule_predictions.py` generates the deterministic baseline predictions locally. It removes all `gold_*` columns before applying extraction rules, creating a code-level barrier against accidental reference-label leakage.

## Task 1: Disease/anatomy classification

- hallux-valgus status;
- scaphoid anatomy: wrist scaphoid / foot navicular / other / uncertain;
- first-CMC OA status and competing-diagnosis labels.

Metrics:

- accuracy;
- class-level precision/recall/F1;
- macro-F1;
- Cohen's kappa where appropriate;
- confusion matrix.

## Task 2: Scaphoid clinical state

Gold multi-class state:

- acute/new;
- established chronic;
- established nonunion;
- chronic/nonunion not distinguishable;
- insufficient/uncertain.

The deterministic v0.3 rule system is primarily benchmarked on the prespecified binary collapse:

- established chronic/nonunion;
- other/not established chronic/nonunion.

Operative text is prohibited from this task.

Metrics:

- multi-class metrics for systems that output the full state taxonomy;
- binary sensitivity, specificity, PPV, NPV and F1 for the frozen collapsed task;
- source-scope violation count.

## Task 3: Target-disease procedure attribution

Every strict-cohort admission with a detailed operative-note module is retained, including operations unrelated to the study disease.

Gold label:

`target_disease_procedure_present = yes / no / uncertain`

Current module-available workloads:

- hallux valgus: 114;
- wrist scaphoid: 31;
- first-CMC OA: 18.

Current deterministic disease-concordant counts (not shown to reviewers) are 113, 28 and 18, respectively.

Metrics:

- accuracy;
- precision/recall/F1 for target-disease procedure present;
- specificity against unrelated-operation hard negatives;
- Cohen's kappa;
- confusion matrix.

This task directly measures cross-anatomy procedure-attribution leakage.

## Task 4: Procedure-component extraction

For physician-adjudicated target-disease procedure records, evaluate multi-label components.

### Hallux valgus

- osteotomy;
- Chevron;
- Akin;
- Scarf;
- fusion/arthrodesis;
- K-wire/steel-wire fixation;
- resection;
- soft-tissue procedure.

### Scaphoid

- internal fixation;
- bone graft;
- reconstruction;
- fusion/arthrodesis;
- hardware removal;
- debridement.

### First-CMC OA

- trapeziectomy;
- tendon procedure;
- ligament procedure;
- arthroplasty;
- fusion/arthrodesis.

Metrics:

- per-label precision/recall/F1;
- macro-F1;
- micro-F1;
- exact-set match;
- mean absolute label-cardinality error.

## Task 5: End-to-end procedure phenotype

A system receives credit only when it both:

1. correctly identifies whether the note documents a target-disease operation; and
2. recovers the target-disease procedure components.

This end-to-end result is reported alongside the conditional component-extraction metrics so that a system cannot appear superior by performing well only after an oracle relevance filter.

## Error analysis

Each discordance is assigned one prespecified error type:

- anatomical confusion;
- negation failure;
- temporal/state confusion;
- procedure-attribution error;
- broad-term overcalling;
- synonym/variant miss;
- procedure-component omission;
- unsupported semantic inference;
- source-scope violation;
- documentation insufficiency.

## Statistical uncertainty

Confidence intervals should be estimated at the admission-episode level, preferably by bootstrap when sample size and class frequency permit. Extremely sparse labels are reported descriptively and are not used to make comparative-superiority claims.

## Decision rule for adding an LLM claim

A claim that semantic/LLM extraction improves the deterministic baseline requires all of the following:

- the physician reference standard was frozen before LLM scoring;
- baseline predictions were generated without access to `gold_*` fields;
- both systems were evaluated on identical records;
- procedure relevance and procedure components were both evaluated;
- improvement is shown on prespecified metrics rather than a selectively chosen label;
- error analysis demonstrates clinically plausible gains rather than relaxed specificity or attribution leakage;
- uncertainty intervals and rare-label limitations are reported.

If these conditions are not met, the LLM component remains an exploratory engineering demonstration rather than a validated scientific contribution.
