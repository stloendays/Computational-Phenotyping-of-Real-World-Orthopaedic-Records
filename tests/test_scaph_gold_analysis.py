import math
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src' / 'ortho_pheno'))

from analyze_scaph_gold_v0_1 import analyze, exact_binary_analysis, state_group
from analyze_scaph_gold_v0_2 import public_rows


class ScaphoidGoldAnalysisTests(unittest.TestCase):
    def record(self, group, graft, fixation='yes', duration=None, basis='injury_since_event'):
        return {
            'group': group,
            'graft': graft,
            'fixation': fixation,
            'reconstruction': 'no',
            'fusion': 'no',
            'augmentation': 'yes' if graft == 'yes' else ('no' if graft == 'no' else 'uncertain'),
            'component_count': None if graft == 'uncertain' else (2 if graft == 'yes' else 1),
            'duration_days': duration,
            'duration_basis': basis if duration is not None else '',
            'age': 35.0,
            'sex': '男',
            'bmi': 24.0,
        }

    def test_state_group_is_strict_acute_vs_established(self):
        self.assertEqual(state_group('acute_or_new_fracture'), 'acute_new')
        self.assertEqual(state_group('established_nonunion'), 'chronic_nonunion')
        self.assertEqual(state_group('established_chronic_fracture'), 'chronic_nonunion')
        self.assertEqual(state_group('chronic_nonunion_not_distinguishable'), 'chronic_nonunion')
        self.assertIsNone(state_group('insufficient_or_uncertain'))

    def test_uncertain_component_is_excluded_from_primary_denominator(self):
        result = exact_binary_analysis(['yes', 'no', 'uncertain'], ['no', 'no', 'yes'])
        self.assertEqual(result['chronic_evaluable'], 2)
        self.assertEqual(result['acute_evaluable'], 3)
        self.assertEqual(result['chronic_uncertain_or_missing'], 1)
        self.assertEqual(result['table']['chronic_yes'], 1)

    def test_analysis_keeps_duration_secondary(self):
        records = [
            self.record('chronic_nonunion', 'yes', duration=365),
            self.record('chronic_nonunion', 'yes', duration=180),
            self.record('chronic_nonunion', 'no', duration=20),
            self.record('acute_new', 'no'),
            self.record('acute_new', 'no'),
            self.record('acute_new', 'yes'),
        ]
        result = analyze(records)
        self.assertEqual(result['primary_bone_graft']['table']['chronic_yes'], 2)
        self.assertEqual(result['primary_bone_graft']['table']['acute_yes'], 1)
        self.assertEqual(result['secondary_duration']['bone_graft_present']['n'], 2)
        self.assertEqual(result['secondary_duration']['bone_graft_absent']['n'], 1)
        self.assertEqual(result['analysis_plan'], 'SCAPHOID_ANALYSIS_PLAN_V0_3')

    def test_leave_one_out_is_generated_for_primary(self):
        records = [
            self.record('chronic_nonunion', 'yes'),
            self.record('chronic_nonunion', 'yes'),
            self.record('chronic_nonunion', 'no'),
            self.record('acute_new', 'no'),
            self.record('acute_new', 'no'),
            self.record('acute_new', 'yes'),
        ]
        result = analyze(records)
        loo = result['leave_one_out_primary_bone_graft']
        self.assertEqual(loo['iterations'], 6)
        self.assertIn('p_min', loo)
        self.assertIn('p_max', loo)

    def test_public_release_suppresses_small_denominator_and_duration_distribution(self):
        records = [
            self.record('chronic_nonunion', 'yes', duration=365),
            self.record('chronic_nonunion', 'yes', duration=180),
            self.record('acute_new', 'no'),
            self.record('acute_new', 'no'),
        ]
        result = analyze(records)
        rows = {r['metric']: r for r in public_rows(result)}
        self.assertEqual(rows['operative_population']['chronic_nonunion'], '<5')
        self.assertEqual(rows['operative_population']['acute_new'], '<5')
        self.assertEqual(rows['bone_graft']['chronic_nonunion'], '<5 total')
        self.assertIn('distribution suppressed', rows['duration_days_graft_present']['chronic_nonunion'])

    def test_exact_or_and_ci_are_available_with_positive_cells(self):
        result = exact_binary_analysis(
            ['yes'] * 8 + ['no'] * 7,
            ['yes'] * 2 + ['no'] * 11,
        )
        self.assertGreater(result['odds_ratio_conditional'], 1)
        self.assertTrue(math.isfinite(result['ci95_low']))
        self.assertTrue(math.isfinite(result['ci95_high']))
        self.assertIsNotNone(result['fisher_two_sided_p'])


if __name__ == '__main__':
    unittest.main()
