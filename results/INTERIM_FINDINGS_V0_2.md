# Interim Aggregate Findings v0.2

**Supersedes:** `INTERIM_FINDINGS_V0_1.md` for current manuscript planning.  
**Phenotype dependency:** `configs/phenotypes_v0.3.yaml`

These results are exploratory until physician validation is completed. They are generated from the fixed local dataset using admission episode as the unit of analysis.

## 1. Cohort reconstruction is a substantive result

Raw diagnosis/demographics rows substantially overstate the analytical sample because one admission may appear repeatedly for multiple diagnoses. The observed row-to-admission inflation factors remain approximately:

- hallux valgus: **10.85**;
- first-CMC candidate retrieval: **12.40**;
- scaphoid candidate retrieval: **13.40**.

The current deterministic strict cohorts are:

- hallux valgus: **193 / 200** candidates;
- first-CMC OA: **28 / 79** candidates;
- wrist scaphoid: **68 / 88** candidates.

## 2. Chinese anatomy disambiguation requires explicit uncertainty

The scaphoid candidate audit now yields:

- **68 wrist-scaphoid episodes (77.3%)**;
- **13 explicit foot-navicular episodes (14.8%)**;
- **7 ambiguous episodes (8.0%)**.

The earlier 72-case wrist-scaphoid count is superseded. The discrepancy arose because character-level context allowed non-anatomical words such as `手术` and `手法` to contribute spurious "hand" evidence. v0.3 removes this shortcut and retains an explicit ambiguous state.

This error mode is itself relevant to the computational-phenotyping claim: Chinese medical text should not be reduced to isolated character co-occurrence when anatomical meaning depends on local lexical context.

## 3. Documentation architecture changes across eras

The 2019-2022 interval remains structurally different from both 2015-2018 and 2023-2025. In the supplied hallux-valgus and scaphoid exports, complaint/examination records remain present, whereas detailed operative-note, examination/imaging and laboratory modules are absent.

For the v0.3 strict scaphoid cohort:

- 2015-2018: 15 episodes;
- 2019-2022: 21 episodes;
- 2023-2025: 32 episodes.

Therefore all-year differences in module availability are treated as documentation-process artifacts rather than clinical outcomes. The 2023-2025 era is retained as the primary treatment-pattern sensitivity analysis.

## 4. Scaphoid established chronic/nonunion phenotype

Within the 68 high-specificity wrist-scaphoid episodes:

- **23** carry an established chronic/nonunion phenotype defined from diagnosis/complaint/examination text;
- **45** form the other wrist-scaphoid comparison group.

The chronic/nonunion count is unchanged from v0.2; the anatomy correction mainly removes false/uncertain records from the comparison group.

In the 2023-2025 sensitivity cohort:

- chronic/nonunion: **18**;
- comparison: **14**;
- age: 37.0 [26.8, 51.5] vs 37.5 [33.8, 44.8], Mann-Whitney p=0.924;
- BMI: 24.5 [23.1, 26.3] vs 25.1 [22.5, 28.7], p=0.802.

Among detailed operative notes in this era, internal fixation remains common in both groups. Bone grafting occurs in **9/18 (50.0%)** chronic/nonunion notes versus a publicly suppressed `<5/13` comparison count. A broader complex-reconstruction marker occurs in **10/18 (55.6%)** versus `<5/13`.

Because the comparison cells are smaller than 5, public OR/CI/exact-P statistics are suppressed. The available pattern supports a treatment-complexity association with an established chronic/nonunion phenotype; it does **not** establish predictors of incident nonunion.

## 5. Hallux-valgus procedure phenotyping remains stable

Among **114** strict hallux-valgus episodes with detailed operative notes:

- osteotomy: **106/114 (93.0%)**;
- K-wire/steel-wire fixation: **103/114 (90.4%)**;
- soft-tissue procedure terms: **111/114 (97.4%)**;
- resection terms: **87/114 (76.3%)**;
- Chevron: **49/114 (43.0%)**;
- fusion: **12/114 (10.5%)**.

The most common multi-label combination remains:

`k_wire + osteotomy + resection + soft_tissue` - **39/114 (34.2%)**.

In an exploratory treatment-pattern comparison, a preoperative bilateral-disease mention is more frequent in Chevron-positive than Chevron-negative episodes:

- Chevron positive: **34/49 (69.4%)**;
- Chevron negative: **29/65 (44.6%)**;
- OR **2.81**, 95% CI **1.29-6.14**;
- Fisher exact p **0.013**.

This result is hypothesis-generating and cannot be interpreted as causal treatment selection until the bilateral phenotype and procedure labels are physician-validated.

## 6. First-CMC OA remains the strongest hard-negative domain

Only **28 of 79** candidate episodes satisfy the current strict first-CMC phenotype. Among the 51 non-strict candidates, competing or nonspecific terminology frequently includes synovitis, generic wrist arthritis, rheumatoid wrist disease and gout-related wrist disease.

This domain is therefore retained as a stringent test of whether an extraction system overcalls broad wrist pathology as first-CMC OA.

## 7. Physician-reference-standard workload is now fixed

The local annotation generator produces:

- disease/anatomy primary review: **367 candidate episodes**;
- scaphoid-state primary review: **68 episodes**;
- procedure primary review: **163 detailed operative notes**;
- deterministic approximately 20% second-review subsets stratified by layer/domain.

The annotation records remain local-only and are never committed to the public repository.

## 8. Current interpretation

The strongest current scientific story is no longer a generic "machine-learning prediction" study. The fixed dataset supports a more defensible clinical-informatics study in which:

1. heterogeneous EHR exports are reconstructed at the admission level;
2. Chinese anatomical ambiguity is explicitly modelled rather than hidden;
3. disease/state/procedure phenotypes are validated against a frozen physician reference standard;
4. only then are real-world treatment-pattern associations analysed.

The next inferential milestone is therefore phenotype validation, not additional model complexity.
