# Table 1. Source architecture and deterministic cohort reconstruction

| Domain | Candidates | Strict phenotype* | Dx rows/admission | Female, % | Age, median [IQR] | BMI, median | Complaint n | Physical exam n | Detailed note module n | Target-disease procedure note n | Imaging/exam record n | CBC n | Coagulation n |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Hallux valgus | 200 | 193 | 10.85 | 82.4 | 54.0 [40.0, 62.0] | 23.5 | 150 | 121 | 114 | 113 | 161 | 161 | 162 |
| Scaphoid retrieval | 88 | 68 | 13.40 | 8.8 | 34.0 [26.8, 45.2] | 25.1 | 55 | 32 | 31 | 28 | 43 | 40 | 39 |
| First-CMC OA | 79 | 28 | 12.40 | 75.0 | 54.0 [46.8, 60.2] | 24.0 | 22 | 18 | 18 | 18 | 24 | 24 | 24 |

*Strict phenotype counts are deterministic phenotype-v0.3 outputs and are not physician-confirmed ground truth until the reference standard is frozen.*

**Interpretation notes.** The analytical unit is the reconstructed admission episode. `Dx rows/admission` quantifies raw diagnosis/demographics row inflation. `Detailed note module n` measures availability of a detailed operative-note export; `Target-disease procedure note n` additionally requires anatomy-aware relevance to the study disease. Missing module availability is not interpreted as clinical absence.
