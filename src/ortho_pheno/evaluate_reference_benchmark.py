#!/usr/bin/env python3
"""Evaluate a frozen physician reference standard against local predictions.

This orchestration layer implements the prespecified hierarchy:
1. disease/anatomy by domain;
2. scaphoid-state binary collapse;
3. target-disease procedure relevance;
4. procedure components conditional on gold relevance;
5. end-to-end procedure components, where relevance errors are penalized.

Inputs and row-level predictions remain local. The script writes aggregate JSON
metrics only; publication of any metric remains subject to privacy/small-cell
review.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import csv
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evaluate_annotations import categorical_metrics, multilabel_metrics

PROCEDURE_LABELS = {
    'hallux_valgus': ['osteotomy','chevron','akin','scarf','fusion','k_wire','resection','soft_tissue'],
    'scaphoid_fracture': ['internal_fixation','bone_graft','reconstruction','fusion','hardware_removal','debridement'],
    'first_cmc_oa': ['trapeziectomy','tendon_procedure','ligament_procedure','arthroplasty','fusion'],
}

SCAPHOID_STATE_BINARY_MAP = {
    'acute_or_new_fracture': 'other_wrist_scaphoid',
    'established_chronic_fracture': 'established_chronic_or_nonunion',
    'established_nonunion': 'established_chronic_or_nonunion',
    'chronic_nonunion_not_distinguishable': 'established_chronic_or_nonunion',
    'insufficient_or_uncertain': None,
}


def read_csv(path: Path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def index(rows, key='study_id'):
    out={}
    for row in rows:
        sid=row[key].strip()
        if sid in out:
            raise ValueError(f'duplicate {key}: {sid}')
        out[sid]=row
    return out


def parse_set(value):
    return {x.strip() for x in (value or '').split('|') if x.strip()}


def join_gold_pred(gold_rows, pred_rows):
    g=index(gold_rows); p=index(pred_rows)
    common=sorted(set(g)&set(p))
    return [(sid,g[sid],p[sid]) for sid in common]


def evaluate_disease_anatomy(gold_rows, pred_rows):
    joined=join_gold_pred(gold_rows,pred_rows)
    out={}
    for domain in ('hallux_valgus','scaphoid_fracture','first_cmc_oa'):
        pairs=[(g['gold_disease_anatomy_label'].strip(),p['pred_disease_anatomy_label'].strip())
               for _,g,p in joined if g['domain']==domain and g['gold_disease_anatomy_label'].strip()]
        if not pairs:
            out[domain]={'status':'no_evaluable_gold'}
            continue
        gold,pred=zip(*pairs)
        out[domain]=categorical_metrics(list(gold),list(pred))
    return out


def evaluate_scaphoid_state(gold_rows,pred_rows):
    joined=join_gold_pred(gold_rows,pred_rows)
    gold=[]; pred=[]; excluded=0
    for _,g,p in joined:
        raw=g['gold_scaphoid_state'].strip()
        if not raw:
            continue
        if raw not in SCAPHOID_STATE_BINARY_MAP:
            raise ValueError(f'unrecognized scaphoid gold state: {raw!r}')
        mapped=SCAPHOID_STATE_BINARY_MAP[raw]
        if mapped is None:
            excluded+=1; continue
        gold.append(mapped); pred.append(p['pred_scaphoid_state_binary'].strip())
    if not gold:
        return {'status':'no_evaluable_gold','excluded_uncertain':excluded}
    m=categorical_metrics(gold,pred,positive_label='established_chronic_or_nonunion')
    m['excluded_uncertain']=excluded
    return m


def evaluate_procedures(gold_rows,pred_rows):
    joined=join_gold_pred(gold_rows,pred_rows)
    out={}
    for domain,labels in PROCEDURE_LABELS.items():
        rows=[(g,p) for _,g,p in joined if g['domain']==domain and g['gold_target_disease_procedure_present'].strip()]
        if not rows:
            out[domain]={'status':'no_evaluable_gold'}
            continue

        # Three-class relevance preserves physician uncertainty and penalizes a
        # yes/no-only baseline when it overcommits on uncertain cases.
        rel_gold=[g['gold_target_disease_procedure_present'].strip() for g,_ in rows]
        rel_pred=[p['pred_target_disease_procedure_present'].strip() for _,p in rows]
        relevance_three_class=categorical_metrics(rel_gold,rel_pred)

        # Binary relevance excludes uncertain gold for interpretable sensitivity/
        # specificity of target-disease procedure detection.
        binary=[(g,p) for g,p in rows if g['gold_target_disease_procedure_present'].strip() in ('yes','no')]
        if binary:
            relevance_binary=categorical_metrics(
                [g['gold_target_disease_procedure_present'].strip() for g,_ in binary],
                [p['pred_target_disease_procedure_present'].strip() for _,p in binary],
                positive_label='yes',
            )
        else:
            relevance_binary={'status':'no_binary_gold'}

        # Conditional component extraction: oracle gold relevance=yes.
        positive=[(g,p) for g,p in rows if g['gold_target_disease_procedure_present'].strip()=='yes']
        if positive:
            conditional=multilabel_metrics(
                [parse_set(g['gold_procedure_labels']) for g,_ in positive],
                [parse_set(p['pred_procedure_labels']) for _,p in positive],
                labels,
            )
        else:
            conditional={'status':'no_gold_positive_procedures'}

        # End-to-end: uncertain relevance excluded. Gold no => empty component
        # set. A false-positive relevance prediction can therefore create FP
        # components, while a false-negative relevance prediction creates FN
        # components on gold-positive records.
        e2e=[]
        for g,p in rows:
            rel=g['gold_target_disease_procedure_present'].strip()
            if rel=='uncertain':
                continue
            gold_set=parse_set(g['gold_procedure_labels']) if rel=='yes' else set()
            pred_set=parse_set(p['pred_procedure_labels']) if p['pred_target_disease_procedure_present'].strip()=='yes' else set()
            e2e.append((gold_set,pred_set))
        end_to_end=multilabel_metrics([x for x,_ in e2e],[y for _,y in e2e],labels) if e2e else {'status':'no_evaluable_gold'}

        out[domain]={
            'relevance_three_class':relevance_three_class,
            'relevance_binary':relevance_binary,
            'component_conditional_on_gold_relevance_yes':conditional,
            'component_end_to_end':end_to_end,
            'n_gold_relevance_uncertain':sum(x=='uncertain' for x in rel_gold),
        }
    return out


def build(gold_dir: Path,pred_dir: Path):
    disease_gold=read_csv(gold_dir/'disease_anatomy_annotation.csv')
    state_gold=read_csv(gold_dir/'scaphoid_state_annotation.csv')
    procedure_gold=read_csv(gold_dir/'procedure_annotation.csv')
    disease_pred=read_csv(pred_dir/'rule_disease_anatomy_predictions.csv')
    state_pred=read_csv(pred_dir/'rule_scaphoid_state_predictions.csv')
    procedure_pred=read_csv(pred_dir/'rule_procedure_predictions.csv')
    return {
        'disease_anatomy':evaluate_disease_anatomy(disease_gold,disease_pred),
        'scaphoid_state_binary':evaluate_scaphoid_state(state_gold,state_pred),
        'procedures':evaluate_procedures(procedure_gold,procedure_pred),
    }


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--gold-dir',required=True)
    ap.add_argument('--pred-dir',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    metrics=build(Path(args.gold_dir),Path(args.pred_dir))
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
