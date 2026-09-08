import csv
import sys
import tempfile
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src' / 'ortho_pheno'))

from freeze_scaph_reference_v0_1 import validate_duration, validate_procedure_row
from make_scaph_adjudication_templates_v0_1 import build_anatomy, build_state, build_procedure


def write_csv(path, rows):
    fields = list(rows[0])
    with Path(path).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


def read_csv(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


class ScaphoidReferenceToolTests(unittest.TestCase):
    def test_duration_consistency(self):
        row = {
            'gold_relevant_duration_present': 'yes',
            'gold_relevant_duration_value': '1.5',
            'gold_relevant_duration_unit': 'months',
            'gold_duration_basis': 'injury_since_event',
        }
        validate_duration(row, 'gold_', 'test')

        bad = dict(row)
        bad['gold_relevant_duration_present'] = 'no'
        with self.assertRaises(ValueError):
            validate_duration(bad, 'gold_', 'test')

    def test_procedure_relevance_controls_component_labels(self):
        yes_row = {
            'gold_target_disease_procedure_present': 'yes',
            'gold_internal_fixation': 'yes',
            'gold_bone_graft': 'no',
            'gold_reconstruction': 'no',
            'gold_fusion': 'no',
        }
        validate_procedure_row(yes_row, 'gold_', 'test')

        bad = dict(yes_row)
        bad['gold_target_disease_procedure_present'] = 'no'
        with self.assertRaises(ValueError):
            validate_procedure_row(bad, 'gold_', 'test')

    def test_anatomy_disagreement_is_not_silently_resolved(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            write_csv(d / 'scaphoid_anatomy_review.csv', [
                {'study_id': 'A', 'gold_anatomy_label': 'wrist_scaphoid'},
                {'study_id': 'B', 'gold_anatomy_label': 'foot_navicular'},
                {'study_id': 'C', 'gold_anatomy_label': 'wrist_scaphoid'},
            ])
            write_csv(d / 'scaphoid_anatomy_review_reviewer2.csv', [
                {'study_id': 'A', 'reviewer2_gold_anatomy_label': 'wrist_scaphoid'},
                {'study_id': 'B', 'reviewer2_gold_anatomy_label': 'wrist_scaphoid'},
            ])
            build_anatomy(d)
            rows = {r['study_id']: r for r in read_csv(d / 'scaphoid_anatomy_adjudicated.csv')}
            self.assertEqual(rows['A']['gold_anatomy_label'], 'wrist_scaphoid')
            self.assertEqual(rows['B']['gold_anatomy_label'], '')
            self.assertEqual(rows['B']['reviewer_agreement'], 'no')
            self.assertEqual(rows['C']['gold_anatomy_label'], 'wrist_scaphoid')

    def test_state_any_vector_disagreement_requires_adjudication(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            write_csv(d / 'scaphoid_state_review.csv', [{
                'study_id': 'A',
                'gold_scaphoid_state': 'established_nonunion',
                'gold_relevant_duration_present': 'yes',
                'gold_relevant_duration_value': '12',
                'gold_relevant_duration_unit': 'months',
                'gold_duration_basis': 'injury_since_event',
            }])
            write_csv(d / 'scaphoid_state_review_reviewer2.csv', [{
                'study_id': 'A',
                'reviewer2_gold_scaphoid_state': 'established_nonunion',
                'reviewer2_gold_relevant_duration_present': 'yes',
                'reviewer2_gold_relevant_duration_value': '10',
                'reviewer2_gold_relevant_duration_unit': 'months',
                'reviewer2_gold_duration_basis': 'injury_since_event',
            }])
            build_state(d)
            row = read_csv(d / 'scaphoid_state_adjudicated.csv')[0]
            self.assertEqual(row['reviewer_agreement'], 'no')
            self.assertEqual(row['gold_scaphoid_state'], '')
            self.assertEqual(row['gold_relevant_duration_value'], '')

    def test_procedure_disagreement_requires_adjudication(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            write_csv(d / 'scaphoid_procedure_review.csv', [{
                'study_id': 'A',
                'gold_target_disease_procedure_present': 'yes',
                'gold_internal_fixation': 'yes',
                'gold_bone_graft': 'yes',
                'gold_reconstruction': 'no',
                'gold_fusion': 'no',
            }])
            write_csv(d / 'scaphoid_procedure_review_reviewer2.csv', [{
                'study_id': 'A',
                'reviewer2_gold_target_disease_procedure_present': 'yes',
                'reviewer2_gold_internal_fixation': 'yes',
                'reviewer2_gold_bone_graft': 'no',
                'reviewer2_gold_reconstruction': 'no',
                'reviewer2_gold_fusion': 'no',
            }])
            build_procedure(d)
            row = read_csv(d / 'scaphoid_procedure_adjudicated.csv')[0]
            self.assertEqual(row['reviewer_agreement'], 'no')
            self.assertEqual(row['gold_bone_graft'], '')


if __name__ == '__main__':
    unittest.main()
