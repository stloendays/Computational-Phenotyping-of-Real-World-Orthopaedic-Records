# Validation Gate

## Current status

The deterministic cohort pipeline and aggregate analyses are implemented through phenotype definition v0.3. The next manuscript-level evidence gate is a physician-reviewed reference standard generated from the existing fixed records.

No LLM-assisted extraction result is treated as validated before this gate is completed.

## Locked sequence

1. Generate the local-only annotation packet with `src/ortho_pheno/make_annotation_packet.py`.
2. Complete primary physician annotation without exposure to deterministic-rule or model predictions.
3. Complete the deterministic approximately 20% independent second-review subset.
4. Resolve prespecified disagreements by consensus or senior adjudication.
5. Freeze the gold-standard files locally and record a version/hash in the protected environment.
6. Benchmark the deterministic regex/rule baseline first.
7. Evaluate dictionary, LLM-assisted and hybrid systems on the exact same locked labels.
8. Generate only aggregate public metrics using `src/ortho_pheno/evaluate_annotations.py`.

## Current annotation workload

- disease/anatomy: 367 candidate admission episodes;
- scaphoid clinical state: 68 high-specificity wrist-scaphoid episodes;
- multi-label procedures: 163 detailed operative notes;
- approximately 20% deterministic stratified second review.

## Prohibited shortcuts

- changing gold labels to improve a model score;
- excluding ambiguous cases after observing model errors;
- using operative text to assign scaphoid chronic/nonunion state in the treatment-comparison analysis;
- tuning extraction rules on the final gold-standard evaluation labels without documenting a new development/evaluation split;
- publishing patient-level annotation files, pseudonymous study IDs or source text.

## Required public outputs after validation

At minimum:

- physician inter-rater reliability;
- deterministic baseline precision/recall/F1;
- LLM-assisted extraction precision/recall/F1 on the same frozen labels;
- macro/micro-F1 and exact-set match for procedure extraction;
- prespecified error taxonomy counts;
- a versioned statement of all model names/configurations used.

Until these outputs exist, current clinical associations remain explicitly exploratory.
