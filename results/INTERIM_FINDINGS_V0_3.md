# Interim Aggregate Findings v0.3

**Supersedes:** `INTERIM_FINDINGS_V0_2.md` for current manuscript planning.  
**Phenotype dependency:** `configs/phenotypes_v0.3.yaml`  
**Procedure-context dependency:** `src/ortho_pheno/procedure_rules.py`

These results remain exploratory until physician reference-standard annotation is completed. The fixed local dataset is unchanged.

## 1. Admission-level cohort reconstruction

Raw diagnosis/demographics rows substantially overstate the analytical sample because a single admission can recur across diagnosis rows. The current admission-level deterministic cohorts remain:

- hallux valgus: **193 / 200** candidates;
- first-CMC OA: **28 / 79** candidates;
- high-specificity wrist scaphoid: **68 / 88** scaphoid-retrieval candidates.

For scaphoid anatomy, the 88 candidates are partitioned into **68 wrist scaphoid, 13 foot navicular and 7 ambiguous** episodes.

## 2. Scaphoid rule-version transition

The superseded heuristic selected 72 apparent wrist-scaphoid episodes. Under v0.3:

- 68 remain high-specificity wrist scaphoid;
- the four removed episodes are all classified as explicit foot navicular;
- no new wrist-scaphoid episodes were introduced relative to the previous heuristic.

The correction therefore removes anatomical contamination rather than expanding the cohort. Ambiguous records remain outside the deterministic primary comparison until physician adjudication.

## 3. Documentation architecture remains era-dependent

The supplied 2019-2022 exports preserve complaint/examination records but lack the detailed operative-note, examination/imaging and laboratory modules seen in other periods for the hallux-valgus and scaphoid datasets. For the v0.3 wrist-scaphoid cohort:

- 2015-2018: 15 episodes;
- 2019-2022: 21 episodes;
- 2023-2025: 32 episodes.

The 2023-2025 era remains the prespecified internally consistent sensitivity period for treatment-pattern comparisons.

## 4. New procedure-context finding: note availability is not treatment attribution

A detailed operative-note module can contain surgery for a different anatomical condition within the same admission. Full-note keyword extraction can therefore assign a procedure to the wrong study disease.

The fixed-data procedure-context audit gives:

| Domain | Detailed-note module admissions | Disease-concordant procedure-note admissions |
|---|---:|---:|
| Hallux valgus | 114 | **113** |
| Wrist scaphoid | 31 | **28** |
| First-CMC OA | 18 | **18** |

This creates two separate variables:

- **module availability**, retained as a documentation/data-quality measure;
- **target-disease procedure attribution**, required for clinical procedure prevalence and treatment-pattern analysis.

All module-available notes remain in the physician/algorithm validation set because unrelated procedures are clinically important hard negatives.

## 5. Hallux-valgus procedure patterns after disease-concordance filtering

The current clinical procedure-analysis denominator is **113**, rather than the 114 admissions with any detailed operative-note module.

Among disease-concordant operative admissions:

- osteotomy: **106/113 (93.8%)**;
- K-wire/steel-wire fixation: **103/113 (91.2%)**;
- soft-tissue procedure terms: **111/113 (98.2%)**;
- resection: **86/113 (76.1%)**;
- Chevron: **49/113 (43.4%)**;
- fusion: **12/113 (10.6%)**.

The most common multi-label combination is:

`k_wire + osteotomy + resection + soft_tissue` - **39/113 (34.5%)**.

The exploratory bilateral-disease contrast remains stable after removing the unrelated operation:

- Chevron positive: **34/49 (69.4%)**;
- Chevron negative: **29/64 (45.3%)**;
- OR **2.74**, 95% CI **1.25-5.98**;
- Fisher exact p **0.013**.

This association remains hypothesis-generating and cannot be interpreted as causal treatment selection before physician validation of both the baseline bilateral phenotype and procedure attribution.

## 6. Scaphoid treatment patterns after disease-concordance filtering

Within 68 high-specificity wrist-scaphoid episodes:

- established chronic/nonunion phenotype from non-operative clinical text: **23**;
- other wrist-scaphoid phenotype: **45**.

Detailed-note **module availability** is 18/23 versus 13/45. However, three module-available chronic/nonunion admissions contain only non-scaphoid detailed operations. The target-disease procedure-analysis denominators are therefore:

- established chronic/nonunion: **15** disease-concordant operative admissions;
- comparison: **13** disease-concordant operative admissions.

Among these disease-concordant notes:

- internal fixation: **14/15** versus **12/13**;
- bone grafting: **8/15** versus a public `<5/13` comparison count;
- composite bone-graft/reconstruction/fusion marker: **9/15** versus `<5/13`.

Public effect estimates are suppressed where they could disclose a cell smaller than five. The qualitative observation that grafting/complex reconstruction is more concentrated in the established chronic/nonunion group remains, but this is a treatment-pattern comparison and not evidence of predictors of incident nonunion.

## 7. First-CMC procedure attribution

All **18/18** strict first-CMC admissions with a detailed operative-note module also have target-disease-concordant operative documentation under the deterministic context rules. Current procedure frequencies include:

- trapeziectomy: **13/18 (72.2%)**;
- tendon procedure: **16/18 (88.9%)**;
- ligament procedure: **10/18 (55.6%)**;
- arthroplasty: **5/18 (27.8%)**;
- fusion: public count suppressed when below five.

The domain remains primarily a diagnostic/anatomical specificity benchmark rather than a predictive modelling cohort.

## 8. Methodological interpretation

Two distinct leakage modes have now been identified before model benchmarking:

1. **anatomical lexical leakage** - non-anatomical character occurrences such as `手术`/`手法` could spuriously support a wrist-scaphoid label;
2. **procedure attribution leakage** - a target-disease admission can contain a detailed operation for another anatomical condition, causing generic procedure terms to be assigned to the wrong disease.

Both are realistic failure modes of clinical NLP applied to heterogeneous EHR exports. They motivate explicit uncertainty, source-scope control and disease-concordant evidence requirements.

## 9. Physician reference standard

The physician validation set continues to include all module-available detailed operative-note admissions rather than only deterministic disease-concordant notes:

- hallux valgus: 114;
- wrist scaphoid: 31;
- first-CMC OA: 18.

Reviewers first adjudicate `target_disease_procedure_present = yes / no / uncertain`, followed by multi-label procedure components. This allows the relevance/attribution step itself to be evaluated rather than treated as hidden preprocessing.

## 10. Current scientific story

The current fixed-data study supports a stronger clinical-informatics narrative than a generic prediction exercise:

1. reconstruct admission-level records and eliminate pseudoreplication;
2. model anatomical uncertainty explicitly;
3. enforce source scope for disease-state definitions;
4. distinguish procedure-note availability from target-disease procedure attribution;
5. validate disease, state, relevance and procedure labels against a frozen physician reference standard;
6. compare deterministic, dictionary, LLM-assisted and hybrid extraction only after the reference standard is locked.

The next inferential milestone remains physician validation. Additional algorithmic complexity is secondary to establishing a defensible reference standard and quantifying these real-world EHR failure modes.
