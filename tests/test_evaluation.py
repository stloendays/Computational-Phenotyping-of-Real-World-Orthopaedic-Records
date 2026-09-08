import csv
import sys
import tempfile
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ortho_pheno.evaluate_annotations import (
    categorical_metrics,
    multilabel_metrics,
    cohen_kappa,
    load_joined,
)


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

    def test_separate_columns_and_prespecified_gold_mapping(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            gold_path = root / 'gold.csv'
            pred_path = root / 'pred.csv'

            with open(gold_path, 'w', encoding='utf-8', newline='') as f:
                w = csv.DictWriter(f, fieldnames=['study_id', 'gold_state'])
                w.writeheader()
                w.writerows([
                    {'study_id': 'A', 'gold_state': 'established_nonunion'},
                    {'study_id': 'B', 'gold_state': 'acute_or_new_fracture'},
                    {'study_id': 'C', 'gold_state': 'insufficient_or_uncertain'},
                    {'study_id': 'D', 'gold_state': ''},
                ])

            with open(pred_path, 'w', encoding='utf-8', newline='') as f:
                w = csv.DictWriter(f, fieldnames=['study_id', 'pred_state'])
                w.writeheader()
                w.writerows([
                    {'study_id': 'A', 'pred_state': 'established_chronic_or_nonunion'},
                    {'study_id': 'B', 'pred_state': 'not_established_chronic_or_nonunion'},
                    {'study_id': 'C', 'pred_state': 'not_established_chronic_or_nonunion'},
                    {'study_id': 'D', 'pred_state': 'not_established_chronic_or_nonunion'},
                ])

            joined = load_joined(
                gold_path,
                pred_path,
                'study_id',
                'gold_state',
                'pred_state',
                {
                    'established_nonunion': 'established_chronic_or_nonunion',
                    'acute_or_new_fracture': 'not_established_chronic_or_nonunion',
                    'insufficient_or_uncertain': None,
                },
            )
            self.assertEqual(joined['ids'], ['A', 'B'])
            self.assertEqual(len(joined['blank_gold_ids_excluded']), 1)
            self.assertEqual(len(joined['mapped_out_gold_ids_excluded']), 1)


if __name__ == '__main__':
    unittest.main()
