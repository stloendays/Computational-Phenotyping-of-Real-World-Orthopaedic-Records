# Cohort Audit v0.2

**Phenotype dependency:** `configs/phenotypes_v0.3.yaml`  
**Dataset:** fixed 18-file local archive  
**Public output:** aggregate only

## 1. Purpose

This audit supersedes the v0.1 scaphoid anatomy count after a cross-pipeline consistency check exposed lexical false positives in the earlier wrist-scaphoid heuristic. Hallux-valgus and first-CMC cohort definitions are unchanged.

No new local clinical data were added.

## 2. Current deterministic cohorts

| Domain | Candidate admissions | Current strict phenotype | Additional anatomy classes |
|---|---:|---:|---|
| Hallux valgus | 200 | 193 | 7 non-strict candidates |
| Scaphoid retrieval | 88 | **68 wrist scaphoid** | **13 foot navicular; 7 ambiguous** |
| First-CMC OA retrieval | 79 | 28 | 51 non-strict candidates |

The primary unit remains the reconstructed admission episode.

## 3. Scaphoid anatomy correction

### Error mode discovered

The earlier anatomy heuristic allowed the character `手` to contribute hand/wrist context. In long clinical and operative text, ordinary words such as:

- `手术` (operation);
- `手法` (manual manoeuvre)

could therefore turn an explicit foot-navicular record into an apparent wrist-scaphoid record.

The annotation-packet generator independently disagreed with the cohort audit, triggering case-level review of the discordant set. This review demonstrated both false inclusion of foot-navicular records and under-recognition of valid constructions such as `左腕桡骨、舟骨骨折`.

### v0.3 resolution

Scaphoid anatomy is now a three-state deterministic phenotype:

1. `wrist_scaphoid` - high-specificity local wrist/hand-to-scaphoid evidence, waist/pole terminology, or generic scaphoid wording with explicit wrist context and no foot evidence;
2. `foot_navicular` - explicit foot/navicular evidence without strong wrist-scaphoid evidence;
3. `ambiguous` - insufficient anatomy evidence.

A genuine multi-site trauma record with explicit wrist-scaphoid and foot-navicular injuries may retain the wrist-scaphoid phenotype.

### Fixed candidate audit

Among 88 candidate admissions:

- wrist scaphoid: **68 (77.3%)**;
- foot navicular: **13 (14.8%)**;
- ambiguous: **7 (8.0%)**.

The seven ambiguous episodes remain in the physician disease/anatomy adjudication packet and are excluded from the primary wrist-scaphoid clinical comparison until reviewed.

## 4. Current scaphoid comparison groups

Within 68 deterministic high-specificity wrist-scaphoid episodes:

- established chronic/nonunion phenotype from non-operative clinical text: **23**;
- other wrist-scaphoid phenotype: **45**.

Operative text remains prohibited from assigning chronic/nonunion case status.

Detailed operative notes are available for:

- 18/23 established chronic/nonunion episodes;
- 13/45 comparison episodes;
- 31/68 strict wrist-scaphoid episodes overall.

## 5. Calendar-era audit

The data-generation discontinuity remains material:

| Era | Strict scaphoid episodes | Interpretation |
|---|---:|---|
| 2015-2018 | 15 | earlier source architecture; surgery-name/imaging/lab data available for many episodes |
| 2019-2022 | 21 | complaint/examination retained; detailed operation/imaging/lab modules absent in supplied exports |
| 2023-2025 | 32 | internally consistent modern documentation era |

The 2023-2025 sensitivity comparison therefore remains prespecified.

Within that era:

- established chronic/nonunion: 18;
- other wrist scaphoid: 14;
- detailed operative notes: 18 vs 13.

## 6. Treatment-phenotype robustness

The anatomy correction reduces the comparison-group denominator but does not reverse the principal treatment-pattern observation:

- internal fixation remains common in both groups;
- bone-grafting and broader complex-reconstruction markers remain concentrated in the established chronic/nonunion group;
- age and BMI distributions remain similar in the 2023-2025 sensitivity cohort.

Small-cell inferential statistics remain suppressed in the public release whenever they could reveal an exact count below 5.

## 7. Other domains

### Hallux valgus

The strict cohort remains 193 episodes. Detailed operative-note analysis remains n=114 and is unaffected by the scaphoid anatomy correction.

### First-CMC OA

The strict cohort remains 28 of 79 candidates. The domain continues to function as a high-specificity anatomical/diagnostic disambiguation benchmark.

## 8. Validation transition

The current deterministic audit now feeds a physician-reference-standard workflow:

- disease/anatomy adjudication: all 367 candidate episodes;
- scaphoid state adjudication: 68 strict wrist-scaphoid episodes;
- procedure adjudication: 163 detailed operative notes;
- approximately 20% deterministic stratified second review.

Private annotation files remain local. Only aggregate validation metrics will be released.

## 9. Audit conclusion

The main methodological result of v0.2 is that anatomy disambiguation cannot rely on character-level co-occurrence in long Chinese EHR text. Explicit uncertainty and source-aware local context are required. The v0.3 rules and regression tests freeze this correction before physician or LLM evaluation.
