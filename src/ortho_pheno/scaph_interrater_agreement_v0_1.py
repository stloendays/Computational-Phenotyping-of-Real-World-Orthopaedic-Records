#!/usr/bin/env python3
"""Aggregate inter-rater agreement for the two-stage scaphoid physician review.

This script must be run **before final adjudication is used for manuscript analysis**.
It compares Reviewer-1 and Reviewer-2 labels only on the prespecified double-review
subsets and writes aggregate metrics without study IDs.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import csv
import json
import statistics

from scipy.stats import spearmanr

from evaluate_annotations import categorical_metrics

DURATION_TO_DAYS = {
    'hours': 1 / 24,
    'days': 1,
    'weeks': 7,
    'months': 30.44,
    'years': 365.25,
}

CHRONIC_STATES = {
    'established_chronic_fracture',
    'established_nonunion',
    'chronic_nonunion_not_distinguishable',
}


def read_map(path: Path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    out = {}
    for row in rows:
        sid = row.get('study_id', '').strip()
        if not sid:
            raise ValueError(f'{path}: blank study_id')
        if sid in out:
            raise ValueError(f'{path}: duplicate study_id {sid}')
        out[sid] = row
    return out


def joined(primary, reviewer2):
    ids = sorted(set(primary) & set(reviewer2))
    if set(reviewer2) - set(primary):
        raise ValueError('Reviewer-2 file contains IDs not present in Reviewer-1 file')
    if not ids:
        raise ValueError('no overlapping double-review IDs')
    return ids


def metric_pair(primary, reviewer2, ids, pfield, rfield, label_map=None):
    a = []; b = []
    excluded = 0
    for sid in ids:
        x = primary[sid].get(pfield, '').strip()
        y = reviewer2[sid].get(rfield, '').strip()
        if not x or not y:
            excluded += 1
            continue
        if label_map:
            x = label_map(x)
            y = label_map(y)
        a.append(x); b.append(y)
    if not a:
        return {'n': 0, 'excluded_blank': excluded, 'accuracy': None, 'cohen_kappa': None}
    result = categorical_metrics(a, b)
    return {
        'n': len(a),
        'excluded_blank': excluded,
        'raw_agreement': result['accuracy'],
        'cohen_kappa': result['cohen_kappa'],
        'labels': sorted(set(a) | set(b)),
    }


def collapsed_state(value):
    if value in CHRONIC_STATES:
        return 'established_chronic_nonunion'
    if value == 'acute_or_new_fracture':
        return 'acute_new'
    return 'uncertain'


def duration_days(row, prefix):
    if row.get(f'{prefix}relevant_duration_present', '').strip() != 'yes':
        return None
    try:
        value = float(row.get(f'{prefix}relevant_duration_value', '').strip())
    except ValueError:
        return None
    unit = row.get(f'{prefix}relevant_duration_unit', '').strip()
    factor = DURATION_TO_DAYS.get(unit)
    if factor is None or value <= 0:
        return None
    return value * factor


def duration_numeric_agreement(primary, reviewer2, ids):
    pairs = []
    for sid in ids:
        a = duration_days(primary[sid], 'gold_')
        b = duration_days(reviewer2[sid], 'reviewer2_gold_')
        if a is not None and b is not None:
            pairs.append((a, b))
    if not pairs:
        return {'n': 0, 'median_absolute_difference_days': None, 'spearman_rho': None, 'spearman_p': None}
    absdiff = [abs(a - b) for a, b in pairs]
    if len(pairs) >= 3 and len(set(a for a, _ in pairs)) > 1 and len(set(b for _, b in pairs)) > 1:
        rho = spearmanr([a for a, _ in pairs], [b for _, b in pairs])
        r = float(rho.statistic); p = float(rho.pvalue)
    else:
        r = p = None
    return {
        'n': len(pairs),
        'median_absolute_difference_days': statistics.median(absdiff),
        'max_absolute_difference_days': max(absdiff),
        'spearman_rho': r,
        'spearman_p': p,
    }


def procedure_component_metric(primary, reviewer2, ids, label):
    use = []
    for sid in ids:
        if (
            primary[sid].get('gold_target_disease_procedure_present', '').strip() == 'yes'
            and reviewer2[sid].get('reviewer2_gold_target_disease_procedure_present', '').strip() == 'yes'
        ):
            use.append(sid)
    return metric_pair(
        primary, reviewer2, use,
        f'gold_{label}', f'reviewer2_gold_{label}'
    ) if use else {'n': 0, 'raw_agreement': None, 'cohen_kappa': None}


def build(review_dir: Path):
    anatomy1 = read_map(review_dir / 'scaphoid_anatomy_review.csv')
    anatomy2 = read_map(review_dir / 'scaphoid_anatomy_review_reviewer2.csv')
    state1 = read_map(review_dir / 'scaphoid_state_review.csv')
    state2 = read_map(review_dir / 'scaphoid_state_review_reviewer2.csv')
    proc1 = read_map(review_dir / 'scaphoid_procedure_review.csv')
    proc2 = read_map(review_dir / 'scaphoid_procedure_review_reviewer2.csv')

    anatomy_ids = joined(anatomy1, anatomy2)
    state_ids = joined(state1, state2)
    proc_ids = joined(proc1, proc2)

    result = {
        'anatomy': metric_pair(
            anatomy1, anatomy2, anatomy_ids,
            'gold_anatomy_label', 'reviewer2_gold_anatomy_label'
        ),
        'state_full': metric_pair(
            state1, state2, state_ids,
            'gold_scaphoid_state', 'reviewer2_gold_scaphoid_state'
        ),
        'state_collapsed_for_primary_analysis': metric_pair(
            state1, state2, state_ids,
            'gold_scaphoid_state', 'reviewer2_gold_scaphoid_state', collapsed_state
        ),
        'duration_present': metric_pair(
            state1, state2, state_ids,
            'gold_relevant_duration_present', 'reviewer2_gold_relevant_duration_present'
        ),
        'duration_basis_among_both_present': None,
        'duration_numeric_among_both_present': duration_numeric_agreement(state1, state2, state_ids),
        'procedure_relevance': metric_pair(
            proc1, proc2, proc_ids,
            'gold_target_disease_procedure_present', 'reviewer2_gold_target_disease_procedure_present'
        ),
        'procedure_components_among_both_relevant': {
            label: procedure_component_metric(proc1, proc2, proc_ids, label)
            for label in ('internal_fixation', 'bone_graft', 'reconstruction', 'fusion')
        },
    }

    both_duration = [
        sid for sid in state_ids
        if state1[sid].get('gold_relevant_duration_present', '').strip() == 'yes'
        and state2[sid].get('reviewer2_gold_relevant_duration_present', '').strip() == 'yes'
    ]
    if both_duration:
        result['duration_basis_among_both_present'] = metric_pair(
            state1, state2, both_duration,
            'gold_duration_basis', 'reviewer2_gold_duration_basis'
        )
    else:
        result['duration_basis_among_both_present'] = {'n': 0, 'raw_agreement': None, 'cohen_kappa': None}

    result['double_review_counts'] = {
        'anatomy': len(anatomy_ids),
        'state_duration': len(state_ids),
        'procedure': len(proc_ids),
    }
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--review-dir', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    result = build(Path(args.review_dir))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'wrote aggregate inter-rater metrics: {out}')


if __name__ == '__main__':
    main()
