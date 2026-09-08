import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ortho_pheno.evaluate_reference_benchmark import (
    evaluate_disease_anatomy, evaluate_scaphoid_state, evaluate_procedures,
)


class ReferenceBenchmarkTests(unittest.TestCase):
    def test_disease_metrics_are_domain_specific(self):
        gold=[
            {'study_id':'H1','domain':'hallux_valgus','gold_disease_anatomy_label':'yes'},
            {'study_id':'S1','domain':'scaphoid_fracture','gold_disease_anatomy_label':'wrist_scaphoid'},
            {'study_id':'C1','domain':'first_cmc_oa','gold_disease_anatomy_label':'no'},
        ]
        pred=[
            {'study_id':'H1','domain':'hallux_valgus','pred_disease_anatomy_label':'yes'},
            {'study_id':'S1','domain':'scaphoid_fracture','pred_disease_anatomy_label':'wrist_scaphoid'},
            {'study_id':'C1','domain':'first_cmc_oa','pred_disease_anatomy_label':'yes'},
        ]
        m=evaluate_disease_anatomy(gold,pred)
        self.assertEqual(m['hallux_valgus']['accuracy'],1.0)
        self.assertEqual(m['scaphoid_fracture']['accuracy'],1.0)
        self.assertEqual(m['first_cmc_oa']['accuracy'],0.0)

    def test_scaphoid_binary_collapse_excludes_uncertain(self):
        gold=[
            {'study_id':'S1','gold_scaphoid_state':'established_nonunion'},
            {'study_id':'S2','gold_scaphoid_state':'acute_or_new_fracture'},
            {'study_id':'S3','gold_scaphoid_state':'insufficient_or_uncertain'},
        ]
        pred=[
            {'study_id':'S1','pred_scaphoid_state_binary':'established_chronic_or_nonunion'},
            {'study_id':'S2','pred_scaphoid_state_binary':'other_wrist_scaphoid'},
            {'study_id':'S3','pred_scaphoid_state_binary':'other_wrist_scaphoid'},
        ]
        m=evaluate_scaphoid_state(gold,pred)
        self.assertEqual(m['n'],2)
        self.assertEqual(m['excluded_uncertain'],1)
        self.assertEqual(m['accuracy'],1.0)

    def test_end_to_end_penalizes_relevance_false_positive(self):
        gold=[
            {'study_id':'H1','domain':'hallux_valgus','gold_target_disease_procedure_present':'yes','gold_procedure_labels':'osteotomy'},
            {'study_id':'H2','domain':'hallux_valgus','gold_target_disease_procedure_present':'no','gold_procedure_labels':''},
        ]
        pred=[
            {'study_id':'H1','domain':'hallux_valgus','pred_target_disease_procedure_present':'yes','pred_procedure_labels':'osteotomy'},
            {'study_id':'H2','domain':'hallux_valgus','pred_target_disease_procedure_present':'yes','pred_procedure_labels':'resection'},
        ]
        m=evaluate_procedures(gold,pred)['hallux_valgus']
        self.assertEqual(m['component_conditional_on_gold_relevance_yes']['exact_set_match'],1.0)
        self.assertLess(m['component_end_to_end']['micro_precision'],1.0)
        self.assertEqual(m['relevance_binary']['specificity'],0.0)

    def test_uncertain_relevance_is_kept_in_three_class_but_excluded_from_e2e(self):
        gold=[
            {'study_id':'C1','domain':'first_cmc_oa','gold_target_disease_procedure_present':'uncertain','gold_procedure_labels':''},
            {'study_id':'C2','domain':'first_cmc_oa','gold_target_disease_procedure_present':'yes','gold_procedure_labels':'trapeziectomy'},
        ]
        pred=[
            {'study_id':'C1','domain':'first_cmc_oa','pred_target_disease_procedure_present':'no','pred_procedure_labels':''},
            {'study_id':'C2','domain':'first_cmc_oa','pred_target_disease_procedure_present':'yes','pred_procedure_labels':'trapeziectomy'},
        ]
        m=evaluate_procedures(gold,pred)['first_cmc_oa']
        self.assertEqual(m['relevance_three_class']['n'],2)
        self.assertEqual(m['n_gold_relevance_uncertain'],1)
        self.assertEqual(m['component_end_to_end']['n'],1)


if __name__=='__main__':
    unittest.main()
