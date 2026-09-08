# Main Manuscript Plan — Focused Scaphoid Study v0.2

## Central paper question

Among physician-confirmed wrist-scaphoid admissions with disease-concordant detailed operative documentation, is **established chronic/nonunion** associated with greater **bone-graft augmentation** than **physician-confirmed acute/new fracture**, while internal fixation remains common in both groups?

The paper is a focused exploratory retrospective clinical study. Computational text processing is a measurement method, not the scientific endpoint.

## Claim hierarchy

1. **Primary:** presentation state -> bone-graft augmentation.
2. **Key contrast:** internal fixation remains common in both groups.
3. **Secondary:** augmentation composite and major procedure-component burden.
4. **Exploratory secondary mechanism:** within established chronic/nonunion, documented wrist-related duration -> graft status.
5. **Measurement support:** physician reference-standard agreement and deterministic extraction accuracy, kept compact or supplementary.

## Main-text structure

### Introduction

1. Mechanical stability and biological environment are both relevant in scaphoid nonunion reconstruction.
2. Grafting is not uniformly required; treatment depends on lesion biology/structure and practice varies.
3. Existing literature mainly studies technique/outcome within established nonunion cohorts or graft-choice variation.
4. Current study asks which **operative component** changes across real-world presentation states: mechanical fixation or biological augmentation.
5. Secondary hypothesis asks whether documented chronicity differentiates graft use within established disease.

### Methods

1. fixed retrospective EHR source;
2. broad 88-record scaphoid retrieval;
3. two-stage physician-defined cohort to avoid verification bias;
4. non-operative state adjudication;
5. procedure relevance adjudication;
6. primary bone-graft outcome and fixation contrast;
7. physician duration variable;
8. sparse exact statistics;
9. leave-one-out robustness;
10. privacy and reference-standard freeze.

### Results

1. physician-defined cohort flow;
2. final acute/new and established chronic/nonunion operative denominators;
3. primary bone-graft 2x2 + OR/CI/Fisher;
4. internal-fixation contrast;
5. augmentation/component-count secondary result;
6. duration distribution by graft status within established chronic/nonunion;
7. robustness and inter-rater/measurement validation.

### Discussion

1. fixation as common mechanical base, augmentation as changing component;
2. relation to nonunion treatment algorithms and practice variation;
3. duration heterogeneity as a secondary observation, not a new graft indication;
4. no causal or outcome-efficacy interpretation;
5. limitations: small single-centre sample, EHR documentation, missing standardized imaging severity, data-derived hypothesis.

## Main figures

### Figure 1 — Physician-defined cohort flow

Final version after Gold:

`88 broad candidates -> physician anatomy -> wrist scaphoid -> physician state -> detailed note -> target-disease operation -> chronic/nonunion vs acute/new`.

No framework/agent/public-private schematic.

### Figure 2 — Operative composition by presentation state

Primary clinical figure.

Preferred display:

- internal-fixation and bone-graft percentages by state with explicit denominators;
- a compact point-range/forest representation of the bone-graft conditional OR and 95% CI when estimable.

The visual point is **fixation nearly invariant versus augmentation changing**.

### Figure 3 — Duration heterogeneity within established chronic/nonunion

Only if physician Gold preserves interpretable duration in both graft groups.

Preferred display:

- individual points on a log-duration axis;
- graft yes versus no;
- median/IQR overlay;
- no fitted cutoff or classifier.

### Figure 4 — Measurement/reference-standard support

Use in the main paper only if necessary; otherwise Supplementary.

Possible content:

- anatomy agreement/confusion;
- state agreement;
- procedure relevance/graft/fixation agreement.

Validation graphics must not dominate the clinical Results.

## Tables

### Table 1 — Final operative cohort characteristics

Columns:
- established chronic/nonunion;
- acute/new fracture.

Rows:
- N;
- age;
- sex;
- BMI;
- relevant documentation availability if useful.

### Table 2 — Operative components

Rows:
- internal fixation;
- bone graft;
- reconstruction;
- fusion;
- augmentation composite;
- component count.

Use exact denominators and the prespecified sparse-table statistics.

### Table 3 or Supplementary Table — Duration secondary analysis

- duration-available N;
- median/IQR days by graft status;
- Mann-Whitney U/P;
- injury-basis-only sensitivity if feasible.

## Manuscript novelty language

Do not claim that the study discovers grafting in nonunion, the relevance of chronicity, or real-world practice variation.

Preferred contribution language:

> Previous work has largely evaluated graft techniques and outcomes within established nonunion. This study instead decomposes documented surgery across wrist-scaphoid presentation states into a common mechanical fixation component and additional biological augmentation, with secondary assessment of duration-related heterogeneity within established disease.

See `LITERATURE_GAP_SCAPHOID_V0_1.md`.

## Current blocker

Final manuscript effect estimates and final Figures 1-3 are blocked only by the two-stage physician Gold workflow in Issue #3.

After Gold freeze, the current analysis entrypoint is:

`src/ortho_pheno/analyze_scaph_gold_v0_2.py`

It produces a private exact manuscript JSON and a separately suppressed public aggregate output.
