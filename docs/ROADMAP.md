# Research Roadmap

## Current gate

**Current human-validation gate:** physician reference-standard annotation v0.1 (GitHub Issue #2).

The deterministic pipeline, cohort audits, privacy-preserving aggregate release, synthetic regression tests, annotation-packet generator, deterministic prediction exporter and evaluation harness are implemented. No LLM-assisted extraction claim is promoted to manuscript evidence until the physician reference standard is frozen.

## Phase 0 - Freeze scope

**Status: complete through phenotype v0.3**

- [x] Fix study to currently available local data only.
- [x] Define disease roles.
- [x] Prespecify inference boundaries.
- [x] Add repository-level PHI safeguards.
- [x] Freeze versioned phenotype definitions.
- [x] Preserve v0.1/v0.2 rule history rather than silently overwriting it.
- [x] Freeze v0.3 explicit scaphoid anatomy uncertainty after cross-pipeline audit.

Current deterministic scaphoid anatomy audit: 68 wrist scaphoid / 13 foot navicular / 7 ambiguous from 88 candidates.

## Phase 1 - Cohort reconstruction

**Status: complete for current fixed-data audit**

Goal: convert heterogeneous source exports to one auditable admission-episode dataset.

Completed deliverables:

- [x] admission-level deduplication;
- [x] complete 18-file source-table inventory;
- [x] calendar-period completeness audit;
- [x] strict disease classification;
- [x] explicit scaphoid anatomy ambiguity report;
- [x] aggregate cohort flow/coverage outputs;
- [x] small-cell-suppressed public release.

Acceptance criteria met:

- no raw diagnosis row is treated as an independent episode;
- every current strict inclusion/exclusion decision has a versioned rule;
- unresolved scaphoid anatomy remains `ambiguous` rather than being forced into a class.

## Phase 2 - Deterministic phenotype baseline

**Status: complete for pre-annotation baseline implementation**

Goal: establish a transparent baseline before any LLM-assisted extraction.

Completed deliverables:

- [x] deterministic disease/anatomy rules;
- [x] procedure multi-label rules;
- [x] scaphoid chronic/nonunion source-scope rule;
- [x] first-CMC strict classifier;
- [x] local-only deterministic prediction exporter;
- [x] synthetic anatomy/leakage/procedure regression tests;
- [x] GitHub Actions CI.

The baseline is evaluated against physicians only after the gold standard is frozen; its apparent agreement with its own construction rules is not treated as validation.

## Phase 3 - Physician reference standard

**Status: current milestone / human review required**

Goal: create a fixed gold standard from the existing records without acquiring new clinical data.

Frozen workload:

- disease/anatomy: 367 candidate episodes;
- scaphoid state: 68 strict wrist-scaphoid episodes;
- procedures: 163 detailed operative notes;
- approximately 20% deterministic stratified independent second review.

Completed infrastructure:

- [x] annotation guideline;
- [x] annotation schema;
- [x] local-only packet generator;
- [x] deterministic second-review manifest generation;
- [x] evaluation harness for categorical and multi-label metrics;
- [x] validation gate and deterministic-first benchmark plan.

Remaining human tasks:

- [ ] primary physician annotation;
- [ ] independent second review;
- [ ] adjudication of disagreements;
- [ ] freeze local gold-standard version/hash;
- [ ] calculate inter-rater reliability.

Acceptance criteria:

- evaluation labels frozen before model scoring;
- reviewers blinded to rule/model predictions during primary annotation;
- no gold label changed merely because a model disagrees.

## Phase 4 - Semantic/LLM phenotyping

**Status: blocked by Phase 3 by design**

Goal: test whether semantic extraction adds measurable value beyond deterministic rules.

Locked evaluation order:

1. phenotype v0.3 deterministic baseline;
2. terminology/dictionary baseline if implemented;
3. LLM structured extraction;
4. hybrid pipeline.

Primary outputs:

- precision/recall/F1;
- accuracy and Cohen's kappa for categorical phenotypes;
- macro/micro-F1 and exact-set match for procedures;
- prespecified error taxonomy;
- uncertainty intervals where supported.

Go/no-go rule:

If semantic methods do not materially improve clinically important phenotype recovery without unacceptable specificity loss, retain the simpler auditable baseline.

## Phase 5 - Scaphoid clinical analysis

**Status: exploratory aggregate analysis complete; confirmatory interpretation pending phenotype validation**

Current primary deterministic comparison:

- 23 established chronic/nonunion episodes;
- 45 other high-specificity wrist-scaphoid episodes.

2023-2025 sensitivity cohort:

- 18 established chronic/nonunion;
- 14 comparison episodes.

Completed outputs:

- [x] cohort characteristics;
- [x] treatment-component frequencies;
- [x] all-year documentation-bias audit;
- [x] 2023-2025 consistent-era sensitivity analysis;
- [x] public small-cell suppression.

Remaining after validation:

- [ ] regenerate comparison using physician-adjudicated phenotypes;
- [ ] assess whether adjusted/Firth modelling is supportable after final event counts;
- [ ] freeze manuscript-level effect estimates.

Interpretation boundary:

Do not describe the analysis as predicting incident nonunion unless progression is explicitly established within existing longitudinal records.

## Phase 6 - Hallux valgus treatment-pattern analysis

**Status: exploratory aggregate analysis complete; procedure-label validation pending**

Completed outputs:

- [x] procedure prevalence;
- [x] pairwise procedure co-occurrence;
- [x] common multi-label procedure combinations;
- [x] exploratory Chevron/fusion contrasts using available baseline phenotypes.

Current hypothesis-generating signal:

A bilateral-disease mention is more frequent in Chevron-positive than Chevron-negative detailed operative episodes. This result remains exploratory until bilateral and Chevron labels are physician-validated.

No recurrence or long-term efficacy claim is planned.

## Phase 7 - First-CMC cross-disease validation

**Status: deterministic audit complete; physician validation pending**

Completed outputs:

- [x] broad vs strict cohort counts;
- [x] competing-diagnosis audit;
- [x] strict anatomical rule implementation.

Remaining:

- [ ] physician precision/recall benchmark;
- [ ] compare deterministic vs semantic extraction specificity;
- [ ] quantify error categories in broad-term overcalling.

## Phase 8 - Manuscript validation package

**Status: scaffolded, not yet frozen**

Before manuscript claims are frozen:

- [ ] reproduce all final tables/figures from scripts;
- [ ] rerun strict/broad sensitivity analyses on physician-adjudicated labels;
- [ ] complete leakage/source-scope audit;
- [ ] verify all denominators against the versioned cohort audit;
- [ ] freeze configs, model identifiers and hashes;
- [ ] generate final claim-to-evidence matrix;
- [ ] classify each claim as validated, exploratory, negative or unsupported.

## Candidate manuscript structure

1. Introduction: real-world EHR heterogeneity as a barrier to orthopaedic phenotyping.
2. Methods: fixed-data cohort reconstruction, explicit anatomy uncertainty, physician reference standard, NLP validation and clinical analyses.
3. Results I: row inflation, source-system shift and anatomical/diagnostic disambiguation.
4. Results II: physician agreement and deterministic/semantic extraction validation.
5. Results III: scaphoid established-phenotype and treatment-complexity analysis.
6. Results IV: hallux-valgus procedural heterogeneity and first-CMC hard-negative validation.
7. Discussion: auditable computational phenotyping, Chinese lexical ambiguity, documentation-process bias, generalizability and inference limits.
