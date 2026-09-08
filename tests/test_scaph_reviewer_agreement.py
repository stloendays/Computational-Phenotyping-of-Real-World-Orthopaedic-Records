import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src' / 'ortho_pheno'))
from scaph_reviewer_agreement_v0_1 import (
    categorical_agreement,
    cohen_kappa,
    duration_numeric_agreement,
    both_duration_yes,
    both_procedure_relevant,
)


class ReviewerAgreementTests(unittest.TestCase):
    def test_perfect_kappa(self):
        self.assertAlmostEqual(cohen_kappa(['a','b','a'], ['a','b','a']), 1.0)

    def test_duration_detail_is_conditional_on_both_present_yes(self):
        primary = [
            {'study_id':'1','gold_relevant_duration_present':'no','gold_relevant_duration_unit':''},
            {'study_id':'2','gold_relevant_duration_present':'yes','gold_relevant_duration_unit':'months'},
        ]
        reviewer2 = [
            {'study_id':'1','reviewer2_gold_relevant_duration_present':'no','reviewer2_gold_relevant_duration_unit':''},
            {'study_id':'2','reviewer2_gold_relevant_duration_present':'yes','reviewer2_gold_relevant_duration_unit':'months'},
        ]
        disagreements=[]
        result = categorical_agreement(
            primary, reviewer2,
            'gold_relevant_duration_unit','reviewer2_gold_relevant_duration_unit',
            'duration_unit',disagreements,include=both_duration_yes,
        )
        self.assertEqual(result['n'], 1)
        self.assertEqual(result['exact_agreement'], 1.0)

    def test_procedure_components_are_conditional_on_both_relevant(self):
        primary = [
            {'study_id':'1','gold_target_disease_procedure_present':'no','gold_bone_graft':''},
            {'study_id':'2','gold_target_disease_procedure_present':'yes','gold_bone_graft':'yes'},
        ]
        reviewer2 = [
            {'study_id':'1','reviewer2_gold_target_disease_procedure_present':'no','reviewer2_gold_bone_graft':''},
            {'study_id':'2','reviewer2_gold_target_disease_procedure_present':'yes','reviewer2_gold_bone_graft':'yes'},
        ]
        disagreements=[]
        result = categorical_agreement(
            primary, reviewer2,
            'gold_bone_graft','reviewer2_gold_bone_graft',
            'bone_graft',disagreements,include=both_procedure_relevant,
        )
        self.assertEqual(result['n'], 1)
        self.assertEqual(result['exact_agreement'], 1.0)

    def test_duration_values_normalize_across_units(self):
        primary = [{
            'study_id':'1','gold_relevant_duration_present':'yes',
            'gold_relevant_duration_value':'6','gold_relevant_duration_unit':'months',
        }]
        reviewer2 = [{
            'study_id':'1','reviewer2_gold_relevant_duration_present':'yes',
            'reviewer2_gold_relevant_duration_value':'0.5','reviewer2_gold_relevant_duration_unit':'years',
        }]
        disagreements=[]
        result = duration_numeric_agreement(primary,reviewer2,disagreements)
        self.assertEqual(result['n_both_duration_yes'], 1)
        self.assertGreater(result['normalized_numeric_agreement'], 0.99)


if __name__ == '__main__':
    unittest.main()
