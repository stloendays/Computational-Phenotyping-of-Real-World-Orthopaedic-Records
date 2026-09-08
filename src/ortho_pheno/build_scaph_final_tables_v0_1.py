#!/usr/bin/env python3
"""Build PRIVATE manuscript-ready tables from the frozen post-Gold analysis JSON.

The generated tables may contain exact small-cell counts and therefore belong in
`outputs/private/` until privacy/manuscript review is complete.

This script does not recalculate statistics. It only formats the exact results
produced by `analyze_scaph_gold_v0_2.py`.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import json
import math


def fmt_num(x, digits=1):
    if x is None:
        return 'NA'
    return f'{float(x):.{digits}f}'


def fmt_p(x):
    if x is None:
        return 'NA'
    x = float(x)
    return '<0.001' if x < 0.001 else f'{x:.3f}'


def fmt_or_ci(item):
    orv = item.get('odds_ratio_conditional')
    lo = item.get('ci95_low')
    hi = item.get('ci95_high')
    if orv is None:
        return 'NA'
    if math.isinf(float(orv)):
        or_text = 'Inf'
    else:
        or_text = f'{float(orv):.2f}'
    if lo is None or hi is None:
        return or_text
    lo_text = '0' if float(lo) == 0 else f'{float(lo):.2f}'
    hi_text = 'Inf' if math.isinf(float(hi)) else f'{float(hi):.2f}'
    return f'{or_text} ({lo_text}-{hi_text})'


def fmt_median_iqr(summary, digits=1):
    if not summary or int(summary.get('n', 0)) == 0:
        return 'NA'
    return f"{fmt_num(summary.get('median'), digits)} [{fmt_num(summary.get('q1'), digits)}, {fmt_num(summary.get('q3'), digits)}]"


def fmt_binary_group(item, prefix):
    t = item['table']
    if prefix == 'chronic':
        yes = int(t['chronic_yes']); n = int(item['chronic_evaluable'])
    else:
        yes = int(t['acute_yes']); n = int(item['acute_evaluable'])
    pct = 100 * yes / n if n else 0
    return f'{yes}/{n} ({pct:.1f}%)'


def table1(result):
    pop = result['operative_population']
    b = result['baseline']
    chronic = b['chronic_nonunion']; acute = b['acute_new']

    def sex_text(x):
        n = int(x.get('known_n', 0)); f = int(x.get('female_n', 0))
        return 'NA' if n == 0 else f'{f}/{n} ({100*f/n:.1f}%)'

    rows = [
        ('Operative records, n', str(pop['chronic_nonunion_n']), str(pop['acute_new_n'])),
        ('Age, years, median [IQR]', fmt_median_iqr(chronic['age']), fmt_median_iqr(acute['age'])),
        ('Female sex, n/N (%)', sex_text(chronic['sex']), sex_text(acute['sex'])),
        ('BMI, kg/m2, median [IQR]', fmt_median_iqr(chronic['bmi']), fmt_median_iqr(acute['bmi'])),
    ]
    lines = [
        '# Table 1. Baseline characteristics of the physician-adjudicated operative cohort',
        '',
        '| Characteristic | Established chronic/nonunion | Acute/new fracture |',
        '|---|---:|---:|',
    ]
    lines += [f'| {a} | {b1} | {b2} |' for a,b1,b2 in rows]
    lines += ['', 'Values are reported using evaluable denominators. Missing BMI/sex data are not imputed.']
    return '\n'.join(lines) + '\n'


def table2(result):
    items = [
        ('Bone-graft augmentation', result['primary_bone_graft']),
        ('Internal fixation', result['key_contrast_internal_fixation']),
        ('Graft/reconstruction/fusion augmentation', result['secondary_augmentation_composite']),
    ]
    lines = [
        '# Table 2. Operative treatment composition by physician-adjudicated presentation state',
        '',
        '| Operative component | Established chronic/nonunion | Acute/new fracture | Conditional OR (95% CI) | Fisher P |',
        '|---|---:|---:|---:|---:|',
    ]
    for label,item in items:
        lines.append(
            f"| {label} | {fmt_binary_group(item,'chronic')} | {fmt_binary_group(item,'acute')} | {fmt_or_ci(item)} | {fmt_p(item.get('fisher_two_sided_p'))} |"
        )

    cc = result['secondary_component_count']
    lines += [
        '',
        'Major operative-component count:',
        '',
        f"- Established chronic/nonunion: {fmt_median_iqr(cc['chronic_nonunion'])}",
        f"- Acute/new fracture: {fmt_median_iqr(cc['acute_new'])}",
        f"- Mann-Whitney P: {fmt_p(cc['mann_whitney'].get('p_value'))}",
        '',
        'Uncertain component labels are excluded from the corresponding binary denominator and are not coded as negative.',
    ]
    return '\n'.join(lines) + '\n'


def table_s1(result):
    d = result['secondary_duration']
    g = d['bone_graft_present']; ng = d['bone_graft_absent']
    injury = d['injury_basis_only']
    lines = [
        '# Supplementary Table S1. Documented wrist-related duration within established chronic/nonunion operative records',
        '',
        '| Duration analysis | Bone graft present | Bone graft absent | Mann-Whitney P |',
        '|---|---:|---:|---:|',
        f"| All physician-valid relevant durations, days, median [IQR] | {fmt_median_iqr(g)} (n={g['n']}) | {fmt_median_iqr(ng)} (n={ng['n']}) | {fmt_p(d['mann_whitney'].get('p_value'))} |",
        f"| Injury-basis only, days, median [IQR] | {fmt_median_iqr(injury['bone_graft_present'])} (n={injury['bone_graft_present']['n']}) | {fmt_median_iqr(injury['bone_graft_absent'])} (n={injury['bone_graft_absent']['n']}) | {fmt_p(injury['mann_whitney'].get('p_value'))} |",
        '',
        'Duration is a prespecified exploratory secondary analysis. No local duration cutoff is optimized.',
    ]
    return '\n'.join(lines) + '\n'


def build(private_json: Path, output_dir: Path):
    result = json.loads(private_json.read_text(encoding='utf-8'))
    required = {
        'operative_population','baseline','primary_bone_graft','key_contrast_internal_fixation',
        'secondary_augmentation_composite','secondary_component_count','secondary_duration'
    }
    missing = required - set(result)
    if missing:
        raise ValueError(f'analysis JSON missing required keys: {sorted(missing)}')

    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        'table1': output_dir / 'Table1_baseline_characteristics.md',
        'table2': output_dir / 'Table2_operative_composition.md',
        'table_s1': output_dir / 'TableS1_duration_secondary.md',
    }
    paths['table1'].write_text(table1(result), encoding='utf-8')
    paths['table2'].write_text(table2(result), encoding='utf-8')
    paths['table_s1'].write_text(table_s1(result), encoding='utf-8')
    return paths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--private-analysis-json', required=True)
    ap.add_argument('--output-dir', required=True)
    args = ap.parse_args()
    paths = build(Path(args.private_analysis_json), Path(args.output_dir))
    for name,path in paths.items():
        print(f'{name}: {path}')


if __name__ == '__main__':
    main()
