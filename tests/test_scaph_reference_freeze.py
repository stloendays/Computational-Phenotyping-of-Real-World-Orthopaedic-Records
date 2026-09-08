import csv
import json
import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src' / 'ortho_pheno'))
from freeze_scaph_reference_v0_1 import build_manifest, verify_manifest


def write_rows(path, fields, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


class ScaphoidReferenceFreezeTests(unittest.TestCase):
    def make_valid(self, root):
        anatomy_fields = ['study_id','gold_anatomy_label']
        anatomy = [
            {'study_id':f'SCA-{i:03d}','gold_anatomy_label':'wrist_scaphoid' if i < 68 else 'foot_navicular'}
            for i in range(88)
        ]
        write_rows(root/'scaphoid_anatomy_review.csv', anatomy_fields, anatomy)
        write_rows(root/'scaphoid_anatomy_review_reviewer2.csv',
                   ['study_id','reviewer2_gold_anatomy_label'],
                   [{'study_id':'SCA-000','reviewer2_gold_anatomy_label':'wrist_scaphoid'}])

        state_fields = [
            'study_id','gold_scaphoid_state','gold_relevant_duration_present',
            'gold_relevant_duration_value','gold_relevant_duration_unit','gold_duration_basis'
        ]
        state = [{
            'study_id':'SCA-000','gold_scaphoid_state':'established_nonunion',
            'gold_relevant_duration_present':'yes','gold_relevant_duration_value':'1.5',
            'gold_relevant_duration_unit':'years','gold_duration_basis':'injury_since_event'
        }]
        write_rows(root/'scaphoid_state_review.csv', state_fields, state)
        write_rows(root/'scaphoid_state_review_reviewer2.csv',
                   ['study_id','reviewer2_gold_scaphoid_state','reviewer2_gold_relevant_duration_present',
                    'reviewer2_gold_relevant_duration_value','reviewer2_gold_relevant_duration_unit','reviewer2_gold_duration_basis'],
                   [{'study_id':'SCA-000','reviewer2_gold_scaphoid_state':'established_nonunion',
                     'reviewer2_gold_relevant_duration_present':'yes','reviewer2_gold_relevant_duration_value':'1.5',
                     'reviewer2_gold_relevant_duration_unit':'years','reviewer2_gold_duration_basis':'injury_since_event'}])

        proc_fields = [
            'study_id','gold_target_disease_procedure_present','gold_internal_fixation',
            'gold_bone_graft','gold_reconstruction','gold_fusion'
        ]
        proc = [{'study_id':'SCA-000','gold_target_disease_procedure_present':'yes',
                 'gold_internal_fixation':'yes','gold_bone_graft':'yes',
                 'gold_reconstruction':'no','gold_fusion':'no'}]
        write_rows(root/'scaphoid_procedure_review.csv', proc_fields, proc)
        write_rows(root/'scaphoid_procedure_review_reviewer2.csv',
                   ['study_id','reviewer2_gold_target_disease_procedure_present','reviewer2_gold_internal_fixation',
                    'reviewer2_gold_bone_graft','reviewer2_gold_reconstruction','reviewer2_gold_fusion'],
                   [{'study_id':'SCA-000','reviewer2_gold_target_disease_procedure_present':'yes',
                     'reviewer2_gold_internal_fixation':'yes','reviewer2_gold_bone_graft':'yes',
                     'reviewer2_gold_reconstruction':'no','reviewer2_gold_fusion':'no'}])

    def test_valid_reference_builds_and_verifies(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_valid(root)
            manifest = build_manifest(root)
            self.assertEqual(manifest['reference_standard_status'], 'frozen')
            out = root/'freeze.json'
            out.write_text(json.dumps(manifest), encoding='utf-8')
            self.assertTrue(verify_manifest(root, out))

    def test_duration_yes_requires_numeric_value_and_unit(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_valid(root)
            p = root/'scaphoid_state_review.csv'
            rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))
            rows[0]['gold_relevant_duration_value'] = ''
            write_rows(p, rows[0].keys(), rows)
            with self.assertRaises(ValueError):
                build_manifest(root)

    def test_duration_no_cannot_retain_value(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_valid(root)
            p = root/'scaphoid_state_review.csv'
            rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))
            rows[0]['gold_relevant_duration_present'] = 'no'
            rows[0]['gold_relevant_duration_value'] = '10'
            rows[0]['gold_relevant_duration_unit'] = 'days'
            rows[0]['gold_duration_basis'] = ''
            write_rows(p, rows[0].keys(), rows)
            with self.assertRaises(ValueError):
                build_manifest(root)

    def test_irrelevant_procedure_cannot_have_component_labels(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_valid(root)
            p = root/'scaphoid_procedure_review.csv'
            rows = list(csv.DictReader(p.open(encoding='utf-8-sig')))
            rows[0]['gold_target_disease_procedure_present'] = 'no'
            with self.assertRaises(ValueError):
                build_manifest(root)

    def test_hash_mutation_is_detected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_valid(root)
            manifest = build_manifest(root)
            out = root/'freeze.json'
            out.write_text(json.dumps(manifest), encoding='utf-8')
            p = root/'scaphoid_anatomy_review.csv'
            p.write_text(p.read_text(encoding='utf-8-sig') + '\n', encoding='utf-8-sig')
            with self.assertRaises(ValueError):
                verify_manifest(root, out)


if __name__ == '__main__':
    unittest.main()
