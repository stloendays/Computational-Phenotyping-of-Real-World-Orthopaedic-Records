# Data Dictionary and Provenance Plan

## 1. Purpose

This document defines the patient-level analytical schema to be reconstructed from the existing orthopaedic source exports. It is intentionally independent of raw spreadsheet layout so that source-system duplication does not become analytical duplication.

## 2. Core identifiers

| Variable | Type | Role | Notes |
|---|---|---|---|
| episode_id | string | internal key | Derived locally from admission identifier; never committed with PHI |
| patient_key | string | optional internal key | Used only if repeated admissions can be linked reliably |
| disease_domain | categorical | cohort label | hallux_valgus / scaphoid / first_cmc_oa |
| source_period | categorical | documentation-era flag | Used for source-system sensitivity analyses |

## 3. Demographics

| Variable | Type | Definition |
|---|---|---|
| sex | categorical | Recorded sex |
| age_years | numeric | Age at admission |
| height_cm | numeric | Height when available |
| weight_kg | numeric | Weight when available |
| bmi | numeric | weight_kg / (height_m^2), only when both valid |

## 4. Temporal variables

| Variable | Type | Definition |
|---|---|---|
| admission_date | date | Admission date |
| surgery_date | date | First relevant operative date in episode |
| discharge_date | date | Discharge date |
| length_of_stay_days | numeric | discharge_date - admission_date |
| operative_record_available | boolean | Whether detailed operative text is available |

Dates are used only when source timestamps are valid. Missing dates are not imputed from text unless a validated extraction rule is prespecified.

## 5. Diagnostic phenotypes

### 5.1 Hallux valgus

| Variable | Type | Definition |
|---|---|---|
| hv_strict | boolean | Meets strict hallux-valgus phenotype |
| hv_bilateral | boolean/unknown | Bilateral disease documented |
| hv_angle_mentioned | boolean | Angle-like deformity measurement present in text |
| hv_angle_value_deg | numeric/unknown | Parsed degree value only after context validation |

### 5.2 Scaphoid

| Variable | Type | Definition |
|---|---|---|
| scaphoid_wrist_strict | boolean | Wrist-scaphoid phenotype after anatomical disambiguation |
| navicular_foot_excluded | boolean | Foot-navicular context present and wrist phenotype excluded |
| scaphoid_chronic_nonunion | boolean | Established chronic/nonunion phenotype |
| scaphoid_acute | boolean/unknown | Explicit acute/new fracture evidence |
| scaphoid_location | categorical/unknown | proximal / waist / distal when documented |

### 5.3 First CMC osteoarthritis

| Variable | Type | Definition |
|---|---|---|
| cmc1_strict | boolean | First-CMC-specific OA phenotype |
| generic_wrist_arthritis_only | boolean | Broad arthritis terminology without first-CMC support |
| competing_wrist_diagnosis | boolean | Alternative wrist-arthritis diagnosis identified |

## 6. Procedure phenotypes

All procedure variables are multi-label and may coexist.

### Hallux valgus

- osteotomy
- chevron
- akin
- scarf
- fusion
- k_wire
- resection
- soft_tissue

### Scaphoid

- fixation
- graft
- reconstruction
- fusion

### First CMC osteoarthritis

- trapeziectomy
- tendon_procedure
- ligament_procedure
- arthroplasty
- fusion

## 7. Derived treatment-complexity variables

A simple ordinal treatment-complexity construct may be evaluated for the scaphoid analysis, but it must be frozen before confirmatory testing.

Candidate hierarchy:

- Level 1: fixation only;
- Level 2: fixation + graft;
- Level 3: reconstruction-type procedure;
- Level 4: salvage/fusion.

This is an analytical abstraction and must not be presented as a validated clinical severity scale.

## 8. Laboratory variables

Laboratory data are retained primarily for baseline/availability description unless paired pre/post measurements are sufficiently complete.

Potential variables include:

- CBC-derived measures;
- coagulation measures;
- CRP;
- ESR;
- liver/renal function;
- electrolytes.

Documentation availability must be reported separately from numeric values. Sparse CRP/ESR measurements should not be treated as universally measured covariates.

## 9. Imaging-report variables

The fixed dataset may include imaging report text and examination identifiers. The project does not assume access to raw DICOM images.

Potential report-derived variables are permitted only when explicitly documented and validated through source-text review.

## 10. Provenance fields

Each automated phenotype should have local provenance fields:

- source_table;
- source_column;
- source_record_timestamp if available;
- extraction_method;
- rule_or_model_version;
- supporting_text_hash or non-reconstructable local reference;
- review_status.

Raw clinical text must not be committed to the public repository.

## 11. Missingness representation

Use explicit three-state or four-state representations where appropriate:

- positive;
- documented negative;
- not documented/unknown;
- structurally unavailable.

Do not collapse unknown into negative.
