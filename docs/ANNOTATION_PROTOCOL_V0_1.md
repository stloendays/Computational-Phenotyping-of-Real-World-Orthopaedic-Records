# Physician Annotation Protocol v0.1

## 1. Purpose

This protocol defines the physician-reviewed reference standard for evaluating computational phenotypes derived from the **existing fixed local dataset**. Annotation does not require acquisition of any additional hospital data. Reviewers label only information already present in the supplied records.

The reference standard is frozen **before** LLM-assisted extraction is evaluated. Reviewers must not see deterministic-rule or model predictions during primary annotation.

## 2. Annotation units

The primary unit is the reconstructed admission episode, not an Excel row.

Three annotation layers are prespecified.

### Layer A - disease and anatomical adjudication

Review all candidate admission episodes:

| Domain | Candidate episodes | Primary labels |
|---|---:|---|
| Hallux valgus | 200 | hallux-valgus phenotype: yes / no / uncertain |
| Scaphoid retrieval | 88 | wrist scaphoid / foot navicular / other / uncertain |
| First-CMC retrieval | 79 | first-CMC OA: yes / no / uncertain; competing diagnosis category |

Total disease/anatomy adjudication workload: **367 admission episodes**.

Under deterministic phenotype v0.3, the 88 scaphoid candidates are provisionally partitioned into **68 high-specificity wrist-scaphoid, 13 explicit foot-navicular and 7 ambiguous episodes**. Reviewers remain blinded to these predictions. The seven deterministic ambiguous records are retained specifically for physician adjudication rather than being forced into either anatomy class.

### Layer B - scaphoid clinical-state adjudication

Review all **68 deterministic strict wrist-scaphoid episodes** using only non-operative clinical sources for the state label.

Primary state labels:

- acute/new fracture;
- established chronic fracture;
- established nonunion;
- chronic/nonunion not distinguishable from available text;
- insufficient documentation / uncertain.

For the primary chronic/nonunion benchmark, `established chronic fracture`, `established nonunion`, and `chronic/nonunion not distinguishable` may be collapsed into a prespecified binary established-chronic/nonunion phenotype. The source-specific multi-class labels remain retained for error analysis.

### Layer C - operative procedure adjudication

Review every available detailed operative note within the strict disease cohorts:

- hallux valgus: **114** notes;
- wrist scaphoid: **31** notes;
- first-CMC OA: **18** notes.

Total detailed operative-note workload: **163 notes**.

Procedure labels are multi-label; multiple components may be present in one operation.

## 3. Blinding and sequence

1. The annotation packet is generated from source records using the frozen local export script.
2. Direct identifiers are removed or masked before review whenever the clinical workflow permits.
3. Primary reviewers see source text only; they do not see rule outputs, model predictions, aggregate study results, or the other reviewer's labels.
4. Primary annotation is completed and locked.
5. A deterministic approximately 20% stratified subset is independently reviewed by a second clinician for inter-rater reliability.
6. Disagreements in the double-reviewed subset are adjudicated by consensus or a prespecified senior reviewer.
7. The locked reference standard is then used for every extraction-system comparison.

The gold-standard labels must not be changed in response to a model error unless the original annotation is shown to violate the written labeling rules. Any such correction requires a versioned annotation erratum.

## 4. Evidence-source rules

Each positive or uncertain label records the evidence source(s):

- diagnosis name/description;
- complaint;
- physical examination;
- operation name;
- detailed operative note.

### Anatomy evidence for scaphoid adjudication

The reviewer decides anatomy from the clinical meaning of the record, not from isolated characters. In particular, common words such as `手术` (operation) and `手法` (manual manoeuvre) do not constitute hand-anatomy evidence. An explicit phrase such as `左手舟骨` or a locally linked wrist-scaphoid description does constitute wrist evidence. Generic `舟骨` wording without sufficient anatomical support may be labelled uncertain.

### Source restriction for scaphoid chronic/nonunion state

The primary scaphoid state label must be determined from:

- diagnosis;
- complaint;
- physical examination.

**Operation names and operative-note contents cannot assign chronic/nonunion case status** in the treatment-comparison analysis. This prevents circularity because operative treatment is a downstream variable.

Operative text may still be annotated independently for fixation, grafting, reconstruction and fusion.

## 5. Hallux-valgus definitions

### Disease phenotype

`yes` requires a clinically explicit hallux-valgus/bunion phenotype or an unambiguous synonymous diagnosis in the source record.

`no` is used when the candidate retrieval is clearly explained by another condition without hallux-valgus evidence.

`uncertain` is used when documentation is insufficient or anatomically ambiguous.

### Baseline phenotype labels

Where explicitly documented:

- laterality: left / right / bilateral / unclear;
- bilateral-disease mention: yes / no / undocumented;
- deformity angle reported: numeric value + unit when explicit;
- pain: present / absent / undocumented;
- functional limitation: present / absent / undocumented.

`undocumented` is distinct from `absent`.

### Procedure labels

Annotate independently:

- osteotomy;
- Chevron osteotomy;
- Akin osteotomy;
- Scarf osteotomy;
- fusion/arthrodesis;
- K-wire/steel-wire fixation;
- resection;
- soft-tissue procedure.

A soft-tissue procedure includes explicit ligament, tendon, capsular or release components. Generic words such as "repair" without anatomical support are insufficient.

## 6. Scaphoid definitions

### Anatomical phenotype

`wrist_scaphoid` requires explicit wrist/hand scaphoid evidence, a locally linked wrist context, or an unambiguous scaphoid waist/pole description consistent with the wrist.

`foot_navicular` is used for explicit foot/navicular context.

`other` is used for a clearly different anatomical or diagnostic entity.

`uncertain` is used when the Chinese term `舟骨` cannot be safely assigned to wrist or foot from the available record.

A genuine multi-site trauma record may contain both foot-navicular and wrist-scaphoid injuries; in that situation the reviewer records the clinically explicit wrist-scaphoid phenotype rather than allowing the foot injury to erase it.

### Clinical state

`acute/new fracture` requires explicit acute/new/recent fracture wording or a clinical narrative consistent with an acute presentation without chronic/nonunion evidence.

`established chronic fracture` requires explicit chronic/old fracture wording without sufficient evidence to label nonunion specifically.

`established nonunion` requires explicit nonunion/nonhealing wording.

`chronic/nonunion not distinguishable` is used when the record clearly places the episode in the chronic/nonunion spectrum but does not support finer separation.

`insufficient/uncertain` is used when none of the above can be assigned reliably.

### Procedure labels

Annotate independently:

- internal fixation;
- bone grafting;
- reconstruction;
- fusion/arthrodesis;
- hardware removal, if present;
- debridement/lesion clearance, if present.

## 7. First-CMC OA definitions

### Strict first-CMC phenotype

`yes` requires explicit evidence that the degenerative/arthritic process involves the first carpometacarpal/trapeziometacarpal joint or an anatomically equivalent description involving the thumb metacarpal base/trapezium.

Broad terms such as `腕关节炎` or `腕掌关节炎` alone are **not sufficient**.

### Competing-diagnosis categories

Record any applicable category:

- radiocarpal arthritis;
- ulnocarpal arthritis;
- rheumatoid wrist disease;
- gout-related wrist disease;
- traumatic wrist arthritis;
- synovitis;
- other specified competing diagnosis;
- anatomically nonspecific wrist arthritis.

Categories may co-occur.

### Procedure labels

Annotate independently:

- trapeziectomy;
- tendon procedure;
- ligament procedure;
- arthroplasty;
- fusion/arthrodesis.

## 8. Missingness and negation

For every phenotype, the annotation system distinguishes:

- `present`;
- `absent` when explicitly negated or clearly excluded;
- `undocumented` when the source contains no usable statement;
- `uncertain` when the source is present but ambiguous.

Missing documentation must never be automatically converted to a negative phenotype.

Negated statements such as "未见骨不连" or "无明显疼痛" must not be treated as positive evidence.

## 9. Double-review subset

A second independent reviewer evaluates an approximately **20% deterministic stratified subset**. Selection is based on a fixed cryptographic hash of the local admission key and a frozen seed; the identifiers and selected texts remain in `annotations/private/` and are never committed.

The current deterministic workload is recorded in `data/aggregate/annotation_workload_summary.csv`.

Stratification ensures representation of:

- deterministic positives and negatives/ambiguous candidates;
- all three disease domains;
- scaphoid chronic/nonunion and comparison phenotypes;
- common hallux procedure labels;
- rare but clinically important procedure labels where feasible.

The public repository contains only the resulting aggregate reliability metrics, never the selected identifiers.

## 10. Inter-rater reliability

Report as appropriate:

- Cohen's kappa for binary/categorical labels;
- weighted kappa for ordered labels if used;
- positive and negative agreement when prevalence is highly imbalanced;
- per-label agreement for multi-label procedure extraction.

Confidence intervals are estimated by admission-level bootstrap when sample size permits.

## 11. Reference-standard metrics

After adjudication, evaluate deterministic, dictionary, LLM-assisted and hybrid systems on the **same locked reference standard**.

Binary/categorical phenotypes:

- sensitivity/recall;
- specificity;
- precision/positive predictive value;
- negative predictive value when meaningful;
- F1 score;
- exact accuracy;
- confusion matrix.

Multi-label procedure phenotypes:

- per-label precision, recall and F1;
- macro-F1;
- micro-F1;
- exact-set match;
- label-cardinality error.

## 12. Error taxonomy

Every extraction error is classified into one primary error type:

- anatomical confusion;
- negation failure;
- temporal/state confusion;
- broad-term overcalling;
- synonym/variant miss;
- procedure-component omission;
- unsupported semantic inference;
- source-scope violation;
- documentation insufficiency.

This taxonomy is used for error analysis, not to tune the frozen reference labels.

## 13. Privacy and data governance

- Annotation packets and adjudication files remain under `annotations/private/` or another approved local protected location.
- No admission key, pseudonymized row-level record, date, free-text note or reviewer-level clinical record is committed to the public repository.
- Public outputs contain only aggregate validation metrics and follow the repository small-cell suppression policy.
- The annotation process does not expand the source dataset; it structures information already present in the fixed archive.

## 14. Freeze condition

Version v0.1 is considered frozen when:

1. label definitions and allowed evidence sources are approved;
2. the private annotation packet has been generated;
3. reviewers begin primary annotation.

After freeze, semantic label definitions cannot be changed without a versioned protocol amendment.
