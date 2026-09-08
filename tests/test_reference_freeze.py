import csv
import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ortho_pheno.freeze_reference_standard import build_manifest, verify_manifest


def write_csv(path, fields, row):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerow(row)


class ReferenceFreezeTests(unittest.TestCase):
    def make_valid_gold(self,root):
        write_csv(root/'disease_anatomy_annotation.csv',
                  ['study_id','domain','gold_disease_anatomy_label'],
                  {'study_id':'H1','domain':'hallux_valgus','gold_disease_anatomy_label':'yes'})
        write_csv(root/'scaphoid_state_annotation.csv',
                  ['study_id','gold_scaphoid_state'],
                  {'study_id':'S1','gold_scaphoid_state':'established_nonunion'})
        write_csv(root/'procedure_annotation.csv',
                  ['study_id','domain','gold_target_disease_procedure_present','gold_procedure_labels'],
                  {'study_id':'H1','domain':'hallux_valgus','gold_target_disease_procedure_present':'yes','gold_procedure_labels':'osteotomy|k_wire'})

    def test_build_and_verify_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); self.make_valid_gold(root)
            manifest=build_manifest(root)
            self.assertEqual(manifest['reference_standard_status'],'frozen')
            out=root/'freeze.json'
            import json
            out.write_text(json.dumps(manifest),encoding='utf-8')
            self.assertTrue(verify_manifest(root,out))

    def test_mutation_breaks_hash_verification(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); self.make_valid_gold(root)
            manifest=build_manifest(root)
            import json
            out=root/'freeze.json'; out.write_text(json.dumps(manifest),encoding='utf-8')
            p=root/'scaphoid_state_annotation.csv'
            p.write_text(p.read_text(encoding='utf-8-sig')+'\n',encoding='utf-8-sig')
            with self.assertRaises(ValueError):
                verify_manifest(root,out)

    def test_relevance_no_cannot_have_target_labels(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); self.make_valid_gold(root)
            write_csv(root/'procedure_annotation.csv',
                      ['study_id','domain','gold_target_disease_procedure_present','gold_procedure_labels'],
                      {'study_id':'H1','domain':'hallux_valgus','gold_target_disease_procedure_present':'no','gold_procedure_labels':'osteotomy'})
            with self.assertRaises(ValueError):
                build_manifest(root)


if __name__=='__main__':
    unittest.main()
