# Procedure Context Audit v0.1

**Phenotype dependency:** `configs/phenotypes_v0.3.yaml`  
**Dataset:** fixed 18-file local archive  
**Public output:** aggregate only

## 1. Purpose

Detailed operative-note availability is not equivalent to documentation of an operation for the target disease. A single admission may contain multiple operations involving different anatomical regions. Searching the entire operative-note export for generic procedure terms can therefore create cross-anatomy procedure leakage.

This audit was initiated after review of discordant procedure phenotypes identified examples in which a target-disease admission contained a detailed operation note for another condition. The correction was defined before physician or LLM evaluation and is not based on optimizing an inferential result.

## 2. Error mechanism

A naive admission-level extractor can make the following incorrect inference:

`target disease appears somewhere in admission + procedure term appears somewhere in operative note -> target-disease procedure present`

This fails when the target disease is documented in the admission header or diagnosis list but the detailed note describes a different operation.

Observed error modes included:

- a hallux-valgus admission with a detailed right-thumb/nail-bed soft-tissue operation;
- strict wrist-scaphoid admissions whose available detailed notes documented distal-radius, median-nerve or other non-scaphoid procedures.

Generic terms such as `切除`, `软组织`, `内固定` and `钢针` are especially vulnerable to this error because they are not anatomically specific.

## 3. Two distinct availability variables

The analysis now separates:

1. **detailed-note module available** - at least one detailed operative note is present for the admission;
2. **disease-concordant detailed note available** - at least one detailed note contains explicit target-disease/anatomical evidence in the procedure body.

The first remains a data-completeness variable. The second defines the denominator for target-disease procedure phenotyping and treatment-pattern analysis.

## 4. Fixed-data audit

| Domain | Strict phenotype admissions | Detailed-note module admissions | Disease-concordant note admissions |
|---|---:|---:|---:|
| Hallux valgus | 193 | 114 | **113** |
| Wrist scaphoid | 68 | 31 | **28** |
| First-CMC OA | 28 | 18 | **18** |

At the note level:

- hallux valgus: 168 detailed notes, 167 disease-concordant;
- wrist scaphoid: 43 detailed notes, 40 disease-concordant;
- first-CMC OA: 27 detailed notes, 27 disease-concordant.

## 5. Canonical procedure taxonomy

Procedure labels are now defined once in `src/ortho_pheno/procedure_rules.py`. All deterministic procedure summaries and future baseline predictions should reference this module rather than maintaining independent regular-expression dictionaries.

The canonical labels are:

### Hallux valgus

- osteotomy;
- Chevron;
- Akin;
- Scarf;
- fusion/arthrodesis;
- K-wire/steel-wire fixation;
- resection;
- soft-tissue procedures.

### Scaphoid

- internal fixation;
- bone grafting;
- reconstruction;
- fusion/arthrodesis;
- hardware removal;
- debridement.

### First-CMC OA

- trapeziectomy;
- tendon procedure;
- ligament procedure;
- arthroplasty;
- fusion/arthrodesis.

## 6. Effect on hallux-valgus analysis

The treatment-pattern denominator changes from 114 module-available admissions to **113 disease-concordant operative admissions**.

Current disease-concordant procedure frequencies include:

- osteotomy: 106/113 (93.8%);
- K-wire/steel-wire fixation: 103/113 (91.2%);
- soft-tissue procedure terms: 111/113 (98.2%);
- resection: 86/113 (76.1%);
- Chevron: 49/113 (43.4%);
- fusion: 12/113 (10.6%).

The exploratory bilateral-disease contrast remains directionally stable after the correction: bilateral mention is present in 69.4% of Chevron-positive versus 45.3% of Chevron-negative disease-concordant admissions (OR 2.74, 95% CI 1.25-5.98; Fisher p=0.013). This remains hypothesis-generating and requires physician validation.

## 7. Effect on scaphoid treatment analysis

The 68-case strict wrist-scaphoid cohort and the 23/45 chronic/nonunion grouping are unchanged. The correction affects only the procedure-analysis denominator.

Detailed-note module availability is 18/23 versus 13/45 for the chronic/nonunion and comparison groups, respectively. After disease-concordance filtering, the procedure-analysis denominators are **15 versus 13**.

Among disease-concordant notes:

- internal fixation is common in both groups;
- bone grafting is 8/15 in the established chronic/nonunion group versus a publicly suppressed `<5/13` comparison count;
- a composite graft/reconstruction/fusion marker is 9/15 versus `<5/13`.

Effect estimates involving suppressed small cells are not released publicly. These results describe treatment-pattern differences in established phenotypes and do not predict incident nonunion.

## 8. Annotation consequence

All module-available detailed notes remain valuable for validation because unrelated operations are clinically important hard negatives. The physician annotation layer should therefore retain all 114 hallux, 31 scaphoid and 18 first-CMC module-available admissions and add an explicit label:

`target_disease_procedure_present = yes / no / uncertain`

Only notes adjudicated as target-disease procedures should contribute to per-procedure clinical prevalence estimates. For algorithm evaluation, the relevance decision itself becomes a measurable extraction task.

## 9. Reproducibility and regression protection

- `src/ortho_pheno/procedure_rules.py` contains the canonical anatomy-aware rules;
- `src/ortho_pheno/procedure_context_audit.py` regenerates the aggregate context-aware outputs;
- `tests/test_procedure_rules.py` includes synthetic cross-anatomy leakage cases;
- historical full-note keyword summaries are retained as baselines rather than silently overwritten.

## 10. Conclusion

Procedure phenotyping from real-world EHRs requires both semantic procedure extraction and attribution of the procedure to the correct anatomical disease target. This audit converts a previously hidden source of label leakage into an explicit, testable component of the computational-phenotyping framework.
