#!/usr/bin/env python3
"""Calculate scaphoid physician inter-rater agreement before adjudication.

Primary and Reviewer-2 files remain local. The script writes aggregate agreement
metrics plus a PRIVATE disagreement list containing study IDs for adjudication.

Agreement is hierarchical:

- duration presence is scored on all double-reviewed state rows;
- duration unit/basis/value are scored only when both reviewers mark duration=yes;
- procedure relevance is scored on all double-reviewed procedure rows;
- procedure components are scored only when both reviewers mark relevance=yes.

This prevents protocol-correct blank fields from being misclassified as missing
labels.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import argparse
import csv
import json
import math

UNIT_TO_DAYS = {
    'hours':1/24,
    'days':1.0,
    'weeks':7.0,
    'months':30.44,
    'years':365.25,
}


def read_rows(path: Path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def index(rows):
    out = {}
    for row in rows:
        sid = row.get('study_id','').strip()
        if not sid:
            raise ValueError('blank study_id')
        if sid in out:
            raise ValueError(f'duplicate study_id: {sid}')
        out[sid] = row
    return out


def cohen_kappa(a, b):
    if len(a) != len(b):
        raise ValueError('label arrays must have equal length')
    if not a:
        return None
    n = len(a)
    observed = sum(x == y for x,y in zip(a,b)) / n
    ca = Counter(a); cb = Counter(b)
    labels = set(ca) | set(cb)
    expected = sum((ca[label]/n) * (cb[label]/n) for label in labels)
    if math.isclose(1.0 - expected, 0.0):
        return 1.0 if math.isclose(observed, 1.0) else None
    return (observed - expected) / (1.0 - expected)


def categorical_agreement(primary_rows, reviewer2_rows, primary_field, reviewer2_field, layer, disagreement_rows, include=None):
    p = index(primary_rows); r = index(reviewer2_rows)
    if not set(r) <= set(p):
        raise ValueError(f'{layer}: reviewer2 IDs are not a subset of primary IDs')
    a=[]; b=[]
    for sid in sorted(r):
        if include is not None and not include(p[sid], r[sid]):
            continue
        x=p[sid].get(primary_field,'').strip(); y=r[sid].get(reviewer2_field,'').strip()
        if not x or not y:
            raise ValueError(f'{layer}: incomplete double-review label for {sid}')
        a.append(x); b.append(y)
        if x != y:
            disagreement_rows.append({
                'study_id':sid,'layer':layer,'field':primary_field,
                'reviewer1_value':x,'reviewer2_value':y,
            })
    return {
        'n':len(a),
        'exact_agreement':sum(x==y for x,y in zip(a,b))/len(a) if a else None,
        'cohen_kappa':cohen_kappa(a,b),
    }


def both_duration_yes(primary_row, reviewer2_row):
    return (
        primary_row.get('gold_relevant_duration_present','').strip() == 'yes'
        and reviewer2_row.get('reviewer2_gold_relevant_duration_present','').strip() == 'yes'
    )


def both_procedure_relevant(primary_row, reviewer2_row):
    return (
        primary_row.get('gold_target_disease_procedure_present','').strip() == 'yes'
        and reviewer2_row.get('reviewer2_gold_target_disease_procedure_present','').strip() == 'yes'
    )


def duration_numeric_agreement(primary_rows, reviewer2_rows, disagreement_rows):
    p=index(primary_rows); r=index(reviewer2_rows)
    pairs=[]
    for sid in sorted(r):
        if not both_duration_yes(p[sid],r[sid]):
            continue
        try:
            pv=float(p[sid].get('gold_relevant_duration_value',''))
            rv=float(r[sid].get('reviewer2_gold_relevant_duration_value',''))
        except Exception as exc:
            raise ValueError(f'duration numeric agreement: invalid numeric duration for {sid}') from exc
        pu=p[sid].get('gold_relevant_duration_unit','').strip()
        ru=r[sid].get('reviewer2_gold_relevant_duration_unit','').strip()
        if pu not in UNIT_TO_DAYS or ru not in UNIT_TO_DAYS:
            raise ValueError(f'duration numeric agreement: invalid duration unit for {sid}')
        pdays=pv*UNIT_TO_DAYS[pu]
        rdays=rv*UNIT_TO_DAYS[ru]
        pairs.append((pdays,rdays))
        if not math.isclose(pdays,rdays,rel_tol=0.01,abs_tol=0.5):
            disagreement_rows.append({
                'study_id':sid,'layer':'state_duration','field':'duration_normalized_days',
                'reviewer1_value':f'{pdays:.6g}','reviewer2_value':f'{rdays:.6g}',
            })
    if not pairs:
        return {'n_both_duration_yes':0,'normalized_numeric_agreement':None,'median_absolute_difference_days':None}
    diffs=sorted(abs(a-b) for a,b in pairs)
    mid=len(diffs)//2
    median=diffs[mid] if len(diffs)%2 else (diffs[mid-1]+diffs[mid])/2
    return {
        'n_both_duration_yes':len(pairs),
        'normalized_numeric_agreement':sum(math.isclose(a,b,rel_tol=0.01,abs_tol=0.5) for a,b in pairs)/len(pairs),
        'median_absolute_difference_days':median,
    }


def build(review_dir: Path):
    anatomy=read_rows(review_dir/'scaphoid_anatomy_review.csv')
    anatomy2=read_rows(review_dir/'scaphoid_anatomy_review_reviewer2.csv')
    state=read_rows(review_dir/'scaphoid_state_review.csv')
    state2=read_rows(review_dir/'scaphoid_state_review_reviewer2.csv')
    procedure=read_rows(review_dir/'scaphoid_procedure_review.csv')
    procedure2=read_rows(review_dir/'scaphoid_procedure_review_reviewer2.csv')

    disagreements=[]
    metrics={
        'anatomy':categorical_agreement(anatomy,anatomy2,'gold_anatomy_label','reviewer2_gold_anatomy_label','anatomy',disagreements),
        'scaphoid_state':categorical_agreement(state,state2,'gold_scaphoid_state','reviewer2_gold_scaphoid_state','state',disagreements),
        'duration_present':categorical_agreement(state,state2,'gold_relevant_duration_present','reviewer2_gold_relevant_duration_present','duration_present',disagreements),
        'duration_unit_when_both_present':categorical_agreement(state,state2,'gold_relevant_duration_unit','reviewer2_gold_relevant_duration_unit','duration_unit',disagreements,include=both_duration_yes),
        'duration_basis_when_both_present':categorical_agreement(state,state2,'gold_duration_basis','reviewer2_gold_duration_basis','duration_basis',disagreements,include=both_duration_yes),
        'procedure_relevance':categorical_agreement(procedure,procedure2,'gold_target_disease_procedure_present','reviewer2_gold_target_disease_procedure_present','procedure_relevance',disagreements),
        'internal_fixation_when_both_relevant':categorical_agreement(procedure,procedure2,'gold_internal_fixation','reviewer2_gold_internal_fixation','internal_fixation',disagreements,include=both_procedure_relevant),
        'bone_graft_when_both_relevant':categorical_agreement(procedure,procedure2,'gold_bone_graft','reviewer2_gold_bone_graft','bone_graft',disagreements,include=both_procedure_relevant),
        'reconstruction_when_both_relevant':categorical_agreement(procedure,procedure2,'gold_reconstruction','reviewer2_gold_reconstruction','reconstruction',disagreements,include=both_procedure_relevant),
        'fusion_when_both_relevant':categorical_agreement(procedure,procedure2,'gold_fusion','reviewer2_gold_fusion','fusion',disagreements,include=both_procedure_relevant),
    }
    metrics['duration_numeric_normalized'] = duration_numeric_agreement(state,state2,disagreements)
    metrics['total_field_disagreements'] = len(disagreements)
    return metrics, disagreements


def write_disagreements(path: Path, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    fields=['study_id','layer','field','reviewer1_value','reviewer2_value']
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--review-dir',required=True)
    ap.add_argument('--aggregate-output',required=True)
    ap.add_argument('--private-disagreements',required=True)
    args=ap.parse_args()
    metrics,disagreements=build(Path(args.review_dir))
    out=Path(args.aggregate_output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    write_disagreements(Path(args.private_disagreements),disagreements)
    print(f'aggregate agreement: {out}')
    print(f'private disagreement list: {args.private_disagreements}')
