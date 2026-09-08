import sys
import tempfile
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src' / 'ortho_pheno'))
from build_scaph_final_figures_v0_1 import figure1_cohort_flow, figure2_composition, figure3_duration


class ScaphoidFinalFigureTests(unittest.TestCase):
    def test_journal_figures_are_valid_svg_and_result_focused(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            counts = {
                'broad': 88, 'wrist': 70, 'foot': 12, 'other_uncertain_anatomy': 6,
                'state': {'chronic': 24, 'acute': 38, 'other': 8},
                'detailed': 32, 'relevant': 29,
                'analytic': {'chronic': 15, 'acute': 10},
            }
            p1 = out/'f1.svg'
            figure1_cohort_flow(counts, p1)

            binary = lambda cy, cn, ay, an, orv, lo, hi, p: {
                'table': {'chronic_yes':cy,'chronic_no':cn,'acute_yes':ay,'acute_no':an},
                'chronic_evaluable': cy+cn,
                'acute_evaluable': ay+an,
                'odds_ratio_conditional': orv,
                'ci95_low': lo,
                'ci95_high': hi,
                'fisher_two_sided_p': p,
            }
            result = {
                'key_contrast_internal_fixation': binary(14,1,9,1,1.5,0.08,35.0,1.0),
                'primary_bone_graft': binary(8,7,1,9,7.8,0.8,75.0,0.04),
            }
            p2 = out/'f2.svg'
            figure2_composition(result, p2)

            p3 = out/'f3.svg'
            figure3_duration({'yes':[180,365,730], 'no':[7,15,30]}, p3)

            for path in (p1,p2,p3):
                ET.parse(path)
                text = path.read_text(encoding='utf-8')
                self.assertNotIn('PUBLIC', text)
                self.assertNotIn('PRIVATE ZONE', text)
                self.assertNotIn('validation-first', text.lower())

            self.assertIn('Physician-confirmed wrist scaphoid', p1.read_text(encoding='utf-8'))
            self.assertIn('Bone-graft augmentation', p2.read_text(encoding='utf-8'))
            self.assertIn('Bone graft present', p3.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
