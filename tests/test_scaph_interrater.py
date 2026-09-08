import csv
import sys
import tempfile
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src' / 'ortho_pheno'))
from scaph_interrater_agreement_v0_1 import build


def write_csv(path, rows):
    with Path(path).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


class ScaphoidInterraterTests(unittest.TestCase):
    def test_builds_aggregate_metrics_without_ids(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            write_csv(d/'scaphoid_anatomy_review.csv', [
                {'study_id':'A','gold_anatomy_label':'wrist_scaphoid'},
                {'study_id':'B','gold_anatomy_label':'foot_navicular'},
            ])
            write_csv(d/'scaphoid_anatomy_review_reviewer2.csv', [
                {'study_id':'A','reviewer2_gold_anatomy_label':'wrist_scaphoid'},
                {'study_id':'B','reviewer2_gold_anatomy_label':'wrist_scaphoid'},
            ])
            write_csv(d/'scaphoid_state_review.csv', [
                {'study_id':'A','gold_scaphoid_state':'established_nonunion','gold_relevant_duration_present':'yes','gold_relevant_duration_value':'12','gold_relevant_duration_unit':'months','gold_duration_basis':'injury_since_event'},
                {'study_id':'B','gold_scaphoid_state':'acute_or_new_fracture','gold_relevant_duration_present':'no','gold_relevant_duration_value':'','gold_relevant_duration_unit':'','gold_duration_basis':''},
            ])
            write_csv(d/'scaphoid_state_review_reviewer2.csv', [
                {'study_id':'A','reviewer2_gold_scaphoid_state':'established_nonunion','reviewer2_gold_relevant_duration_present':'yes','reviewer2_gold_relevant_duration_value':'1','reviewer2_gold_relevant_duration_unit':'years','reviewer2_gold_duration_basis':'injury_since_event'},
                {'study_id':'B','reviewer2_gold_scaphoid_state':'acute_or_new_fracture','reviewer2_gold_relevant_duration_present':'no','reviewer2_gold_relevant_duration_value':'','reviewer2_gold_relevant_duration_unit':'','reviewer2_gold_duration_basis':''},
            ])
            write_csv(d/'scaphoid_procedure_review.csv', [
                {'study_id':'A','gold_target_disease_procedure_present':'yes','gold_internal_fixation':'yes','gold_bone_graft':'yes','gold_reconstruction':'no','gold_fusion':'no'},
            ])
            write_csv(d/'scaphoid_procedure_review_reviewer2.csv', [
                {'study_id':'A','reviewer2_gold_target_disease_procedure_present':'yes','reviewer2_gold_internal_fixation':'yes','reviewer2_gold_bone_graft':'yes','reviewer2_gold_reconstruction':'no','reviewer2_gold_fusion':'no'},
            ])
            result = build(d)
            self.assertEqual(result['double_review_counts']['anatomy'], 2)
            self.assertEqual(result['state_full']['raw_agreement'], 1.0)
            self.assertEqual(result['procedure_relevance']['raw_agreement'], 1.0)
            self.assertEqual(result['duration_numeric_among_both_present']['n'], 1)
            self.assertAlmostEqual(result['duration_numeric_among_both_present']['median_absolute_difference_days'], 0.0, places=6)
            self.assertNotIn('A', str(result))
            self.assertNotIn('B', str(result))


if __name__ == '__main__':
    unittest.main()
