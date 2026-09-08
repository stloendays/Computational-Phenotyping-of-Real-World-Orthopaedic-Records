# Data-Driven Question Selection v0.1

**Purpose:** document why the primary manuscript question was selected from the fixed dataset before physician-reference scoring.

This project is explicitly problem-first. Computational phenotyping is retained only as a measurement tool required to recover clinical variables from the supplied records.

## Candidate questions observed in the fixed data

### Candidate A — Scaphoid chronic/nonunion and surgical augmentation

Observed structure:

- high-specificity wrist-scaphoid cohort: 68 admissions;
- established chronic/nonunion phenotype: 23;
- comparison phenotype: 45;
- disease-concordant detailed operative sample: 28, all from 2023-2025;
- internal fixation is common in both operative groups;
- bone-graft augmentation is concentrated in the established chronic/nonunion group.

Strengths:

- direct clinical question;
- exposure can be defined without operative-text leakage;
- treatment components are available in detailed operative records;
- the contrast between stable fixation use and increased biologic augmentation is clinically interpretable;
- contemporary literature supports genuine variation in graft/reconstructive strategy for scaphoid nonunion.

Limitations:

- small operative sample;
- no postoperative union outcome;
- no independent historical detailed-note replication;
- association is exploratory because the same fixed dataset generated the question.

### Candidate B — Hallux valgus baseline phenotype and Chevron selection

Exploratory screening identified associations between documented forefoot symptoms and Chevron use, including metatarsalgia and bilateral-disease mentions.

Strengths:

- larger operative sample;
- sufficient frequency for simple multivariable modelling.

Limitations:

- standardized radiographic severity is unavailable for most patients;
- procedure selection is strongly confounded by deformity geometry, surgeon preference and other unmeasured indications;
- several observed associations may reflect familiar operative indications rather than a distinct scientific finding.

### Candidate C — Hallux valgus arthritis phenotype and fusion

Arthritis/limited-motion terms are enriched among fusion cases.

Strengths:

- clinically coherent positive-control signal.

Limitations:

- the association is close to an expected indication for first-MTP fusion and therefore has limited novelty as a primary paper question.

### Candidate D — Cohort misclassification from broad diagnostic retrieval

The fixed data show substantial variation in broad-to-strict phenotype yield across disease domains, particularly for first-CMC OA and scaphoid anatomy.

Strengths:

- important clinical-informatics problem;
- directly measurable in the current exports;
- likely to affect observational inference.

Limitations:

- shifts the paper back toward a methods/informatics emphasis;
- user intent for the main manuscript is a disease-focused scientific problem rather than a generic phenotyping framework.

## Selected primary question

**Candidate A is selected as the main manuscript direction.**

The paper will ask whether established chronic/nonunion wrist-scaphoid disease is associated with a treatment-composition shift toward bone-graft augmentation while internal fixation remains common in both groups.

Selection is based on:

1. clinical interpretability;
2. compatibility with the fixed data actually available;
3. a clear exposure/outcome separation;
4. an observable treatment-composition pattern that does not require inventing long-term outcomes;
5. a lower risk of turning the manuscript into a generic AI/framework paper.

The choice is **not** justified by the smallest exploratory P value. Hallux-valgus screening produced smaller P values for some associations, but those signals were not selected because statistical significance alone is insufficient to define a scientific question.

## Consequence for the manuscript

Primary paper:

> **Established chronic/nonunion scaphoid phenotype and bone-graft augmentation in real-world surgical treatment.**

Computational work is limited to measuring:

- wrist-scaphoid anatomy;
- chronic/nonunion state;
- target-disease operative relevance;
- fixation and graft components.

Hallux valgus and first-CMC OA remain secondary/supplementary analyses unless the primary scaphoid signal fails physician adjudication.
