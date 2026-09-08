# Claim-to-Evidence Matrix v0.2

**Supersedes:** `CLAIM_EVIDENCE_MATRIX_V0_1.md` for current manuscript planning.  
**Current dependencies:** phenotype v0.3, procedure-context audit v0.1, physician gold standard pending.

This matrix separates source-data facts, deterministic computational findings, exploratory clinical associations and blocked future claims. A claim can change status only when new versioned evidence is added.

| ID | Candidate manuscript claim | Current status | Current evidence | Validation dependency | Allowed wording now |
|---|---|---|---|---|---|
| C1 | Raw diagnosis rows cannot be treated as independent clinical episodes because repeated diagnosis coding causes severe row inflation. | Supported source-data fact | `source_duplication_audit.csv` | Code reproducibility only | State as a property of the supplied exports. |
| C2 | The supplied EHR exports exhibit a material calendar-era documentation discontinuity, particularly in 2019-2022. | Supported source-data fact | `era_module_coverage.csv`; `year_distribution.csv` | Code reproducibility only | State as a documentation/data-generation property, not a clinical trend. |
| C3 | Broad Chinese `舟骨` retrieval cannot be assumed to represent wrist scaphoid disease. | Strong deterministic evidence; physician confirmation pending | `scaphoid_anatomy_audit.csv` | Physician disease/anatomy adjudication | Report deterministic audit output; do not call it ground-truth prevalence. |
| C4 | Phenotype v0.3 partitions the 88 scaphoid candidates into 68 wrist scaphoid, 13 foot navicular and 7 ambiguous episodes. | Frozen deterministic output | `scaphoid_anatomy_audit.csv`; `phenotypes_v0.3.yaml` | Physician accuracy benchmark pending | Report as algorithmic cohort output. |
| C5 | The v0.3 scaphoid correction removed anatomical contamination rather than increasing sample size. | Supported rule-transition fact | `scaphoid_rule_version_transition.csv` | None beyond reproducibility | May state that all 68 current wrist episodes overlap the prior 72 and four removed records are v0.3 foot-navicular; zero new wrist episodes were added. |
| C6 | Character-level Chinese matching can create anatomy errors when non-anatomical words such as `手术` or `手法` are treated as hand context. | Supported failure-mode finding | `PHENOTYPE_CHANGELOG.md`; regression tests | Physician benchmark quantifies real-data performance | May describe as an observed failure mode of the superseded heuristic. |
| C7 | Operative-note module availability is not equivalent to documentation of surgery for the target disease. | Supported deterministic audit finding | `PROCEDURE_CONTEXT_AUDIT_V0_1.md`; `procedure_note_relevance_audit.csv` | Physician procedure-relevance adjudication validates accuracy | May report the deterministic module-vs-concordance discrepancy. |
| C8 | Full-note keyword procedure extraction can produce cross-anatomy procedure-attribution leakage. | Supported failure-mode finding; clinical frequency pending | `procedure_rules.py`; `test_procedure_rules.py`; procedure-context audit | Physician relevance benchmark | May describe as a discovered EHR NLP failure mode; final error rate awaits gold standard. |
| C9 | Current deterministic disease-concordant procedure denominators are 113 hallux, 28 scaphoid and 18 first-CMC admissions, versus module counts 114/31/18. | Frozen deterministic output | `procedure_note_relevance_audit.csv` | Physician relevance adjudication | Report as algorithm outputs, not true procedure counts. |
| C10 | Hallux-valgus operative treatment is dominated by osteotomy, fixation, soft-tissue and resection components. | Exploratory deterministic phenotype result | `procedure_phenotype_counts_concordant.csv`; `hallux_procedure_combinations_concordant.csv` | Physician relevance + component annotation | Report as deterministic disease-concordant text-phenotype frequencies, not validated prevalence. |
| C11 | Bilateral-disease mention is more frequent in Chevron-positive than Chevron-negative hallux episodes. | Exploratory association | `hallux_treatment_pattern_contrasts_concordant.csv` | Physician validation of bilateral phenotype, relevance and Chevron label; multiplicity-aware interpretation | Hypothesis-generating only; no causal treatment-selection language. |
| C12 | Established chronic/nonunion wrist-scaphoid phenotypes show more grafting/complex reconstruction than comparison phenotypes. | Exploratory association | `scaphoid_procedure_by_group_concordant.csv`; v0.3 interim findings | Physician anatomy/state/relevance/component adjudication | Describe as exploratory treatment-pattern signal. |
| C13 | The scaphoid comparison identifies predictors of future incident nonunion. | **Not supported** | Fixed records do not establish an acute baseline-to-incident-nonunion trajectory for all cases | Would require unavailable longitudinal outcome evidence | Prohibited claim. |
| C14 | The dataset supports long-term postoperative efficacy, recurrence or functional recovery conclusions. | **Not supported** | Long-term outcomes are not consistently available | Would require unavailable additional local data | Prohibited claim. |
| C15 | The deterministic baseline has been benchmarked against physician gold labels. | **Not yet completed** | Blinded prediction and hierarchical scoring infrastructure are implemented; gold annotation pending | Complete/freeze physician annotation | Do not publish performance numbers yet. |
| C16 | LLM-assisted extraction improves over deterministic rules. | **Not yet tested** | No frozen physician-gold comparison yet | Freeze gold, score deterministic baseline, then score LLM on identical rows/metrics | No improvement claim before benchmark. |
| C17 | A hybrid NLP system is superior and clinically reliable across three orthopaedic domains. | **Not supported yet** | Cross-domain infrastructure exists; no locked physician-performance comparison | Physician reference standard + prespecified uncertainty/error analysis | Future claim only if criteria are met. |
| C18 | Procedure attribution should be evaluated separately from component extraction. | Supported methodological design; empirical comparative performance pending | Annotation protocol v0.2; baseline benchmark plan; hierarchical evaluator | Physician gold standard for performance values | Can state as prespecified evaluation architecture. |
| C19 | Public aggregate artifacts can be reproduced without publishing patient-level clinical data. | Supported repository-design claim | safe-release code, privacy policy, aggregate outputs, `.gitignore` | Final publication privacy audit | State as a reproducibility/privacy design property. |

## Evidence classes

### Source-data claims available now

C1, C2 and the repository-design component of C19 concern the structure of the supplied exports rather than clinical truth labels.

### Deterministic computational findings awaiting physician accuracy estimates

C3-C10 describe frozen rule-system outputs or failure modes. They can be reported as computational audit findings, but clinical precision/recall/PPV must come from the physician reference standard.

### Exploratory clinical associations

C11-C12 remain hypothesis-generating. A low P value from deterministic labels cannot upgrade either claim before label validation and multiplicity-aware interpretation.

### Claims prohibited by the fixed-data boundary

C13-C14 cannot be rescued by model complexity. The necessary longitudinal outcomes are absent from the fixed dataset.

### AI comparison claims blocked by the gold-standard gate

C15-C17 cannot be upgraded until the physician reference standard is completed, frozen and applied identically to all extraction systems.

## Procedure evaluation freeze

Procedure-model performance must be reported at two levels:

1. target-disease procedure relevance/attribution;
2. procedure-component extraction.

Conditional component metrics and end-to-end metrics are both required. A system cannot be called superior if it improves component F1 by relying on an oracle relevance filter while worsening cross-anatomy attribution.

## Update rule

A claim changes status only when a new versioned evidence artifact is added. Model sophistication, narrative preference or a more favourable effect estimate is not sufficient to upgrade evidence class.
