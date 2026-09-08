"""Evaluate hallux-valgus baseline phenotypes on the frozen physician labels."""
from __future__ import annotations

from pathlib import Path
import csv
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evaluate_annotations import categorical_metrics

FIELDS = {
    'laterality': ('gold_hallux_laterality','pred_hallux_laterality'),
    'bilateral_disease_mention': ('gold_hallux_bilateral_disease_mention','pred_hallux_bilateral_disease_mention'),
    'pain': ('gold_hallux_pain','pred_hallux_pain'),
    'functional_limitation': ('gold_hallux_functional_limitation','pred_hallux_functional_limitation'),
}


def read_csv(path: Path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))


def evaluate(gold_path: Path,pred_path: Path):
    gold={r['study_id']:r for r in read_csv(gold_path) if r.get('domain')=='hallux_valgus' and r.get('gold_disease_anatomy_label','').strip()=='yes'}
    pred={r['study_id']:r for r in read_csv(pred_path) if r.get('domain')=='hallux_valgus'}
    common=sorted(set(gold)&set(pred))
    out={'n_confirmed_hallux_with_predictions':len(common),'fields':{}}
    for name,(gcol,pcol) in FIELDS.items():
        pairs=[(gold[sid].get(gcol,'').strip(),pred[sid].get(pcol,'').strip()) for sid in common]
        pairs=[x for x in pairs if x[0]]
        if not pairs:
            out['fields'][name]={'status':'no_evaluable_gold'}
            continue
        g,p=zip(*pairs)
        m=categorical_metrics(list(g),list(p))
        if name=='bilateral_disease_mention' and 'present' in set(g):
            # A secondary clinically interpretable binary view groups all
            # non-present gold states together only for the current "mention"
            # analysis; the full categorical metrics remain primary.
            gb=['present' if x=='present' else 'not_present' for x in g]
            pb=['present' if x=='present' else 'not_present' for x in p]
            m['binary_present_vs_not_present']=categorical_metrics(gb,pb,positive_label='present')
        out['fields'][name]=m
    return out
