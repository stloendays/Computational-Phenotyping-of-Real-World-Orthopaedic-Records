# Scaphoid Main-Paper Current Status v0.1

## Scientific question

Primary comparison:

**physician-confirmed established chronic/nonunion vs physician-confirmed acute/new fracture**

Primary outcome: **bone-graft augmentation**  
Key contrast: **internal fixation**  
Secondary mechanism: **physician-adjudicated wrist-related duration within established chronic/nonunion vs graft status**

## Complete

- fixed 88-record broad scaphoid candidate population;
- deterministic 68 wrist / 13 foot / 7 ambiguous audit retained as pre-validation evidence;
- two-stage physician Gold workflow avoiding verification bias;
- Stage-1 input frozen before annotation;
- separate Reviewer-1 / Reviewer-2 / adjudicated Gold architecture;
- duration vocabulary and Chinese duration-parser regression tests;
- analysis plan v0.3 and transparent analysis changelog;
- literature-gap audit constraining novelty claims;
- post-Gold statistical engine;
- private-exact/public-suppressed output separation;
- synthetic two-stage Gold and post-Gold analysis tests passing in CI.

## Not complete

- physician Stage-1 anatomy labels;
- Stage-1 adjudication and Gold freeze;
- Stage-2 state/duration/procedure review;
- final physician-adjudicated clinical effect estimates;
- final main Figures 1-3.

## Protocol correction made before Gold

An earlier plan contained a broad comparison plus an `acute-only` sensitivity analysis. Under the physician state vocabulary, every sufficiently classifiable non-chronic record is already `acute_or_new_fracture`, so those two groups would be identical.

The redundancy was identified before Stage-2 Gold and removed. The final primary comparison directly uses physician-confirmed acute/new fracture. The primary bone-graft outcome did not change.

## Current analysis entrypoint after Gold

`src/ortho_pheno/analyze_scaph_gold_v0_2.py`

It validates final Gold and produces:

- a private manuscript JSON with exact 2x2 tables, conditional OR/95% CI, Fisher P, baseline descriptors, component-count, duration, and leave-one-out analyses;
- a separately privacy-suppressed public aggregate CSV.

## Publication positioning

The study does not claim to discover that nonunion may require grafting or that chronicity matters. The defensible contribution is narrower:

- mechanical fixation as a common base;
- biological augmentation as the component that changes across presentation state;
- duration-related heterogeneity within established disease as an exploratory secondary observation.

With the fixed data, the realistic format is a focused exploratory retrospective study / brief report, contingent on physician Gold preserving a robust signal.
