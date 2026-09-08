import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ortho_pheno.predict_deterministic_baseline import (
    predict_disease_anatomy,
    predict_scaphoid_binary_state,
    predict_procedure_labels,
)


class DeterministicBaselineTests(unittest.TestCase):
    def test_hallux_disease_baseline(self):
        self.assertEqual(
            predict_disease_anatomy('hallux_valgus', '双足拇外翻'),
            'yes',
        )

    def test_scaphoid_foot_not_triggered_by_operation_word(self):
        self.assertEqual(
            predict_disease_anatomy(
                'scaphoid_fracture',
                '左足舟骨病理性骨折，拟行手术治疗',
            ),
            'foot_navicular',
        )

    def test_scaphoid_ambiguous_is_exposed_as_uncertain(self):
        self.assertEqual(
            predict_disease_anatomy('scaphoid_fracture', '右舟骨骨折术后11个月'),
            'uncertain',
        )

    def test_scaphoid_binary_state_uses_clinical_text(self):
        self.assertEqual(
            predict_scaphoid_binary_state('右腕舟骨骨折不连接'),
            'established_chronic_or_nonunion',
        )
        self.assertEqual(
            predict_scaphoid_binary_state('右腕舟骨新鲜骨折'),
            'not_established_chronic_or_nonunion',
        )

    def test_multilabel_hallux_procedure(self):
        labels = predict_procedure_labels(
            'hallux_valgus',
            'Chevron截骨术',
            '克氏针固定，联合关节囊松解及内侧骨赘切除',
        )
        self.assertTrue({'osteotomy', 'chevron', 'k_wire', 'soft_tissue', 'resection'} <= labels)


if __name__ == '__main__':
    unittest.main()
