#!/usr/bin/env python3
"""Audit how much explicit acute/new evidence exists in the operative comparison group.

This is a conservative deterministic audit, not a replacement for physician
adjudication. It is used to justify a prespecified acute-only sensitivity analysis.

The script reads local raw XLSX exports and writes aggregate counts only.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import csv
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scaphoid_augmentation_analysis_v0_1 import collect

ACUTE_TIME_RE = re.compile(
    r'(?:伤后|受伤|摔伤|扭伤|砸伤|撞伤|跌伤|车祸|外伤).{0,20}'
    r'(?:\d+|一|二|三|四|五|六|七|八|九|十|半).{0,3}(?:小时|天|日|周|星期)'
)
ACUTE_WORD_RE = re.compile(r'新鲜|急性')
POSTOP_RE = re.compile(r'术后|内固定物存留|取出内固定|内固定.*取出')
LONG_DURATION_RE = re.compile(r'(?:\d+|一|二|三|四|五|六|七|八|九|十|半).{0,3}(?:个月|月|年)')

CATEGORIES = (
    'explicit_acute_or_recent_injury',
    'postoperative_history_without_chronic_keyword',
    'months_or_years_duration_without_chronic_keyword',
    'insufficient_explicit_state_evidence',
)


def classify(text: str) -> str:
    text = text or ''
    if ACUTE_TIME_RE.search(text) or ACUTE_WORD_RE.search(text):
        return CATEGORIES[0]
    if POSTOP_RE.search(text):
        return CATEGORIES[1]
    if LONG_DURATION_RE.search(text):
        return CATEGORIES[2]
    return CATEGORIES[3]


def suppress(n: int) -> str:
    return '<5' if 0 < n < 5 else str(n)


def build(raw_dir: Path):
    recs = collect(raw_dir)
    strict = [r for r in recs.values() if r['anatomy'] == 'wrist_scaphoid']
    operative = [r for r in strict if r['relevant_notes']]
    comparison = [r for r in operative if not r['chronic_nonunion']]

    counts = {key: 0 for key in CATEGORIES}
    for r in comparison:
        counts[classify(r['clinical_text_joined'])] += 1

    if len(comparison) != 13:
        raise AssertionError(f'expected 13 deterministic operative comparison records, got {len(comparison)}')

    rows = []
    for category in CATEGORIES:
        n = counts[category]
        rows.append({
            'comparison_state_evidence_category': category,
            'n_public': suppress(n),
            'denominator': len(comparison),
            'interpretation': {
                CATEGORIES[0]: 'explicit acute/new or recent-injury wording is present',
                CATEGORIES[1]: 'postoperative-history wording is present but explicit chronic/nonunion wording is absent',
                CATEGORIES[2]: 'month/year duration wording is present but explicit chronic/nonunion wording is absent',
                CATEGORIES[3]: 'conservative rule finds insufficient explicit evidence to call the record acute/new',
            }[category],
        })
    return rows


def main(raw_dir: Path, output: Path):
    rows = build(raw_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', encoding='utf-8-sig', newline='') as f:
        fields = ['comparison_state_evidence_category','n_public','denominator','interpretation']
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)
    print(f'wrote aggregate audit: {output}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--raw-dir', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    main(Path(args.raw_dir), Path(args.output))
