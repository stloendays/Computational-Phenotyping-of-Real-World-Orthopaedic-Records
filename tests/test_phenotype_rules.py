import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ortho_pheno.rules import (
    is_hallux_valgus, is_first_cmc_oa, is_wrist_scaphoid,
    scaphoid_anatomy_class, is_established_scaphoid_chronic_nonunion,
    has_bilateral_mention,
)


class PhenotypeRuleTests(unittest.TestCase):
    def test_hallux_variant(self):
        self.assertTrue(is_hallux_valgus('诊断：双足拇外翻'))

    def test_first_cmc_specificity(self):
        self.assertTrue(is_first_cmc_oa('右拇指第一腕掌关节骨关节炎'))
        self.assertFalse(is_first_cmc_oa('右桡腕关节炎'))
        self.assertFalse(is_first_cmc_oa('腕关节滑膜炎'))

    def test_scaphoid_anatomical_disambiguation(self):
        self.assertTrue(is_wrist_scaphoid('右腕舟骨腰部骨折'))
        self.assertTrue(is_wrist_scaphoid('左腕桡骨、舟骨骨折术后'))
        self.assertTrue(is_wrist_scaphoid('左手舟骨、大多角骨骨折'))
        self.assertTrue(is_wrist_scaphoid('舟骨骨折不连接；左腕疼痛'))
        self.assertFalse(is_wrist_scaphoid('左足舟骨骨折，足背肿痛'))

    def test_generic_hand_words_do_not_create_wrist_anatomy(self):
        self.assertEqual(
            scaphoid_anatomy_class('左足舟骨病理性骨折，手术名称：舟骨切除术'),
            'foot_navicular'
        )
        self.assertEqual(
            scaphoid_anatomy_class('左足舟骨骨折，术中手法牵拉复位舟骨'),
            'foot_navicular'
        )

    def test_genuinely_multisite_record_retains_explicit_wrist_scaphoid(self):
        self.assertEqual(
            scaphoid_anatomy_class('足舟骨骨折；另有左手舟骨、大多角骨骨折'),
            'wrist_scaphoid'
        )

    def test_unsupported_generic_scaphoid_is_ambiguous(self):
        self.assertEqual(scaphoid_anatomy_class('右舟骨骨折术后11个月'), 'ambiguous')

    def test_scaphoid_case_source_scope(self):
        clinical = '诊断：右腕舟骨新鲜骨折'
        operative = '术中见骨不连，行植骨内固定'
        self.assertFalse(is_established_scaphoid_chronic_nonunion(clinical))
        self.assertTrue(is_established_scaphoid_chronic_nonunion(operative))
        # Pipeline contract: only `clinical` is allowed to assign case status.

    def test_bilateral_is_specific(self):
        self.assertTrue(has_bilateral_mention('双足拇外翻'))
        self.assertFalse(has_bilateral_mention('双氧水冲洗切口'))


if __name__ == '__main__':
    unittest.main()
