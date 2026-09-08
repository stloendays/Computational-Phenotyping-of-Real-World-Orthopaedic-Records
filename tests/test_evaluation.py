import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ortho_pheno.evaluate_annotations import categorical_metrics, multilabel_metrics, cohen_kappa


class EvaluationTests(unittest.TestCase):
    def test_binary_metrics(self):
        gold = ['yes', 'yes', 'no', 'no']
        pred = ['yes', 'no', 'no', 'no']
        m = categorical_metrics(gold, pred, positive_label='yes')
        self.assertAlmostEqual(m['accuracy'], 0.75)
        self.assertAlmostEqual(m['sensitivity'], 0.5)
        self.assertAlmostEqual(m['specificity'], 1.0)
        self.assertAlmostEqual(m['ppv'], 1.0)
        self.assertAlmostEqual(m['f1'], 2 / 3)

    def test_kappa_perfect(self):
        x = ['a', 'b', 'a', 'c']
        self.assertAlmostEqual(cohen_kappa(x, x), 1.0)

    def test_multilabel_metrics(self):
        gold = [{'osteotomy', 'k_wire'}, {'fusion'}, set()]
        pred = [{'osteotomy', 'k_wire'}, {'fusion', 'k_wire'}, set()]
        m = multilabel_metrics(gold, pred, ['osteotomy', 'k_wire', 'fusion'])
        self.assertAlmostEqual(m['exact_set_match'], 2 / 3)
        self.assertAlmostEqual(m['micro_precision'], 0.75)
        self.assertAlmostEqual(m['micro_recall'], 1.0)
        self.assertAlmostEqual(m['micro_f1'], 6 / 7)


if __name__ == '__main__':
    unittest.main()
