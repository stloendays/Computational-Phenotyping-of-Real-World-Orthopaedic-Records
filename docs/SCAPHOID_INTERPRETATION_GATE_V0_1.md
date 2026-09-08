# Scaphoid Post-Gold Interpretation Gate v0.1

**Frozen before Stage-2 physician Gold completion.**

This document prevents post-hoc endpoint switching or significance-based story rescue in the small fixed operative sample.

## 1. Primary result is always reported

The primary result is:

**physician-confirmed established chronic/nonunion vs physician-confirmed acute/new fracture -> bone-graft augmentation**.

After Gold freeze, the exact 2x2 table, conditional odds ratio, 95% confidence interval, and two-sided Fisher exact P value are reported regardless of statistical significance.

The paper will not replace this result with:

- augmentation composite;
- component count;
- duration;
- an LLM-derived label;
- another subgroup;
- a locally optimized threshold.

## 2. Evidence is judged by more than a P-value

Because the final acute/new operative denominator may be small, interpretation considers:

1. direction and magnitude of the conditional odds ratio;
2. exact/sparse confidence interval width;
3. Fisher exact P value;
4. leave-one-out stability of the direction;
5. whether deterministic and physician-adjudicated analyses are directionally consistent;
6. whether the secondary duration result is directionally coherent, without requiring it to be significant.

## 3. Interpretation classes

### A. Supportive exploratory evidence

Appropriate when:

- the physician-adjudicated primary effect is clearly in the hypothesized direction (OR > 1 or an appropriate infinite estimate from a zero cell);
- leave-one-out analyses do not reverse the direction;
- the result is not created solely by reclassifying one ambiguous record;
- uncertainty is reported transparently.

A 95% CI excluding 1 strengthens the evidence but is not required to describe the study as exploratory supportive evidence.

Allowed wording:

> Established chronic/nonunion presentations showed greater bone-graft augmentation than acute/new fractures, with wide uncertainty reflecting the small operative sample.

### B. Directionally suggestive but inconclusive

Appropriate when:

- the point estimate is in the hypothesized direction;
- confidence interval is very wide and includes 1;
- leave-one-out direction is generally stable but precision is insufficient.

Allowed wording:

> Bone-graft augmentation was more frequent in established chronic/nonunion records, but the physician-adjudicated sample was too small for a precise association estimate.

This is still a valid result. The paper should not be rescued by switching endpoints.

### C. Fragile / single-record-dependent

Appropriate when:

- removing one evaluable record reverses the effect direction or qualitatively changes the principal conclusion;
- the effect depends strongly on one disputed/adjudicated record.

Allowed wording:

> The apparent treatment-composition difference was sensitive to individual records and should be considered unstable.

In this situation the paper is downgraded to a descriptive cohort/measurement report.

### D. No supportive primary signal

Appropriate when:

- physician-adjudicated bone-graft use is similar across states or opposite to the hypothesized direction.

Required action:

- report the negative primary result;
- do not promote duration or a composite to primary status;
- do not introduce a predictive model to manufacture a stronger story.

## 4. Role of the duration secondary hypothesis

Duration can strengthen mechanistic interpretation only if:

- both graft groups contain physician-valid duration data;
- the continuous distribution remains directionally consistent with the frozen hypothesis;
- the result is presented as secondary and non-causal.

A strong duration P value cannot override a null primary treatment-composition result.

If duration is sparse or inconsistent, it is reported descriptively or omitted from the main text and retained in Supplementary material.

## 5. Role of internal fixation

Internal fixation is the prespecified contrast used to test the proposed treatment-composition dissociation.

If fixation is similarly common in both states while graft differs, the mechanical-base / biological-augmentation interpretation is supported.

If fixation also differs substantially, the paper must describe a broader treatment-composition change rather than forcing the `fixation invariant` narrative.

## 6. Publication decision

### Continue as focused clinical paper

Reasonable if the Gold result is supportive or directionally coherent with acceptable record-level stability.

### Downgrade to brief descriptive report

Appropriate if the primary effect is highly imprecise or single-record-dependent but cohort construction and physician adjudication remain informative.

### Do not rescue with extra modelling

If physician Gold eliminates the signal, the result is negative. The study may be archived as a negative/descriptive analysis; high-capacity ML, LLMs, post-hoc composites, or selective subgroups are not added to create significance.
