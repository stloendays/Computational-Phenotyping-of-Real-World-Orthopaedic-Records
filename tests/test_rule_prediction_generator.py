import csv
import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ortho_pheno.generate_rule_predictions import (
    read_source_rows, disease_anatomy_predictions,
    scaphoid_state_predictions, procedure_predictions,
)


class RulePredictionGeneratorTests(unittest.TestCase):
    def test_gold_columns_are_never_exposed(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'x.csv'
            with p.open('w',encoding='utf-8-sig',newline='') as f:
                w=csv.DictWriter(f,fieldnames=['study_id','domain','diagnosis_text','gold_disease_anatomy_label'])
                w.writeheader(); w.writerow({'study_id':'S1','domain':'hallux_valgus','diagnosis_text':'双足拇外翻','gold_disease_anatomy_label':'no'})
            rows=read_source_rows(p)
            self.assertNotIn('gold_disease_anatomy_label',rows[0])
            self.assertEqual(disease_anatomy_predictions(rows)[0]['pred_disease_anatomy_label'],'yes')

    def test_scaphoid_ambiguous_maps_to_uncertain(self):
        rows=[{'study_id':'S2','domain':'scaphoid_fracture','diagnosis_text':'舟骨骨折','complaint_text':'','physical_exam_text':''}]
        self.assertEqual(disease_anatomy_predictions(rows)[0]['pred_disease_anatomy_label'],'uncertain')

    def test_scaphoid_state_uses_nonoperative_text_only(self):
        rows=[{'study_id':'S3','diagnosis_text':'右腕舟骨新鲜骨折','complaint_text':'','physical_exam_text':''}]
        self.assertEqual(scaphoid_state_predictions(rows)[0]['pred_scaphoid_state_binary'],'other_wrist_scaphoid')

    def test_unrelated_operation_becomes_procedure_hard_negative(self):
        rows=[{'study_id':'S4','domain':'scaphoid_fracture','operation_name_text':'腕舟骨骨折','operation_note_text':'手术名称：右桡骨远端骨折钢针内固定术。'}]
        pred=procedure_predictions(rows)[0]
        self.assertEqual(pred['pred_target_disease_procedure_present'],'no')
        self.assertEqual(pred['pred_procedure_labels'],'')

    def test_target_operation_extracts_components(self):
        rows=[{'study_id':'S5','domain':'scaphoid_fracture','operation_name_text':'腕舟骨植骨内固定术','operation_note_text':'手术名称：腕舟骨骨不连植骨内固定术。舟骨骨折端植骨，空心钉固定。'}]
        pred=procedure_predictions(rows)[0]
        self.assertEqual(pred['pred_target_disease_procedure_present'],'yes')
        labels=set(pred['pred_procedure_labels'].split('|'))
        self.assertIn('bone_graft',labels)
        self.assertIn('internal_fixation',labels)


if __name__=='__main__':
    unittest.main()
