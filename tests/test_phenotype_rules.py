import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ortho_pheno.rules import (
    is_hallux_valgus, is_first_cmc_oa, is_wrist_scaphoid,
    is_established_scaphoid_chronic_nonunion, has_bilateral_mention,
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
        self.assertTrue(is_wrist_scaphoid('舟骨腰部骨折，腕部疼痛'))
        self.assertFalse(is_wrist_scaphoid('左足舟骨骨折，足背肿痛'))

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
