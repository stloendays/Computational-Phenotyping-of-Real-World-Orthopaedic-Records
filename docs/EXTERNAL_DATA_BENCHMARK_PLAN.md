# External Data and Benchmark Plan

## 1. Principle

External datasets are used to benchmark or pretrain **computational components**. They are not pooled with the local hospital patients to inflate the clinical sample size.

The local fixed dataset answers the orthopaedic clinical questions. External datasets answer narrower methodological questions such as whether a system has general Chinese biomedical language competence.

## 2. Selected external benchmark: CBLUE

**CBLUE (Chinese Biomedical Language Understanding Evaluation)** is a public Chinese biomedical NLP benchmark described in ACL 2022.

Primary references:

- official repository: https://github.com/CBLUEbenchmark/CBLUE
- paper: https://aclanthology.org/2022.acl-long.544/
- DOI: https://doi.org/10.18653/v1/2022.acl-long.544
- dataset-download entry referenced by the official repository: https://tianchi.aliyun.com/dataset/dataDetail?dataId=95414

The official benchmark includes eight Chinese biomedical NLU tasks. The two tasks most relevant to this project are:

### CMeEE

Task: Chinese medical named-entity recognition.

Official benchmark sizes:

- train: 15,000;
- dev: 5,000;
- test: 3,000;
- primary metric: micro-F1.

Role in this project:

- assess generic Chinese medical entity extraction competence;
- test robustness to biomedical disease/body-part/symptom terminology;
- provide external methodological context for local anatomy/disease extraction.

CMeEE is **not** an external validation cohort for hallux valgus, scaphoid disease or first-CMC OA.

### CHIP-CDN

Task: normalization of diagnosis entities from Chinese clinical records to standardized diagnosis terms.

Official benchmark sizes:

- train: 6,000;
- dev: 2,000;
- test: 10,192;
- primary metric: micro-F1.

Role in this project:

- assess diagnosis-normalization competence on Chinese clinical terminology;
- motivate/benchmark handling of synonymous or non-standard diagnosis strings;
- provide an external task relevant to normalization before local orthopaedic disambiguation.

CHIP-CDN does **not** directly validate the local strict disease definitions, because the local task additionally requires orthopaedic anatomical context, uncertainty handling and admission-level evidence integration.

## 3. Optional CBLUE tasks

CMeIE relation extraction may be explored if a later model explicitly extracts relations such as anatomy-to-disease or procedure-to-anatomical-target. It is not required for the primary paper.

Other CBLUE classification, similarity and QA tasks are outside the primary scientific question and should not be added merely to increase the number of benchmarks.

## 4. Two-level validation design

A model may therefore have two distinct evidence layers.

### Layer A - public task-native competence

Evaluate on the original CBLUE task and metric without changing the benchmark definition.

This answers:

> Does the system perform reasonably on an established Chinese biomedical NLP benchmark?

### Layer B - local orthopaedic clinical validity

Evaluate the same extraction architecture on the frozen physician reference standard for:

- disease/anatomy classification;
- scaphoid state;
- target-disease procedure attribution;
- procedure-component extraction.

This answers:

> Does the system correctly solve the actual orthopaedic EHR tasks in this study?

Strong CBLUE performance cannot substitute for Layer B.

## 5. No clinical pooling

The following design is prohibited:

`CBLUE records + local hospital patients -> one enlarged clinical cohort`

Reasons:

- different tasks and sampling frames;
- different outcome definitions;
- different source systems;
- no patient-level comparability;
- risk of invalid clinical inference.

External data may influence model development or provide an independent benchmark, but local clinical denominators remain unchanged.

## 6. Imaging datasets

Public musculoskeletal imaging datasets were considered earlier. They are not part of the current primary analysis because the fixed local dataset does not provide the raw local X-ray/CT images needed for meaningful local image-model validation.

Accordingly, this study will not add an imaging deep-learning module solely because external image datasets exist. An external-only imaging experiment would answer a separate question and would dilute the current EHR-phenotyping paper.

## 7. Data and licence handling

The CBLUE GitHub repository is distributed under Apache-2.0 for the repository/code. Dataset users must additionally follow the terms shown by the official dataset-download source and task documentation.

Third-party datasets are downloaded locally and are not vendored into this repository. `.gitignore` excludes local external-data directories.

## 8. Reporting boundary

Allowed wording after completing a public benchmark:

> The extraction architecture was additionally evaluated on established Chinese biomedical NLP tasks to characterize general-domain biomedical language competence.

Not allowed:

> The local orthopaedic findings were externally clinically validated by CBLUE.

The latter would misrepresent the external data.

## 9. Current priority

External benchmark work is secondary to the frozen local physician reference standard. The sequence remains:

1. complete/freeze physician annotations;
2. score deterministic local baseline;
3. run the same candidate semantic/LLM system on local frozen labels;
4. use CBLUE as an auxiliary public benchmark for Chinese biomedical NLP competence;
5. report public and local results as distinct validation layers.
