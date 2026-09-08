# Validation Data Requirements

The validation scripts should operate only on de-identified, analysis-ready data. No protected health information should be committed to this repository.

## Minimum tables / fields

### 1. Patient index table
One row per analysis episode or patient, with:
- stable de-identified `patient_id`;
- `index_date` or index time;
- cohort inclusion/exclusion flags;
- outcome/phenotype label if applicable;
- site/service-line identifier where permitted;
- clinically relevant subgroup variables used in the manuscript.

### 2. Feature table
Feature rows keyed to `patient_id` (and episode/time where applicable), containing only information available at or before the prespecified index time for predictive analyses.

### 3. Phenotype-definition manifest
Versioned code lists, NLP rules, thresholds, temporal windows, and composite logic used to create the computational phenotype.

### 4. Split manifest
Frozen assignment of each patient to development, validation, temporal test, and/or external test partitions. A patient must never appear in more than one partition.

### 5. Analysis configuration
A machine-readable configuration specifying:
- primary endpoint / phenotype;
- primary metric(s);
- cohort variants;
- phenotype variants;
- subgroup definitions;
- resampling seeds;
- temporal cutoff;
- missing-data strategies;
- baseline models;
- ablations;
- negative controls;
- pass/fail tolerances where scientifically defensible.

## Repository policy

Raw clinical records, direct identifiers, free text containing PHI, dates not permitted by the governing data-use agreement, and secret credentials must not be committed. Store only code, schemas, synthetic examples, aggregate outputs, and approved de-identified derivatives.
