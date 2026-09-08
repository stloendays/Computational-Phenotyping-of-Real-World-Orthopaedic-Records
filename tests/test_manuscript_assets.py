import csv
import shutil
import sys
import tempfile
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / 'src'))
from ortho_pheno.build_manuscript_assets_v0_1 import build


class ManuscriptAssetTests(unittest.TestCase):
    def test_pre_gold_assets_regenerate_from_public_aggregates(self):
        required = [
            'cohort_overview.csv',
            'source_duplication_audit.csv',
            'scaphoid_anatomy_audit.csv',
            'scaphoid_rule_version_transition.csv',
            'procedure_note_relevance_audit.csv',
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            agg = root / 'data' / 'aggregate'
            agg.mkdir(parents=True)
            for name in required:
                shutil.copy2(REPO_ROOT / 'data' / 'aggregate' / name, agg / name)

            build(root)

            fig1 = (root / 'figures/pre_gold/Figure1_validation_first_framework.svg').read_text(encoding='utf-8')
            fig2 = (root / 'figures/pre_gold/Figure2_cohort_reconstruction.svg').read_text(encoding='utf-8')
            fig3 = (root / 'figures/pre_gold/Figure3_procedure_attribution.svg').read_text(encoding='utf-8')

            self.assertIn('18 raw exports', fig1)
            self.assertIn('SHA-256 frozen before gold', fig1)
            self.assertIn('68/88 (77.3%)', fig2)
            self.assertIn('Removed as foot navicular', fig2)
            self.assertIn('4 episodes', fig2)
            self.assertIn('New wrist additions relative to the superseded heuristic: 0', fig2)
            self.assertIn('module 114', fig3)
            self.assertIn('target-disease 113', fig3)
            self.assertIn('module 31', fig3)
            self.assertIn('target-disease 28', fig3)

            table = root / 'results/tables/TABLE1_SOURCE_ARCHITECTURE_V0_1.csv'
            with table.open(encoding='utf-8-sig', newline='') as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 3)
            by_domain = {r['domain']: r for r in rows}
            self.assertEqual(by_domain['Hallux valgus']['deterministic_strict_phenotype'], '193')
            self.assertEqual(by_domain['Scaphoid retrieval']['deterministic_strict_phenotype'], '68')
            self.assertEqual(by_domain['First-CMC OA']['deterministic_strict_phenotype'], '28')
            self.assertEqual(by_domain['Scaphoid retrieval']['disease_concordant_procedure_note_n'], '28')


if __name__ == '__main__':
    unittest.main()
