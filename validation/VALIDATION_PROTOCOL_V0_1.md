# Validation Protocol V0.1

## Purpose

This protocol defines the validation evidence required before making strong claims about computational phenotypes derived from real-world orthopaedic records. Criteria should be frozen before outcome inspection wherever possible.

## Core validation matrix

### V1. Cohort-definition robustness
Test whether headline findings persist under reasonable changes in inclusion/exclusion rules, look-back windows, encounter definitions, and duplicate-record handling.

**Pass criterion:** direction and substantive interpretation of the primary result remain unchanged across prespecified cohort variants.

### V2. Phenotype-definition robustness
Perturb code lists, NLP rules, thresholds, temporal windows, and composite-phenotype logic within clinically defensible ranges.

**Pass criterion:** phenotype prevalence and primary associations/predictions remain within prespecified tolerance; no single arbitrary rule drives the conclusion.

### V3. Patient-level separation and leakage audit
Ensure all records from a patient remain in one split. Audit features for information recorded after the prediction/index time, outcome-derived variables, proxy labels, and duplicated notes/events.

**Pass criterion:** zero identified post-index leakage variables in the final feature set; patient IDs do not cross train/validation/test partitions.

### V4. Internal resampling stability
Repeat the analysis across bootstrap or repeated cross-validation splits, depending on the study design.

**Report:** point estimate, 95% CI, between-split variability, and failure frequency.

### V5. Temporal validation
Train/develop on an earlier period and validate on a later period to test resilience to coding, practice, population, and workflow drift.

**Pass criterion:** primary conclusion is retained; degradation is quantified rather than hidden.

### V6. Site/service-line validation where available
Validate across hospitals, clinics, surgeons, or service lines when provenance permits.

**Pass criterion:** direction of the primary conclusion is not isolated to one site/provider stratum. If heterogeneity exists, report it explicitly.

### V7. Missingness and documentation-process sensitivity
Characterize missingness by variable, time, site, and patient subgroup. Compare complete-case, missing-indicator, and clinically appropriate imputation strategies where relevant.

**Pass criterion:** primary finding is not created by one missing-data treatment; documentation intensity is evaluated as a potential confounder/proxy.

### V8. Subgroup stability
Evaluate prespecified clinically relevant subgroups (for example age bands, sex, procedure class, diagnosis group, emergency/elective status, and site where available).

**Report:** subgroup effect/performance estimates with uncertainty. Avoid declaring equivalence from non-significance alone.

### V9. Calibration and decision utility (prediction studies only)
If the phenotype supports prediction, report discrimination plus calibration and clinically interpretable decision metrics.

**Minimum:** calibration intercept/slope or calibration curve; Brier score or equivalent; threshold-based PPV/NPV/sensitivity/specificity where clinically relevant; decision-curve analysis if a decision threshold is claimed.

### V10. Baseline comparison
Compare against simple, defensible baselines: prevalence/majority, logistic/linear model as applicable, code-count/rule-based phenotype, or an established clinical score where relevant.

**Pass criterion:** any claimed gain is quantified with uncertainty and not limited to one favorable metric.

### V11. Ablation
Remove major information sources or workflow components one at a time (e.g. structured codes, medications, procedures, notes, temporal aggregation, learned representation).

**Purpose:** identify which components carry the result and whether complexity is justified.

### V12. Negative controls
Use at least one negative-control exposure/outcome/feature family when scientifically defensible, or an intentionally unrelated label/permutation test for purely computational components.

**Pass criterion:** the pipeline does not manufacture a comparable signal under the negative control.

### V13. Label/annotation validation
If labels are manually adjudicated or algorithmically constructed, quantify agreement or audit against an independent sample.

**Minimum:** blinded review where possible; agreement/confusion matrix; adjudication procedure; sample size and selection process.

### V14. Sensitivity to analytic choices
Re-run headline analyses across prespecified alternatives for thresholding, regularization, class weighting, feature scaling, time aggregation, and statistical model specification.

**Pass criterion:** substantive conclusion is not dependent on one narrow hyperparameter or analytical choice.

### V15. Outlier and influence analysis
Identify extreme-utilization patients, unusually long records, high encounter counts, rare codes, and influential observations.

**Pass criterion:** removing or winsorizing prespecified extremes does not qualitatively reverse the primary conclusion, unless that dependence is itself the finding.

### V16. Reproducibility
Pin environment, configuration, random seeds, data dictionary version, code-list version, and analysis commit.

**Target:** a clean run can regenerate the manuscript tables/figures from the permitted analysis inputs.

## Evidence tiers

### Tier A — mandatory before submission
V1, V2, V3, V4, V5, V7, V8, V10, V12, V14, V16.

### Tier B — mandatory when applicable
V6, V9, V11, V13, V15.

### Tier C — strong external validation
Independent health system, independent annotation set, or prospective/locked future-time cohort.

## Claim-to-validation rule

Every headline manuscript claim must be linked to at least one direct validation test. Generalization claims require validation outside the development distribution. Clinical-utility claims require decision-level evidence, not discrimination alone.

## Status convention

- `NOT_STARTED`: protocol defined, analysis absent.
- `RUNNING`: frozen analysis running.
- `PASS`: prespecified criterion met.
- `QUALIFIED`: result survives with an important caveat/heterogeneity.
- `FAIL`: prespecified criterion not met.
- `NA`: scientifically not applicable, with justification.
