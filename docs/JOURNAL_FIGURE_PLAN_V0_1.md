# Journal Figure Plan v0.1

**Purpose:** replace repository/presentation-style visuals with evidence-centered manuscript figures.

## Design principle

Main figures must communicate scientific evidence, denominators, error structure, uncertainty and validated clinical findings. Workflow/project-management graphics are secondary and should not dominate the main text.

Avoid in main figures:

- large rounded workflow boxes;
- promotional labels such as `PUBLIC/PRIVATE ZONE`;
- repository/process branding;
- claims such as `validation-first` as a visual headline;
- long explanatory sentences inside panels;
- decorative arrows without quantitative content.

Prefer:

- white background;
- black/grey journal palette;
- panel labels A-D;
- bar/point/forest/flow plots with explicit denominators;
- confidence intervals where inferential estimates are shown;
- concise axis labels and legends;
- methodological schematics only when they explain an analysis that cannot be shown quantitatively.

## Revised main-figure hierarchy

### Figure 1. Study cohort derivation and analytical sample

**Role:** establish who entered each analysis.

Panel A — source cohort counts by disease domain.

Panel B — candidate to deterministic strict phenotype:
- hallux valgus: 200 -> 193;
- first-CMC OA: 79 -> 28;
- scaphoid retrieval: 88 -> 68 wrist scaphoid, with 13 foot navicular and 7 ambiguous.

Panel C — scaphoid rule transition:
- previous wrist selection: 72;
- retained as wrist scaphoid under v0.3: 68;
- removed as explicit foot navicular: 4;
- new wrist additions: 0.

Panel D — analysis denominators for downstream procedure and state analyses.

**No large workflow schematic in the main panel.**

### Figure 2. Data-quality distortions corrected during phenotyping

**Role:** demonstrate why naive spreadsheet analysis is invalid.

Panel A — diagnosis-row inflation by disease (rows/admission).

Panel B — calendar-era module coverage, preferably as a compact heat map or dot matrix showing the 2019-2022 documentation discontinuity.

Panel C — broad retrieval versus strict phenotype yield across domains.

Panel D — optional first-CMC competing-diagnosis composition or scaphoid ambiguous fraction.

This figure should be quantitative rather than conceptual.

### Figure 3. Procedure-attribution error in operative records

**Role:** demonstrate the second major EHR error mode.

Panel A — module-available versus disease-concordant operative admissions:
- hallux valgus: 114 vs 113;
- wrist scaphoid: 31 vs 28;
- first-CMC OA: 18 vs 18.

Panel B — proportion of module-available notes judged disease-concordant.

Panel C — after physician gold is available, confusion matrix or false-attribution rate for deterministic / LLM / hybrid systems.

A minimal one-line schematic may be used only to define `module available -> target-disease relevance -> procedure components`; the quantitative panel is primary.

### Figure 4. Physician-reference validation benchmark

**Blocked until physician gold is frozen.**

Panel A — disease/anatomy macro-F1 by system and domain.

Panel B — scaphoid-state sensitivity/specificity or F1 with 95% CI.

Panel C — procedure-relevance performance.

Panel D — conditional versus end-to-end multi-label procedure performance.

Show uncertainty and identical evaluation denominators.

### Figure 5. Hallux-valgus clinical and operative phenotype

**Final version blocked until physician validation.**

Panel A — validated procedure-component prevalence.

Panel B — common procedure combinations/co-occurrence.

Panel C — bilateral phenotype by Chevron status.

Panel D — effect estimate (odds ratio with 95% CI) in a compact forest/point-range format.

The panel should foreground the clinical association, not the NLP pipeline.

### Figure 6. Scaphoid phenotype and treatment pattern

**Final version blocked until physician validation.**

Panel A — established chronic/nonunion versus comparison group characteristics.

Panel B — disease-concordant procedure components.

Panel C — graft/reconstruction/fusion composite by phenotype group.

Panel D — 2023-2025 sensitivity analysis.

Maintain explicit wording that this is an established-phenotype treatment-pattern comparison, not incident-nonunion prediction.

## Supplementary / repository-only figures

The current workflow-heavy graphics should be retained for reproducibility/documentation but removed from the main-paper figure sequence:

- `figures/pre_gold/Figure1_validation_first_framework.svg` -> Supplementary schematic / repository overview;
- the current Figure 2 and Figure 3 may be reused only after being reformatted to the journal plan above.

## Table strategy

### Table 1
Baseline cohort characteristics and source availability.

### Table 2
Physician-reference validation metrics.

### Table 3
Hallux-valgus validated clinical/procedure phenotype.

### Table 4
Scaphoid established-phenotype comparison.

Tables should carry exact denominators, N (%), median (IQR), and inferential estimates only where prespecified.

## Visual style

- white background;
- black, dark grey and light grey only unless a journal-specific colour scheme is later required;
- no gradients, shadows or decorative icons;
- no figure title inside the artwork unless the target journal requires it;
- panel letters in upper-left corners;
- 7-9 pt final-print text size after scaling;
- confidence intervals shown as line ranges rather than text when possible;
- legends outside data regions;
- minimal explanatory prose inside the plot.

## Manuscript rule

A main figure must answer a scientific question. If a panel mainly explains repository architecture, validation governance or file handling, it belongs in Methods, Supplementary Information or the repository README rather than the main Results figures.
