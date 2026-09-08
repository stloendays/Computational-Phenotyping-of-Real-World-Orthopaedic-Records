#!/usr/bin/env python3
"""Privacy-tight public wrapper for the prespecified scaphoid post-Gold analysis.

The statistical engine is `analyze_scaph_gold_v0_1.py`. This v0.2 entrypoint
strengthens public-release suppression: if an outcome cell, denominator, or duration
subgroup contains 1-4 records, the public artifact never exposes enough detail to
reconstruct the small cell. Exact results remain in the private manuscript JSON.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import csv
import json

from analyze_scaph_gold_v0_1 import (
    load_gold,
    load_demographics,
    operative_records,
    analyze,
)
from make_scaph_physician_packet_v0_1 import load_salt


def suppress_n(n):
    if n is None:
        return ''
    n = int(n)
    return '<5' if 0 < n < 5 else str(n)


def group_fraction(yes_n, denominator):
    if denominator is None:
        return ''
    if 0 < int(denominator) < 5:
        return '<5 total'
    if 0 < int(yes_n) < 5:
        return f'<5/{int(denominator)}'
    return f'{int(yes_n)}/{int(denominator)}'


def public_rows(result):
    rows = []
    pop = result['operative_population']
    rows.append({
        'metric': 'operative_population',
        'chronic_nonunion': suppress_n(pop['chronic_nonunion_n']),
        'acute_new': suppress_n(pop['acute_new_n']),
        'note': 'physician-adjudicated target-disease detailed operations',
    })

    for key, label in [
        ('primary_bone_graft', 'bone_graft'),
        ('key_contrast_internal_fixation', 'internal_fixation'),
        ('secondary_augmentation_composite', 'augmentation_composite'),
    ]:
        item = result[key]
        t = item['table']
        cells = (t['chronic_yes'], t['chronic_no'], t['acute_yes'], t['acute_no'])
        denominators = (item['chronic_evaluable'], item['acute_evaluable'])
        any_small = any(0 < int(x) < 5 for x in cells + denominators)
        rows.append({
            'metric': label,
            'chronic_nonunion': group_fraction(t['chronic_yes'], item['chronic_evaluable']),
            'acute_new': group_fraction(t['acute_yes'], item['acute_evaluable']),
            'note': (
                'exact inferential statistics suppressed in public release due to small cells'
                if any_small else
                f"conditional OR={item['odds_ratio_conditional']:.3g}; Fisher p={item['fisher_two_sided_p']:.4g}"
            ),
        })

    duration = result['secondary_duration']
    for key, label in [
        ('bone_graft_present', 'duration_days_graft_present'),
        ('bone_graft_absent', 'duration_days_graft_absent'),
    ]:
        summary = duration[key]
        n = int(summary['n'])
        if 0 < n < 5:
            display = 'n=<5; distribution suppressed'
        elif n == 0:
            display = 'n=0'
        else:
            display = f"n={n}; median={summary['median']:.1f}; IQR={summary['q1']:.1f}-{summary['q3']:.1f}"
        rows.append({
            'metric': label,
            'chronic_nonunion': display,
            'acute_new': '',
            'note': 'secondary physician-adjudicated duration analysis',
        })
    return rows


def write_public_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ['metric', 'chronic_nonunion', 'acute_new', 'note']
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


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
    print(f'private manuscript analysis: {private_out}')
    print(f'public-safe aggregate: {args.public_output}')


if __name__ == '__main__':
    main()
