# Research Roadmap

## Phase 0 - Freeze scope

Status: in progress

- [x] Fix study to currently available local data only.
- [x] Define disease roles.
- [x] Draft strict phenotype definitions.
- [x] Prespecify inference boundaries.
- [x] Add repository-level PHI safeguards.
- [ ] Freeze v0.1 after first deterministic audit.

## Phase 1 - Cohort reconstruction

Goal: convert heterogeneous source exports to one auditable episode-level dataset.

Deliverables:

- patient/admission deduplication script;
- source-table inventory;
- calendar-period completeness audit;
- strict disease classification;
- anatomical ambiguity report;
- aggregate cohort flow table.

Acceptance criteria:

- no raw row counted as an independent patient episode;
- every strict inclusion/exclusion decision has a versioned rule;
- unresolved cases remain explicit rather than silently forced into a class.

## Phase 2 - Deterministic phenotype baseline

Goal: establish a transparent baseline before any LLM-assisted extraction.

Deliverables:

- regex/dictionary extractor;
- procedure multi-label extractor;
- scaphoid anatomy/chronicity classifier;
- first-CMC strict classifier;
- synthetic unit tests.

Acceptance criteria:

- all rules pass synthetic positive, negative, negation and ambiguity tests;
- rule failures are documented in an error taxonomy.

## Phase 3 - Physician-reviewed evaluation set

Goal: create a fixed gold-standard subset from the existing records.

Deliverables:

- annotation guideline;
- blinded/frozen evaluation IDs stored outside public GitHub;
- adjudication protocol;
- inter-rater agreement where two reviewers are available.

Acceptance criteria:

- evaluation labels frozen before comparing semantic/LLM systems;
- no test-set examples used for prompt/rule tuning.

## Phase 4 - Semantic/LLM phenotyping

Goal: test whether semantic extraction adds measurable value beyond deterministic rules.

Systems:

- regex baseline;
- terminology baseline;
- LLM structured extraction;
- hybrid pipeline.

Primary outputs:

- precision/recall/F1;
- macro/micro-F1 for procedures;
- error categories;
- confidence intervals.

Go/no-go rule:

If semantic methods do not materially improve clinically important phenotype recovery, retain the simpler auditable baseline.

## Phase 5 - Scaphoid clinical analysis

Goal: compare established chronic/nonunion and acute/other wrist-scaphoid phenotypes.

Primary outputs:

- cohort characteristics;
- treatment-component frequencies;
- treatment-complexity comparison;
- effect sizes and 95% CIs;
- parsimonious Firth/logistic model only if supported by sample size;
- strict/broad and calendar-period sensitivity analyses.

Interpretation boundary:

Do not describe the model as predicting incident nonunion unless progression is explicitly established within existing longitudinal records.

## Phase 6 - Hallux valgus treatment-pattern analysis

Goal: characterize real-world operative heterogeneity from free-text surgery records.

Primary outputs:

- procedure label prevalence;
- co-occurrence network/matrix;
- dominant procedure combinations;
- exploratory association with available baseline phenotypes.

No recurrence or long-term efficacy claim is planned.

## Phase 7 - First CMC cross-disease validation

Goal: quantify the failure of broad keyword retrieval and test strict anatomical phenotyping.

Primary outputs:

- broad vs strict cohort counts;
- competing-diagnosis taxonomy;
- strict classification performance;
- transfer performance of the common phenotype architecture.

## Phase 8 - Manuscript validation package

Before manuscript claims are frozen:

- reproduce all tables/figures from scripts;
- repeat strict/broad sensitivity analyses;
- perform leakage audit;
- verify denominators manually against aggregate cohort audit;
- freeze configs and hashes;
- generate a claim-to-evidence table.

## Candidate manuscript structure

1. Introduction: real-world EHR heterogeneity as a barrier to orthopaedic phenotyping.
2. Methods: fixed-data cohort reconstruction, phenotype definitions, NLP validation and clinical analyses.
3. Results I: cohort reconstruction and diagnostic disambiguation.
4. Results II: NLP/procedure extraction validation.
5. Results III: scaphoid phenotype and treatment-complexity analysis.
6. Results IV: hallux-valgus procedural heterogeneity and CMC cross-disease validation.
7. Discussion: auditable computational phenotyping, generalizability, documentation bias and inference limits.
