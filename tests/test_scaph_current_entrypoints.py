import json
import sys
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src' / 'ortho_pheno'))

import freeze_scaph_reference_v0_2 as freeze_v2
from build_scaph_final_tables_v0_1 import build as build_tables


class CurrentScaphoidEntrypointTests(unittest.TestCase):
    def test_freeze_v2_aligns_manifest_metadata(self):
        fake = {
            'manifest_version': 'x',
            'reference_standard_status': 'final_frozen',
            'files': {},
        }
        with mock.patch.object(freeze_v2, '_build_final_manifest', return_value=fake.copy()):
            result = freeze_v2.build_final_manifest(Path('/tmp/unused'))
        self.assertEqual(result['analysis_plan'], 'SCAPHOID_ANALYSIS_PLAN_V0_3')
        self.assertEqual(result['primary_outcome'], 'bone_graft_augmentation')
        self.assertEqual(
            result['primary_comparison'],
            'established_chronic_nonunion_vs_physician_confirmed_acute_new',
        )

    def test_table_builder_formats_exact_private_results(self):
        result = {
            'operative_population': {
                'chronic_nonunion_n': 6,
                'acute_new_n': 5,
                'total_n': 11,
            },
            'baseline': {
                'chronic_nonunion': {
                    'age': {'n': 6, 'median': 40, 'q1': 30, 'q3': 50},
                    'bmi': {'n': 5, 'median': 24, 'q1': 22, 'q3': 26},
                    'sex': {'known_n': 6, 'female_n': 1},
                },
                'acute_new': {
                    'age': {'n': 5, 'median': 35, 'q1': 28, 'q3': 41},
                    'bmi': {'n': 4, 'median': 25, 'q1': 23, 'q3': 27},
                    'sex': {'known_n': 5, 'female_n': 0},
                },
            },
            'primary_bone_graft': {
                'table': {'chronic_yes': 4, 'chronic_no': 2, 'acute_yes': 1, 'acute_no': 4},
                'chronic_evaluable': 6,
                'acute_evaluable': 5,
                'odds_ratio_conditional': 6.2,
                'ci95_low': 0.5,
                'ci95_high': 120,
                'fisher_two_sided_p': 0.12,
            },
            'key_contrast_internal_fixation': {
                'table': {'chronic_yes': 6, 'chronic_no': 0, 'acute_yes': 5, 'acute_no': 0},
                'chronic_evaluable': 6,
                'acute_evaluable': 5,
                'odds_ratio_conditional': float('nan'),
                'ci95_low': 0,
                'ci95_high': float('inf'),
                'fisher_two_sided_p': 1.0,
            },
            'secondary_augmentation_composite': {
                'table': {'chronic_yes': 5, 'chronic_no': 1, 'acute_yes': 1, 'acute_no': 4},
                'chronic_evaluable': 6,
                'acute_evaluable': 5,
                'odds_ratio_conditional': 13,
                'ci95_low': 0.7,
                'ci95_high': 500,
                'fisher_two_sided_p': 0.08,
            },
            'secondary_component_count': {
                'chronic_nonunion': {'n': 6, 'median': 2, 'q1': 1, 'q3': 2},
                'acute_new': {'n': 5, 'median': 1, 'q1': 1, 'q3': 1},
                'mann_whitney': {'u': 20, 'p_value': 0.04},
            },
            'secondary_duration': {
                'bone_graft_present': {'n': 4, 'median': 180, 'q1': 90, 'q3': 365},
                'bone_graft_absent': {'n': 2, 'median': 20, 'q1': 10, 'q3': 30},
                'mann_whitney': {'u': 8, 'p_value': 0.09},
                'injury_basis_only': {
                    'bone_graft_present': {'n': 3, 'median': 200, 'q1': 100, 'q3': 400},
                    'bone_graft_absent': {'n': 2, 'median': 20, 'q1': 10, 'q3': 30},
                    'mann_whitney': {'u': 6, 'p_value': 0.10},
                },
            },
        }
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            js = root / 'analysis.json'
            js.write_text(json.dumps(result), encoding='utf-8')
            paths = build_tables(js, root / 'tables')
            self.assertTrue(paths['table1'].exists())
            self.assertTrue(paths['table2'].exists())
            self.assertTrue(paths['table_s1'].exists())
            text = paths['table2'].read_text(encoding='utf-8')
            self.assertIn('Bone-graft augmentation', text)
            self.assertIn('4/6 (66.7%)', text)
            self.assertIn('6.20', text)


if __name__ == '__main__':
    unittest.main()
