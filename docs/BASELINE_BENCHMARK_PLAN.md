# Frozen Baseline Benchmark Plan

## Objective

Benchmark the current deterministic extraction system against the physician reference standard before evaluating any LLM-assisted method.

## Evaluation order

The order is fixed to prevent post-hoc baseline weakening:

1. phenotype v0.3 deterministic rules;
2. terminology/dictionary augmentation, if implemented as a distinct prespecified system;
3. LLM-assisted structured extraction;
4. hybrid extraction.

All systems are evaluated on identical locked gold-standard labels.

## Tasks

### Disease/anatomy classification

- hallux-valgus status;
- scaphoid anatomy: wrist scaphoid / foot navicular / other / uncertain;
- first-CMC OA status and competing-diagnosis labels.

Metrics:

- accuracy;
- class-level precision/recall/F1;
- macro-F1;
- Cohen's kappa where appropriate;
- confusion matrix.

### Scaphoid clinical state

Multi-class state:

- acute/new;
- established chronic;
- established nonunion;
- chronic/nonunion not distinguishable;
- insufficient/uncertain.

Secondary collapsed binary phenotype:

- established chronic/nonunion;
- not established chronic/nonunion.

Metrics:

- multi-class accuracy and macro-F1;
- binary sensitivity, specificity, PPV, NPV and F1;
- source-scope violation count.

### Procedure extraction

Multi-label tasks by disease:

- hallux valgus: osteotomy, Chevron, Akin, Scarf, fusion, K-wire, resection, soft-tissue procedure;
- scaphoid: internal fixation, bone graft, reconstruction, fusion, hardware removal, debridement;
- first-CMC OA: trapeziectomy, tendon procedure, ligament procedure, arthroplasty, fusion.

Metrics:

- per-label precision/recall/F1;
- macro-F1;
- micro-F1;
- exact-set match;
- mean absolute label-cardinality error.

## Error analysis

Each discordance is assigned one prespecified error type:

- anatomical confusion;
- negation failure;
- temporal/state confusion;
- broad-term overcalling;
- synonym/variant miss;
- procedure-component omission;
- unsupported semantic inference;
- source-scope violation;
- documentation insufficiency.

## Statistical uncertainty

Confidence intervals should be estimated at the admission-episode level, preferably by bootstrap when sample size and class frequency permit. Extremely sparse labels are reported descriptively and are not used to make comparative superiority claims.

## Decision rule for adding an LLM claim

A claim that semantic/LLM extraction improves the deterministic baseline requires all of the following:

- the physician reference standard was frozen before LLM scoring;
- both systems were evaluated on identical records;
- improvement is shown on prespecified metrics rather than a selectively chosen label;
- error analysis demonstrates that gains are clinically plausible rather than due to leakage or relaxed specificity;
- uncertainty intervals and rare-label limitations are reported.

If these conditions are not met, the LLM component remains an exploratory engineering demonstration rather than a validated scientific contribution.
