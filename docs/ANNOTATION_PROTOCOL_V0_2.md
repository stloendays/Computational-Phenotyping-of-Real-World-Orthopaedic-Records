# Physician Annotation Protocol v0.2

**Supersedes:** `ANNOTATION_PROTOCOL_V0_1.md` for current validation work.  
**Phenotype dependency:** `configs/phenotypes_v0.3.yaml`  
**Annotation schema:** `configs/annotation_schema_v0.1.yaml`

## 1. Purpose

This protocol defines the physician reference standard for evaluating computational phenotypes from the existing fixed local dataset. No additional hospital data are required or assumed.

The reference standard must be completed and frozen **before** LLM-assisted extraction results are inspected. Reviewers do not see deterministic-rule predictions, model predictions, aggregate result tables or the other reviewer's labels during primary review.

## 2. Unit of annotation

The analytical and annotation unit is the reconstructed **admission episode**, not an Excel row.

The protocol contains three main layers.

### Layer A - disease/anatomy adjudication

Review all candidate episodes:

| Domain | Candidate episodes | Primary label |
|---|---:|---|
| Hallux valgus | 200 | yes / no / uncertain |
| Scaphoid retrieval | 88 | wrist scaphoid / foot navicular / other / uncertain |
| First-CMC retrieval | 79 | first-CMC OA yes / no / uncertain + competing diagnosis |

Total: **367 admission episodes**.

The current deterministic scaphoid v0.3 partition is 68 wrist scaphoid, 13 foot navicular and 7 ambiguous. Reviewers remain blinded to this partition.

### Layer B - scaphoid state adjudication

Review all **68 deterministic high-specificity wrist-scaphoid episodes** using diagnosis, complaint and physical-examination text only for the state label.

Allowed labels:

- acute/new fracture;
- established chronic fracture;
- established nonunion;
- chronic/nonunion not distinguishable;
- insufficient/uncertain.

For the prespecified binary comparison, the three established chronic/nonunion-spectrum labels may be collapsed after adjudication. Operative text cannot assign this state because operative treatment is analysed downstream.

### Layer C - procedure attribution and procedure-component adjudication

Review every strict-cohort admission with a detailed operative-note module:

- hallux valgus: **114**;
- wrist scaphoid: **31**;
- first-CMC OA: **18**.

Total module-available procedure-review workload: **163 admission episodes**.

Procedure annotation is explicitly **hierarchical**.

#### Stage C1 - target-disease procedure attribution

For each admission, assign:

`target_disease_procedure_present = yes / no / uncertain`

This asks whether the detailed operative documentation actually describes treatment of the study disease/anatomical target. A target disease appearing only in the diagnosis/header does not establish that the detailed operation treated that disease.

Current deterministic context rules identify 113 hallux, 28 scaphoid and 18 first-CMC admissions as disease-concordant. Reviewers remain blinded to these predictions.

#### Stage C2 - procedure components

If Stage C1 is `yes`, annotate the target-disease procedure components. If Stage C1 is `no`, target-disease procedure labels should be empty. If relevance is `uncertain`, label only components that can be attributed with defensible clinical evidence and preserve uncertainty in the reviewer comment.

Unrelated operations are deliberately retained in the validation set as hard negatives.

## 3. Blinding and review sequence

1. Generate the private annotation packet from the fixed source archive.
2. Remove/mask direct identifiers in the review packet.
3. Primary reviewer labels source text without seeing rule/model outputs.
4. Lock primary annotations.
5. A deterministic approximately 20% stratified subset is independently reviewed by a second clinician.
6. Resolve disagreements by consensus or a prespecified senior reviewer.
7. Freeze the adjudicated reference standard.
8. Only then evaluate deterministic, dictionary, LLM-assisted and hybrid systems on the same labels.

A gold label may be corrected after freeze only if it demonstrably violates the written annotation rules. Corrections require a versioned annotation erratum and must not be driven by model errors.

## 4. General evidence and missingness rules

Possible evidence sources are:

- diagnosis name/description;
- complaint;
- physical examination;
- operation name;
- detailed operative note.

For every phenotype distinguish:

- `present`;
- `absent` when explicitly negated or clinically excluded;
- `undocumented` when there is no usable statement;
- `uncertain` when evidence exists but is insufficient or conflicting.

Undocumented is not equivalent to negative.

Negated statements such as `未见骨不连` or `无明显疼痛` must not be converted into positive evidence.

## 5. Scaphoid anatomy rules

`wrist_scaphoid` requires explicit wrist/hand-scaphoid evidence, a locally linked wrist context, or an unambiguous scaphoid waist/pole description consistent with the wrist.

`foot_navicular` requires explicit foot/navicular context.

`other` is used for a clearly different entity.

`uncertain` is used when generic `舟骨` wording cannot be assigned safely.

Clinical meaning must be assessed from lexical/local context rather than isolated Chinese characters. In particular, `手` inside `手术` or `手法` is not hand anatomy.

A true multi-site trauma episode can contain both a wrist scaphoid injury and a foot-navicular injury. Explicit evidence of one site must not erase explicit evidence of another site.

## 6. Scaphoid state rules

The primary state assignment uses only non-operative clinical sources.

`acute/new fracture` requires explicit acute/new/recent wording or a clearly acute narrative without chronic/nonunion evidence.

`established chronic fracture` requires explicit old/chronic fracture wording without sufficient evidence for specific nonunion.

`established nonunion` requires explicit nonunion/nonhealing wording.

`chronic/nonunion not distinguishable` is used when the record clearly lies in the chronic/nonunion spectrum but does not permit finer separation.

`insufficient/uncertain` is used when no state can be assigned reliably.

Operation name/note is prohibited from assigning this state in the treatment-comparison analysis.

## 7. Procedure-attribution rules

The reviewer must decide whether the operation belongs to the target disease **before** assigning procedure components.

Examples of attribution errors to avoid:

- a hallux-valgus admission whose detailed operation is for a hand/nail-bed lesion;
- a wrist-scaphoid admission whose detailed note describes only distal-radius fixation;
- a generic term such as `内固定` or `切除` appearing in an operation for a different anatomical site.

Use the operation name and procedure-body narrative as the primary attribution evidence. The admission diagnosis list may provide context but cannot by itself make an unrelated operation disease-concordant.

If several operations are documented in the same admission, annotate target-disease components from the relevant operation(s) only.

## 8. Hallux-valgus labels

### Disease/baseline

Where documented, annotate:

- laterality: left / right / bilateral / unclear / undocumented;
- bilateral-disease mention: present / absent / undocumented / uncertain;
- explicit deformity angle, numeric degrees when present;
- pain;
- functional limitation.

### Procedure components

- osteotomy;
- Chevron;
- Akin;
- Scarf;
- fusion/arthrodesis;
- K-wire/steel-wire fixation;
- resection;
- soft-tissue procedure.

A soft-tissue procedure requires explicit tendon, ligament, capsular or release content. Generic unrelated soft-tissue wording is insufficient.

## 9. Scaphoid procedure components

- internal fixation;
- bone grafting;
- reconstruction;
- fusion/arthrodesis;
- hardware removal;
- debridement/lesion clearance.

Procedure components must be attributable to scaphoid treatment, not merely present elsewhere in the admission.

## 10. First-CMC OA labels

### Disease/anatomy

A positive first-CMC phenotype requires explicit evidence involving the first carpometacarpal/trapeziometacarpal joint or an anatomically equivalent thumb-base/trapezium description. Broad `腕关节炎` or `腕掌关节炎` alone is insufficient.

Competing categories may include:

- radiocarpal arthritis;
- ulnocarpal arthritis;
- rheumatoid wrist disease;
- gout-related wrist disease;
- traumatic wrist arthritis;
- synovitis;
- nonspecific wrist arthritis;
- other specified competing diagnosis.

### Procedure components

- trapeziectomy;
- tendon procedure;
- ligament procedure;
- arthroplasty;
- fusion/arthrodesis.

## 11. Double review

Approximately 20% of each layer/domain is selected by a fixed cryptographic hash using the frozen seed `ORTHOPHENO-VAL-2026-09-v0.1`.

Current planned second-review workloads are recorded in `data/aggregate/annotation_workload_summary.csv`.

The second-review subset must represent, as feasible:

- deterministic positive/negative/ambiguous disease phenotypes;
- all three domains;
- scaphoid chronic/nonunion and comparison states;
- target-disease procedure-positive and procedure-negative records;
- common and clinically important procedure components.

## 12. Reliability metrics

Report as appropriate:

- Cohen's kappa for categorical labels;
- positive/negative agreement for highly imbalanced binary tasks;
- attribution agreement for `target_disease_procedure_present`;
- per-label agreement for multi-label procedure components.

Admission-level bootstrap confidence intervals are used when sample size permits.

## 13. Algorithm evaluation

All systems are evaluated on the same locked reference standard.

### Disease/anatomy and state

- sensitivity/recall;
- specificity;
- precision;
- F1;
- exact accuracy;
- confusion matrix.

### Procedure relevance

Evaluate `target_disease_procedure_present` separately before component extraction. This quantifies cross-anatomy attribution errors.

### Procedure components

Among adjudicated target-disease procedure records, report:

- per-label precision/recall/F1;
- macro-F1;
- micro-F1;
- exact-set match;
- label-cardinality error.

Also report an end-to-end result in which relevance and component extraction must both be correct.

## 14. Privacy and release

Annotation rows contain pseudonymous study IDs and protected clinical text and remain under `annotations/private/` only. They are never committed to the public repository.

Only aggregate validation metrics are released. Public cells smaller than five follow the repository small-cell suppression policy.

## 15. Freeze condition

The physician reference standard is considered frozen when:

- primary review is complete;
- prespecified second review is complete;
- adjudication is complete;
- missing/uncertain states have been resolved according to this protocol;
- a version/hash of the local gold files is recorded without releasing the files themselves.

LLM-assisted comparison begins only after this freeze condition is satisfied.
