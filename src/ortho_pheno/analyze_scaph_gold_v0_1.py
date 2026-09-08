#!/usr/bin/env python3
"""Run the prespecified post-Gold analysis for the focused scaphoid manuscript.

The script operates only after the two-stage physician reference standard is
complete. It validates the final Gold population, reconstructs the physician-defined
acute/new and established chronic/nonunion operative groups, and calculates the
frozen primary/secondary analyses.

Outputs
-------
* private JSON: exact counts, effect estimates, influence analyses, duration data
  summaries. This file is for the authorized manuscript environment and must not
  be committed to the public repository.
* public CSV: privacy-preserving aggregate summaries with small cells suppressed.

No raw free text, patient identifiers, admission identifiers, or study IDs are
written to either output.
"""
from __future__ import annotations

from pathlib import Path
from collections import defaultdict
import argparse
import csv
import json
import math
import statistics

from scipy.stats import fisher_exact, mannwhitneyu
from scipy.stats.contingency import odds_ratio as scipy_odds_ratio

from build_safe_release import read_xlsx, norm_id
from freeze_scaph_reference_v0_1 import build_final_manifest
from make_scaph_physician_packet_v0_1 import load_salt, make_study_id

BASIC_FILE = '2015-2025舟骨骨折患者基本信息和诊断信息.xlsx'

CHRONIC_STATES = {
    'established_chronic_fracture',
    'established_nonunion',
    'chronic_nonunion_not_distinguishable',
}
ACUTE_STATE = 'acute_or_new_fracture'
UNCERTAIN_STATE = 'insufficient_or_uncertain'
BINARY = {'yes', 'no'}
DURATION_TO_DAYS = {
    'hours': 1 / 24,
    'days': 1,
    'weeks': 7,
    'months': 30.44,
    'years': 365.25,
}


def read_rows(path: Path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def qtile(values, p):
    xs = sorted(float(x) for x in values)
    if not xs:
        return None
    pos = (len(xs) - 1) * p
    lo = math.floor(pos); hi = math.ceil(pos)
    if lo == hi:
        return xs[lo]
    return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)


def numeric_summary(values):
    xs = [float(x) for x in values if x is not None]
    if not xs:
        return {'n': 0, 'median': None, 'q1': None, 'q3': None, 'min': None, 'max': None}
    return {
        'n': len(xs),
        'median': statistics.median(xs),
        'q1': qtile(xs, 0.25),
        'q3': qtile(xs, 0.75),
        'min': min(xs),
        'max': max(xs),
    }


def safe_mannwhitney(x, y):
    x = [float(v) for v in x]
    y = [float(v) for v in y]
    if not x or not y:
        return {'u': None, 'p_value': None}
    result = mannwhitneyu(x, y, alternative='two-sided', method='auto')
    return {'u': float(result.statistic), 'p_value': float(result.pvalue)}


def exact_binary_analysis(group1_values, group2_values):
    """Analyze yes/no labels; uncertain/missing labels are excluded explicitly."""
    g1 = [v for v in group1_values if v in BINARY]
    g2 = [v for v in group2_values if v in BINARY]
    a = sum(v == 'yes' for v in g1)
    b = sum(v == 'no' for v in g1)
    c = sum(v == 'yes' for v in g2)
    d = sum(v == 'no' for v in g2)
    if not g1 or not g2:
        return {
            'table': {'chronic_yes': a, 'chronic_no': b, 'acute_yes': c, 'acute_no': d},
            'chronic_evaluable': len(g1), 'acute_evaluable': len(g2),
            'odds_ratio_conditional': None, 'ci95_low': None, 'ci95_high': None,
            'fisher_two_sided_p': None,
        }
    table = [[a, b], [c, d]]
    fisher = fisher_exact(table, alternative='two-sided')
    conditional = scipy_odds_ratio(table, kind='conditional')
    ci = conditional.confidence_interval(confidence_level=0.95)
    return {
        'table': {'chronic_yes': a, 'chronic_no': b, 'acute_yes': c, 'acute_no': d},
        'chronic_evaluable': len(g1),
        'acute_evaluable': len(g2),
        'chronic_uncertain_or_missing': len(group1_values) - len(g1),
        'acute_uncertain_or_missing': len(group2_values) - len(g2),
        'odds_ratio_conditional': float(conditional.statistic),
        'ci95_low': float(ci.low),
        'ci95_high': float(ci.high),
        'fisher_two_sided_p': float(fisher.pvalue),
    }


def state_group(state):
    if state in CHRONIC_STATES:
        return 'chronic_nonunion'
    if state == ACUTE_STATE:
        return 'acute_new'
    return None


def augmentation_label(row):
    values = [row.get('gold_bone_graft', ''), row.get('gold_reconstruction', ''), row.get('gold_fusion', '')]
    if 'yes' in values:
        return 'yes'
    if all(v == 'no' for v in values):
        return 'no'
    return 'uncertain'


def component_count(row):
    values = [
        row.get('gold_internal_fixation', ''),
        row.get('gold_bone_graft', ''),
        row.get('gold_reconstruction', ''),
        row.get('gold_fusion', ''),
    ]
    if not all(v in BINARY for v in values):
        return None
    return sum(v == 'yes' for v in values)


def duration_days(row):
    if row.get('gold_relevant_duration_present', '').strip() != 'yes':
        return None
    try:
        value = float(row.get('gold_relevant_duration_value', '').strip())
    except ValueError:
        return None
    unit = row.get('gold_relevant_duration_unit', '').strip()
    factor = DURATION_TO_DAYS.get(unit)
    if factor is None or value <= 0:
        return None
    return value * factor


def load_demographics(raw_dir: Path, salt: str):
    """Map private pseudonymous study ID to one baseline demographic record."""
    data = defaultdict(lambda: {'sex': None, 'age': None, 'height': None, 'weight': None})
    path = raw_dir / BASIC_FILE
    if not path.exists():
        raise FileNotFoundError(path)
    for _, _, rows in read_xlsx(path):
        for row in rows:
            admission_key = norm_id(row.get('住院id'))
            if not admission_key:
                continue
            sid = make_study_id(admission_key, salt)
            rec = data[sid]
            if rec['sex'] is None and row.get('性别') is not None:
                rec['sex'] = str(row.get('性别')).strip()
            if rec['age'] is None and row.get('年龄') is not None:
                try: rec['age'] = float(row.get('年龄'))
                except Exception: pass
            if rec['height'] is None and row.get('身高') is not None:
                try: rec['height'] = float(row.get('身高'))
                except Exception: pass
            if rec['weight'] is None and row.get('体重') is not None:
                try: rec['weight'] = float(row.get('体重'))
                except Exception: pass
    for rec in data.values():
        h = rec['height']; w = rec['weight']
        if h and w:
            h = h / 100.0 if h > 3 else h
            bmi = w / (h * h) if h > 0 else None
            rec['bmi'] = bmi if bmi and 10 <= bmi <= 60 else None
        else:
            rec['bmi'] = None
    return data


def load_gold(review_dir: Path):
    # build_final_manifest performs controlled-vocabulary and population checks.
    build_final_manifest(review_dir)
    anatomy = {r['study_id'].strip(): r for r in read_rows(review_dir / 'scaphoid_anatomy_adjudicated.csv')}
    state = {r['study_id'].strip(): r for r in read_rows(review_dir / 'scaphoid_state_adjudicated.csv')}
    procedure = {r['study_id'].strip(): r for r in read_rows(review_dir / 'scaphoid_procedure_adjudicated.csv')}
    return anatomy, state, procedure


def operative_records(state, procedure, demographics=None):
    demographics = demographics or {}
    records = []
    for sid, proc in procedure.items():
        if proc.get('gold_target_disease_procedure_present', '').strip() != 'yes':
            continue
        state_row = state.get(sid)
        if not state_row:
            continue
        group = state_group(state_row.get('gold_scaphoid_state', '').strip())
        if group is None:
            continue
        records.append({
            'study_id': sid,
            'group': group,
            'state': state_row.get('gold_scaphoid_state', '').strip(),
            'fixation': proc.get('gold_internal_fixation', '').strip(),
            'graft': proc.get('gold_bone_graft', '').strip(),
            'reconstruction': proc.get('gold_reconstruction', '').strip(),
            'fusion': proc.get('gold_fusion', '').strip(),
            'augmentation': augmentation_label(proc),
            'component_count': component_count(proc),
            'duration_days': duration_days(state_row),
            'duration_basis': state_row.get('gold_duration_basis', '').strip(),
            'age': demographics.get(sid, {}).get('age'),
            'sex': demographics.get(sid, {}).get('sex'),
            'bmi': demographics.get(sid, {}).get('bmi'),
        })
    return records


def leave_one_out_binary(records, outcome):
    evaluable = [r for r in records if r[outcome] in BINARY]
    rows = []
    for i in range(len(evaluable)):
        subset = evaluable[:i] + evaluable[i+1:]
        chronic = [r[outcome] for r in subset if r['group'] == 'chronic_nonunion']
        acute = [r[outcome] for r in subset if r['group'] == 'acute_new']
        if not chronic or not acute:
            continue
        result = exact_binary_analysis(chronic, acute)
        rows.append({
            'removed_group': evaluable[i]['group'],
            'removed_outcome': evaluable[i][outcome],
            'odds_ratio_conditional': result['odds_ratio_conditional'],
            'fisher_two_sided_p': result['fisher_two_sided_p'],
        })
    ors = [r['odds_ratio_conditional'] for r in rows if r['odds_ratio_conditional'] is not None]
    ps = [r['fisher_two_sided_p'] for r in rows if r['fisher_two_sided_p'] is not None]
    return {
        'iterations': len(rows),
        'or_min': min(ors) if ors else None,
        'or_max': max(ors) if ors else None,
        'p_min': min(ps) if ps else None,
        'p_max': max(ps) if ps else None,
        'all_or_above_one': bool(ors) and all(x > 1 for x in ors),
        'iterations_detail': rows,
    }


def analyze(records):
    chronic = [r for r in records if r['group'] == 'chronic_nonunion']
    acute = [r for r in records if r['group'] == 'acute_new']

    primary = exact_binary_analysis([r['graft'] for r in chronic], [r['graft'] for r in acute])
    fixation = exact_binary_analysis([r['fixation'] for r in chronic], [r['fixation'] for r in acute])
    augmentation = exact_binary_analysis([r['augmentation'] for r in chronic], [r['augmentation'] for r in acute])

    chronic_components = [r['component_count'] for r in chronic if r['component_count'] is not None]
    acute_components = [r['component_count'] for r in acute if r['component_count'] is not None]

    duration_records = [r for r in chronic if r['graft'] in BINARY and r['duration_days'] is not None]
    graft_duration = [r['duration_days'] for r in duration_records if r['graft'] == 'yes']
    no_graft_duration = [r['duration_days'] for r in duration_records if r['graft'] == 'no']

    injury_duration_records = [r for r in duration_records if r['duration_basis'] in {'injury_since_event', 'both'}]
    injury_graft = [r['duration_days'] for r in injury_duration_records if r['graft'] == 'yes']
    injury_no_graft = [r['duration_days'] for r in injury_duration_records if r['graft'] == 'no']

    def female_count(group):
        known = [r['sex'] for r in group if r['sex']]
        female = sum(str(x).strip() in {'女', 'female', 'Female', 'F'} for x in known)
        return {'known_n': len(known), 'female_n': female}

    return {
        'analysis_plan': 'SCAPHOID_ANALYSIS_PLAN_V0_3',
        'operative_population': {
            'chronic_nonunion_n': len(chronic),
            'acute_new_n': len(acute),
            'total_n': len(records),
        },
        'baseline': {
            'chronic_nonunion': {
                'age': numeric_summary([r['age'] for r in chronic if r['age'] is not None]),
                'bmi': numeric_summary([r['bmi'] for r in chronic if r['bmi'] is not None]),
                'sex': female_count(chronic),
            },
            'acute_new': {
                'age': numeric_summary([r['age'] for r in acute if r['age'] is not None]),
                'bmi': numeric_summary([r['bmi'] for r in acute if r['bmi'] is not None]),
                'sex': female_count(acute),
            },
        },
        'primary_bone_graft': primary,
        'key_contrast_internal_fixation': fixation,
        'secondary_augmentation_composite': augmentation,
        'secondary_component_count': {
            'chronic_nonunion': numeric_summary(chronic_components),
            'acute_new': numeric_summary(acute_components),
            'mann_whitney': safe_mannwhitney(chronic_components, acute_components),
        },
        'secondary_duration': {
            'bone_graft_present': numeric_summary(graft_duration),
            'bone_graft_absent': numeric_summary(no_graft_duration),
            'mann_whitney': safe_mannwhitney(graft_duration, no_graft_duration),
            'injury_basis_only': {
                'bone_graft_present': numeric_summary(injury_graft),
                'bone_graft_absent': numeric_summary(injury_no_graft),
                'mann_whitney': safe_mannwhitney(injury_graft, injury_no_graft),
            },
        },
        'leave_one_out_primary_bone_graft': leave_one_out_binary(records, 'graft'),
    }


def suppress(n):
    if n is None:
        return ''
    n = int(n)
    return '<5' if 0 < n < 5 else str(n)


def public_rows(result):
    rows = []
    pop = result['operative_population']
    rows.append({'metric': 'operative_population', 'chronic_nonunion': str(pop['chronic_nonunion_n']), 'acute_new': str(pop['acute_new_n']), 'note': 'physician-adjudicated target-disease detailed operations'})

    for key, label in [
        ('primary_bone_graft', 'bone_graft'),
        ('key_contrast_internal_fixation', 'internal_fixation'),
        ('secondary_augmentation_composite', 'augmentation_composite'),
    ]:
        item = result[key]
        t = item['table']
        cy = t['chronic_yes']; cn = t['chronic_no']; ay = t['acute_yes']; an = t['acute_no']
        any_small = any(0 < x < 5 for x in (cy, cn, ay, an))
        rows.append({
            'metric': label,
            'chronic_nonunion': f"{suppress(cy)}/{item['chronic_evaluable']}",
            'acute_new': f"{suppress(ay)}/{item['acute_evaluable']}",
            'note': 'exact inferential statistics suppressed in public release due to small cells' if any_small else f"conditional OR={item['odds_ratio_conditional']:.3g}; Fisher p={item['fisher_two_sided_p']:.4g}",
        })

    duration = result['secondary_duration']
    for key, label in [('bone_graft_present', 'duration_days_graft_present'), ('bone_graft_absent', 'duration_days_graft_absent')]:
        s = duration[key]
        rows.append({
            'metric': label,
            'chronic_nonunion': f"n={s['n']}; median={s['median']:.1f}; IQR={s['q1']:.1f}-{s['q3']:.1f}" if s['n'] else 'n=0',
            'acute_new': '',
            'note': 'secondary physician-adjudicated duration analysis',
        })
    return rows


def write_public_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ['metric', 'chronic_nonunion', 'acute_new', 'note']
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--review-dir', required=True)
    ap.add_argument('--raw-dir', required=True)
    ap.add_argument('--salt-file', required=True)
    ap.add_argument('--private-output', required=True)
    ap.add_argument('--public-output', required=True)
    args = ap.parse_args()

    review_dir = Path(args.review_dir)
    raw_dir = Path(args.raw_dir)
    salt = load_salt(args.salt_file)
    _, state, procedure = load_gold(review_dir)
    demographics = load_demographics(raw_dir, salt)
    records = operative_records(state, procedure, demographics)
    result = analyze(records)

    private_out = Path(args.private_output)
    private_out.parent.mkdir(parents=True, exist_ok=True)
    private_out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    write_public_csv(Path(args.public_output), public_rows(result))
    print(f"private manuscript analysis: {private_out}")
    print(f"public-safe aggregate: {args.public_output}")


if __name__ == '__main__':
    main()
