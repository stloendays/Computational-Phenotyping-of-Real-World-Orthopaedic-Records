# Claim-to-Evidence Matrix v0.1

This matrix separates data-engineering facts, deterministic phenotype findings, exploratory clinical associations and future validation claims. It is intentionally conservative and should be updated after physician adjudication.

| ID | Candidate manuscript claim | Current status | Current evidence | Validation dependency | Allowed wording now |
|---|---|---|---|---|---|
| C1 | Raw diagnosis rows cannot be treated as independent clinical episodes because repeated diagnosis coding causes severe row inflation. | Supported by source audit | `data/aggregate/source_duplication_audit.csv` | None beyond code reproducibility | Can be stated as a dataset property. |
| C2 | The supplied EHR exports exhibit a calendar-era documentation discontinuity, especially in 2019-2022. | Supported by source audit | `data/aggregate/era_module_coverage.csv`; `year_distribution.csv` | None beyond code reproducibility | Can be stated as a data-generation/documentation property, not a clinical trend. |
| C3 | Broad `舟骨` retrieval cannot be assumed to represent wrist scaphoid disease. | Strong deterministic evidence; physician confirmation pending | `scaphoid_anatomy_audit.csv`; phenotype changelog | Physician disease/anatomy adjudication | State as deterministic audit finding; final accuracy requires physician reference standard. |
| C4 | v0.3 deterministic scaphoid anatomy yields 68 wrist-scaphoid, 13 foot-navicular and 7 ambiguous candidate episodes. | Deterministic, frozen | `scaphoid_anatomy_audit.csv`; `phenotypes_v0.3.yaml` | Physician adjudication for accuracy/PPV/recall | Can report as algorithmic cohort output, not ground truth. |
| C5 | Character-level Chinese context can create anatomy errors, e.g. interpreting `手术`/`手法` as hand anatomy. | Supported by rule audit and regression tests | `PHENOTYPE_CHANGELOG.md`; `tests/test_phenotype_rules.py` | Physician validation quantifies clinical frequency/impact | Can be described as a discovered failure mode of the initial deterministic heuristic. |
| C6 | Broad first-CMC retrieval has low deterministic specificity relative to strict anatomical rules. | Deterministic evidence; physician confirmation pending | `first_cmc_disambiguation_audit.csv`; cohort overview | Physician first-CMC adjudication | Avoid calling the 28 strict cases true positives until adjudicated. |
| C7 | Hallux-valgus operative notes exhibit heterogeneous multi-label procedure patterns dominated by osteotomy, fixation, soft-tissue and resection components. | Exploratory phenotype result | `procedure_phenotype_counts.csv`; `hallux_procedure_combinations.csv`; `hallux_procedure_cooccurrence.csv` | Physician procedure annotation | Report as deterministic text-phenotype frequencies, not validated clinical procedure prevalence. |
| C8 | Bilateral-disease mention is more frequent in Chevron-positive than Chevron-negative hallux episodes. | Exploratory association | `hallux_treatment_pattern_contrasts.csv` | Physician validation of bilateral and Chevron labels; multiplicity-aware interpretation | May be presented as hypothesis-generating only. No causal treatment-selection language. |
| C9 | Established chronic/nonunion wrist-scaphoid phenotypes show more complex reconstructive treatment patterns than comparison phenotypes. | Exploratory association | `scaphoid_procedure_by_group.csv`; `scaphoid_2023_2025_sensitivity.csv` | Physician anatomy/state/procedure adjudication | State as an exploratory deterministic-phenotype treatment-pattern signal. |
| C10 | The scaphoid comparison identifies predictors of future incident nonunion. | **Not supported** | Fixed data do not establish acute baseline-to-incident-nonunion progression for all cases | Would require longitudinal outcome evidence not assumed available | Prohibited claim. |
| C11 | The dataset supports long-term postoperative efficacy, recurrence or functional recovery conclusions. | **Not supported** | Long-term outcomes are not consistently available | Would require unavailable additional local data | Prohibited claim. |
| C12 | LLM-assisted extraction improves over deterministic rules. | **Not yet tested** | No frozen physician gold-standard scores yet | Complete Issue #2 physician reference-standard annotation, then benchmark all systems on identical labels | Do not claim improvement before validation. |
| C13 | A hybrid NLP system is superior and clinically reliable across three orthopaedic domains. | **Not yet supported** | Architecture is implemented/planned; no physician-reference benchmark yet | Physician gold standard + prespecified benchmark + uncertainty/error analysis | Future claim only if benchmark criteria are met. |
| C14 | The computational framework generalizes across deformity, trauma/nonunion and degenerative hand disease. | Partially supported methodologically; clinical validation pending | Same architecture/rule infrastructure used in three domains | Cross-domain physician metrics | Can describe cross-domain implementation, not validated generalization performance. |
| C15 | Public aggregate artifacts are reproducible without disclosing patient-level clinical data. | Supported at repository-design level | safe-release builder, privacy policy, aggregate outputs, `.gitignore` | Final publication privacy audit | Can be stated as repository/reproducibility design. |

## Claim classes

### Supported data-engineering claims

C1, C2 and the repository-level component of C15 can be used before physician annotation because they concern source-file structure and reproducible data handling rather than clinical truth labels.

### Deterministic phenotype claims awaiting reference-standard validation

C3-C7 describe outputs of the current v0.3 phenotyping system. They may be reported as deterministic algorithm outputs, but their clinical accuracy must be quantified against physicians before being described as validated phenotypes.

### Exploratory clinical associations

C8 and C9 require both phenotype validation and cautious multiplicity-aware interpretation. Statistical significance from deterministic labels alone does not upgrade them to confirmatory findings.

### Prohibited claims under the fixed-data design

C10 and C11 remain unsupported regardless of model sophistication. No machine-learning method can repair the absence of the required longitudinal outcomes.

### Future AI-validation claims

C12-C14 are blocked by the physician reference standard. Model performance must be measured on the frozen labels rather than inferred from face validity or agreement with rules.

## Update rule

A claim changes status only when a new versioned evidence artifact is added. Narrative enthusiasm, model complexity or a lower P value is not sufficient to upgrade evidence class.
