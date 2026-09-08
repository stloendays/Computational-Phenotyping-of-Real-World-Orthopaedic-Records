# Interim aggregate findings v0.1

These results are generated from the fixed local dataset using admission episode as the unit of analysis. They are exploratory until physician validation of text phenotypes is completed.

## 1. Raw-row inflation is substantial

The demographics/diagnosis exports contain many repeated rows per admission because multiple diagnoses are represented as separate records. The observed row-to-admission inflation factors are approximately:

- hallux valgus: **10.85 rows per admission**;
- first-CMC candidate retrieval: **12.40 rows per admission**;
- scaphoid candidate retrieval: **13.40 rows per admission**.

This confirms that row-level analysis would produce severe pseudoreplication. All subsequent analyses therefore use admission-level reconstruction.

## 2. Documentation architecture changes across calendar eras

The 2019-2022 interval behaves differently from both 2015-2018 and 2023-2025. For hallux valgus and scaphoid records in 2019-2022, complaint/examination records are present, whereas operative-note, imaging-exam and laboratory modules are absent from the supplied exports. In 2023-2025, these modules are again available for the large majority of strict episodes.

Therefore, apparent associations involving data availability across all years are not interpreted clinically. Procedure comparisons are accompanied by a 2023-2025 sensitivity analysis.

## 3. Scaphoid phenotype comparison

After the v0.2 leakage correction, the strict wrist-scaphoid cohort contains **72** admission episodes:

- **23** established chronic/nonunion phenotypes defined from diagnosis/complaint/examination text;
- **49** other strict wrist-scaphoid records.

The chronic/nonunion phenotype is strongly concentrated in the 2023-2025 documentation era (78.3%), whereas 44.9% of the comparison group falls in the 2019-2022 interval. This calendar imbalance explains much of the all-year difference in operative-note, imaging and laboratory availability.

Within the 2023-2025 sensitivity cohort, age and BMI distributions are similar between phenotype groups. Internal fixation is common in both groups. Bone-grafting and broader complex-reconstruction markers are more frequent in the chronic/nonunion phenotype group, but public inferential statistics are suppressed where small cells could be reconstructed. These findings should be interpreted as treatment-pattern differences associated with an established phenotype, not as predictors of incident nonunion.

## 4. Hallux valgus operative phenotypes

Among 114 strict hallux-valgus episodes with detailed operative notes:

- osteotomy is present in 93.0%;
- K-wire/steel-wire fixation in 90.4%;
- soft-tissue procedure terms in 97.4%;
- resection terms in 76.3%;
- Chevron in 43.0%;
- fusion in 10.5%.

The most common multi-label combination is `k_wire + osteotomy + resection + soft_tissue` (34.2%), followed by two Chevron-containing combinations.

In an exploratory treatment-pattern comparison, a preoperative bilateral-disease mention is more common in Chevron-positive than Chevron-negative operative records (69.4% vs 44.6%; OR 2.81, 95% CI 1.29-6.14, Fisher p=0.013). This is hypothesis-generating and requires phenotype validation before manuscript-level interpretation.

## 5. First-CMC OA is a high-value disambiguation test

The broad first-CMC retrieval contains 79 candidate admission episodes, but only 28 satisfy the current strict first-CMC phenotype. Among non-strict candidates, generic wrist arthritis, synovitis, rheumatoid/gout-related wrist disease and other competing diagnoses are common. This makes the domain useful for evaluating anatomical specificity and overcalling by broad keyword retrieval or LLM-based extraction.

## 6. Next locked steps

1. physician validation sample design for strict disease and procedure phenotypes;
2. synthetic unit tests for anatomy and source-scope rules;
3. frozen NLP baseline benchmark (regex/dictionary first);
4. only after baseline freeze, LLM-assisted extraction comparison;
5. manuscript figures generated solely from versioned aggregate outputs.
