# Data Release Notes v0.1

## Scope

This release organizes the complete source archive supplied for the project while enforcing a strict public-data boundary. The source archive contains 18 files: 12 `.xlsx` EHR exports and 6 legacy `.xls` examination/laboratory workbooks.

## Key reproducible cohort counts

| Domain | Candidate admissions | Deterministic strict phenotype |
|---|---:|---:|
| Hallux valgus | 200 | 193 |
| First CMC osteoarthritis | 79 | 28 |
| Wrist scaphoid | 88 | 72 |

The large reduction in the first-CMC cohort reflects diagnostic/anatomical contamination of broad wrist-arthritis retrieval. The scaphoid phenotype requires explicit wrist/hand scaphoid evidence to avoid conflating wrist scaphoid with foot navicular fractures.

## Data-density observations

The source data are longitudinally heterogeneous. Diagnosis tables contain repeated rows per admission because each additional diagnosis generates another row, so Excel row counts cannot be treated as sample size. All inferential analyses must operate at the admission/patient-episode level.

The legacy examination and laboratory exports are now included in the inventory and aggregate coverage calculations. Their raw row counts represent repeated tests, not unique patients.

## Public release strategy

Only aggregate outputs are committed. Small cells in public stratified tables are suppressed as `<5`. Direct identifiers, patient-level dates, free text, and row-level laboratory/examination data remain local.

## Interpretation boundary

The scaphoid chronic/nonunion flag is a **text-supported established phenotype**. Unless a patient's available records explicitly document progression from an acute fracture to subsequent nonunion, the group comparison must not be interpreted as prospective prediction of incident nonunion.
