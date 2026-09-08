import csv
import sys
import tempfile
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src' / 'ortho_pheno'))
from freeze_scaph_reference_v0_1 import build_stage1_manifest, build_final_manifest


def write_csv(path, rows):
    fields = list(rows[0])
    with Path(path).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


class ScaphoidTwoStageFreezeTests(unittest.TestCase):
    def make_stage1(self, root):
        primary = []
        final = []
        for i in range(88):
            sid = f'SCA-{i:03d}'
            label = 'wrist_scaphoid' if i < 2 else 'foot_navicular'
            primary.append({'study_id': sid, 'gold_anatomy_label': label})
            final.append({'study_id': sid, 'gold_anatomy_label': label})
        write_csv(root / 'scaphoid_anatomy_review.csv', primary)
        write_csv(root / 'scaphoid_anatomy_review_reviewer2.csv', [
            {'study_id': 'SCA-000', 'reviewer2_gold_anatomy_label': 'wrist_scaphoid'},
            {'study_id': 'SCA-002', 'reviewer2_gold_anatomy_label': 'foot_navicular'},
        ])
        write_csv(root / 'scaphoid_anatomy_double_review_manifest.csv', [
            {'study_id': 'SCA-000', 'layer': 'anatomy', 'hash_score': '0.01'},
            {'study_id': 'SCA-002', 'layer': 'anatomy', 'hash_score': '0.02'},
        ])
        write_csv(root / 'scaphoid_anatomy_adjudicated.csv', final)

    def make_stage2(self, root):
        state_primary = [
            {
                'study_id': 'SCA-000', 'gold_scaphoid_state': 'established_nonunion',
                'gold_relevant_duration_present': 'yes', 'gold_relevant_duration_value': '12',
                'gold_relevant_duration_unit': 'months', 'gold_duration_basis': 'injury_since_event',
            },
            {
                'study_id': 'SCA-001', 'gold_scaphoid_state': 'acute_or_new_fracture',
                'gold_relevant_duration_present': 'no', 'gold_relevant_duration_value': '',
                'gold_relevant_duration_unit': '', 'gold_duration_basis': '',
            },
        ]
        write_csv(root / 'scaphoid_state_review.csv', state_primary)
        write_csv(root / 'scaphoid_state_review_reviewer2.csv', [{
            'study_id': 'SCA-000', 'reviewer2_gold_scaphoid_state': 'established_nonunion',
            'reviewer2_gold_relevant_duration_present': 'yes', 'reviewer2_gold_relevant_duration_value': '1',
            'reviewer2_gold_relevant_duration_unit': 'years', 'reviewer2_gold_duration_basis': 'injury_since_event',
        }])
        write_csv(root / 'scaphoid_state_adjudicated.csv', state_primary)

        procedure_primary = [{
            'study_id': 'SCA-000', 'gold_target_disease_procedure_present': 'yes',
            'gold_internal_fixation': 'yes', 'gold_bone_graft': 'yes',
            'gold_reconstruction': 'no', 'gold_fusion': 'no',
        }]
        write_csv(root / 'scaphoid_procedure_review.csv', procedure_primary)
        write_csv(root / 'scaphoid_procedure_review_reviewer2.csv', [{
            'study_id': 'SCA-000', 'reviewer2_gold_target_disease_procedure_present': 'yes',
            'reviewer2_gold_internal_fixation': 'yes', 'reviewer2_gold_bone_graft': 'yes',
            'reviewer2_gold_reconstruction': 'no', 'reviewer2_gold_fusion': 'no',
        }])
        write_csv(root / 'scaphoid_procedure_adjudicated.csv', procedure_primary)
        write_csv(root / 'scaphoid_downstream_double_review_manifest.csv', [
            {'study_id': 'SCA-000', 'layer': 'state', 'hash_score': '0.01'},
            {'study_id': 'SCA-000', 'layer': 'procedure', 'hash_score': '0.01'},
        ])

    def test_stage1_and_final_manifest_build(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_stage1(root)
            stage1 = build_stage1_manifest(root)
            self.assertEqual(stage1['reference_standard_status'], 'stage1_frozen')
            self.make_stage2(root)
            final = build_final_manifest(root)
            self.assertEqual(final['reference_standard_status'], 'final_frozen')

    def test_final_manifest_rejects_state_id_drift(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_stage1(root)
            self.make_stage2(root)
            p = root / 'scaphoid_state_review.csv'
            rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))
            rows.pop()
            write_csv(p, rows)
            with self.assertRaises(ValueError):
                build_final_manifest(root)

    def test_final_manifest_rejects_nonwrist_procedure_id(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_stage1(root)
            self.make_stage2(root)
            p = root / 'scaphoid_procedure_review.csv'
            rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))
            rows[0]['study_id'] = 'SCA-002'
            write_csv(p, rows)
            with self.assertRaises(ValueError):
                build_final_manifest(root)


if __name__ == '__main__':
    unittest.main()
