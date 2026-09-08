# Phenotype definition changelog

## v0.2 - cohort-audit freeze

The v0.1 audit exposed a circularity risk in the scaphoid analysis: if chronic/nonunion status is allowed to be assigned from the operative note, then operative-note availability and treatment components can become mechanically associated with case status.

v0.2 therefore changes the scaphoid chronic/nonunion source scope to **diagnosis, complaint and physical-examination text only**. Operative names and operative-note contents remain available as downstream treatment phenotypes but cannot assign scaphoid case status in the treatment-comparison analysis.

Consequences in the fixed dataset:

- strict wrist-scaphoid cohort remains 72 admission episodes;
- established chronic/nonunion phenotype changes from the preliminary all-text count of 24 to **23**;
- comparison group becomes **49**;
- 2023-2025 is prespecified as the internally consistent documentation-era sensitivity analysis because operative, examination and laboratory capture is markedly incomplete in 2019-2022.

No rule was changed to improve statistical significance. The revision is a leakage/circularity correction discovered during the preregistered cohort audit.

## v0.1

Initial preregistration draft defining strict disease terms, anatomical disambiguation and procedure labels.
