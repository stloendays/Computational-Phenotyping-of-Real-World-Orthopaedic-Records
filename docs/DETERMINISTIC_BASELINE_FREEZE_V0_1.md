# Deterministic Baseline Freeze v0.1

## Purpose

The deterministic rule baseline was generated and cryptographically frozen **before any physician gold-standard labels were entered**. This prevents post-hoc rule tuning against the reference standard and provides a reproducible comparator for later dictionary, LLM-assisted and hybrid systems.

## Pre-gold condition

At prediction-generation time, the local private annotation packets contained:

- disease/anatomy review rows: **367**;
- scaphoid-state review rows: **68**;
- procedure review rows: **163**;
- nonblank cells across every `gold_*` column: **0**.

The prediction generator also removes every `gold_*` field before passing a row to any prediction function. This behaviour is protected by synthetic regression tests.

## Frozen private predictions

The prediction rows remain private because they contain pseudonymous study IDs. Only aggregate metadata and cryptographic hashes are published.

| Private prediction file | Rows | SHA-256 |
|---|---:|---|
| `rule_disease_anatomy_predictions.csv` | 367 | `56d51f1795bb31ee7050acf0c38abdc29c5e234779e2f6f2dd2bf41e587823e6` |
| `rule_scaphoid_state_predictions.csv` | 68 | `620d7ab77cf3d92fd11a67e4936eacf12a0f2008f76833dac0662656c0a05f5b` |
| `rule_procedure_predictions.csv` | 163 | `0ef84299300eb1d47f74a5843b105d025f645915bacc4b0b6fde65944e0cfb05` |

Machine-readable metadata are stored in `results/DETERMINISTIC_BASELINE_FREEZE_V0_1.json`.

## Rule scope frozen at this point

The deterministic baseline includes:

- phenotype-v0.3 disease/anatomy rules;
- non-operative scaphoid chronic/nonunion state rules;
- conservative hallux laterality, bilateral-mention, pain and functional-limitation rules;
- anatomy-aware target-disease procedure attribution;
- canonical multi-label procedure-component rules.

## Anti-leakage safeguards

### Gold-field isolation

`src/ortho_pheno/generate_rule_predictions.py` strips all columns beginning with `gold_` before prediction.

### Source-scope control

Scaphoid state uses diagnosis, complaint and physical-examination text only. Operative text is excluded from state assignment.

### Procedure attribution gate

Procedure components are extracted only after the deterministic system decides that the detailed operative record is attributable to the target disease/anatomy.

### Missingness preservation

Conservative hallux baseline rules return `undocumented` when source text does not contain sufficient evidence; missing text is not converted to a clinical negative.

## Scoring rule

Official deterministic-baseline scoring occurs only after the physician reference standard is completed and frozen with `freeze_reference_standard.py`.

`score_frozen_reference.py` first verifies the physician-gold SHA-256 freeze manifest, then applies the prespecified hierarchical evaluation:

1. disease/anatomy;
2. hallux baseline phenotypes;
3. scaphoid state;
4. target-disease procedure relevance;
5. procedure components conditional on gold relevance;
6. end-to-end procedure performance.

## Post-freeze modification policy

The frozen baseline predictions must not be regenerated with modified rules and substituted as the primary comparator after physician labels are reviewed.

If a later rule revision is scientifically necessary, it must be reported as a **new versioned system** and compared separately. The v0.1 frozen predictions remain the preregistered baseline.

## Privacy

The public repository does not contain:

- study IDs;
- row-level predictions;
- physician labels;
- clinical text;
- admission identifiers.

Only file hashes, row counts, code-version metadata and aggregate validation metrics are eligible for public release.
