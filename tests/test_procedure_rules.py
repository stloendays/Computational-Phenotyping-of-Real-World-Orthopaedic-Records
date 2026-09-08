import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ortho_pheno.procedure_rules import (
    note_is_domain_concordant, extract_procedure_labels, procedure_body,
)


class ProcedureRuleTests(unittest.TestCase):
    def test_header_diagnosis_does_not_make_unrelated_hallux_operation_relevant(self):
        note = (
            '术前诊断：左足踇趾外翻,右手拇指甲下肿物\n'
            '手术名称：骨骼肌软组织切除术 拔甲\n'
            '手术步骤：右拇指甲床切开并切除肿物。'
        )
        self.assertFalse(note_is_domain_concordant('hallux_valgus', note))
        self.assertEqual(extract_procedure_labels('hallux_valgus', [note]), set())

    def test_hallux_operation_is_concordant(self):
        note = '手术名称：拇外翻矫形术\n第一跖骨Chevron截骨，克氏针固定，关节囊松解。'
        self.assertTrue(note_is_domain_concordant('hallux_valgus', note))
        self.assertEqual(
            extract_procedure_labels('hallux_valgus', [note]),
            {'osteotomy', 'chevron', 'k_wire', 'soft_tissue'},
        )

    def test_unrelated_radius_operation_is_not_scaphoid_procedure(self):
        note = '术前诊断：腕舟骨骨折\n手术名称：右桡骨远端骨折闭合复位钢针内固定术\n桡骨远端复位固定。'
        self.assertFalse(note_is_domain_concordant('scaphoid_fracture', note))
        self.assertEqual(extract_procedure_labels('scaphoid_fracture', [note]), set())

    def test_scaphoid_grafting_labels(self):
        note = '手术名称：腕舟骨骨不连植骨内固定术\n清理舟骨骨折端后植骨并行空心钉内固定。'
        self.assertTrue(note_is_domain_concordant('scaphoid_fracture', note))
        labels = extract_procedure_labels('scaphoid_fracture', [note])
        self.assertIn('bone_graft', labels)
        self.assertIn('internal_fixation', labels)

    def test_procedure_body_removes_preoperative_header(self):
        note = '术前诊断：左足拇外翻\n手术名称：右手拔甲术\n拔除指甲。'
        self.assertNotIn('拇外翻', procedure_body(note))


if __name__ == '__main__':
    unittest.main()
