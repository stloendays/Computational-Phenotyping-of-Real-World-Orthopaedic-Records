import csv
import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ortho_pheno.hallux_baseline_rules import (
    predict_laterality,predict_bilateral_disease_mention,predict_pain,predict_functional_limitation,
)
from ortho_pheno.evaluate_hallux_baseline import evaluate


class HalluxBaselineTests(unittest.TestCase):
    def test_bilateral_and_laterality(self):
        text='双足拇外翻，双侧第一跖趾关节内侧突出。'
        self.assertEqual(predict_laterality(text),'bilateral')
        self.assertEqual(predict_bilateral_disease_mention(text),'present')

    def test_non_disease_double_word_is_not_bilateral(self):
        self.assertEqual(predict_bilateral_disease_mention('双氧水冲洗切口'),'undocumented')

    def test_missing_is_not_negative(self):
        self.assertEqual(predict_pain('双足拇外翻'),'undocumented')
        self.assertEqual(predict_functional_limitation('双足拇外翻'),'undocumented')

    def test_negation_precedes_positive_keyword(self):
        self.assertEqual(predict_pain('目前无明显疼痛'),'absent')
        self.assertEqual(predict_functional_limitation('活动正常，无活动受限'),'absent')

    def test_hallux_baseline_evaluation(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); g=root/'g.csv'; p=root/'p.csv'
            fields=['study_id','domain','gold_disease_anatomy_label','gold_hallux_laterality',
                    'gold_hallux_bilateral_disease_mention','gold_hallux_pain','gold_hallux_functional_limitation']
            with g.open('w',encoding='utf-8-sig',newline='') as f:
                w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
                w.writerow({'study_id':'H1','domain':'hallux_valgus','gold_disease_anatomy_label':'yes',
                            'gold_hallux_laterality':'bilateral','gold_hallux_bilateral_disease_mention':'present',
                            'gold_hallux_pain':'present','gold_hallux_functional_limitation':'undocumented'})
                w.writerow({'study_id':'H2','domain':'hallux_valgus','gold_disease_anatomy_label':'yes',
                            'gold_hallux_laterality':'left','gold_hallux_bilateral_disease_mention':'undocumented',
                            'gold_hallux_pain':'absent','gold_hallux_functional_limitation':'present'})
            pfields=['study_id','domain','pred_hallux_laterality','pred_hallux_bilateral_disease_mention','pred_hallux_pain','pred_hallux_functional_limitation']
            with p.open('w',encoding='utf-8-sig',newline='') as f:
                w=csv.DictWriter(f,fieldnames=pfields); w.writeheader()
                w.writerow({'study_id':'H1','domain':'hallux_valgus','pred_hallux_laterality':'bilateral','pred_hallux_bilateral_disease_mention':'present','pred_hallux_pain':'present','pred_hallux_functional_limitation':'undocumented'})
                w.writerow({'study_id':'H2','domain':'hallux_valgus','pred_hallux_laterality':'right','pred_hallux_bilateral_disease_mention':'undocumented','pred_hallux_pain':'absent','pred_hallux_functional_limitation':'present'})
            m=evaluate(g,p)
            self.assertEqual(m['fields']['bilateral_disease_mention']['accuracy'],1.0)
            self.assertEqual(m['fields']['laterality']['accuracy'],0.5)


if __name__=='__main__':
    unittest.main()
