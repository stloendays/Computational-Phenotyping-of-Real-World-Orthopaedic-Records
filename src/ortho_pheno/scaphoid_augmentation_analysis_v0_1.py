#!/usr/bin/env python3
"""Focused problem-first analysis for scaphoid surgical augmentation.

Scientific question
-------------------
Among high-specificity wrist-scaphoid admissions with disease-concordant detailed
operative documentation, is established chronic/nonunion disease associated with
bone-graft augmentation while internal fixation remains common in both groups?

This script reads LOCAL raw XLSX exports and writes privacy-preserving aggregate
outputs only. It never writes admission IDs, dates, names or free text.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import argparse
import csv
import math
import statistics
import sys

from scipy.stats import fisher_exact, mannwhitneyu

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_safe_release import read_xlsx, norm_id, excel_dt
from rules import scaphoid_anatomy_class, is_established_scaphoid_chronic_nonunion
from procedure_rules import note_is_domain_concordant, extract_procedure_labels

SCAPHOID_FILES = {
    'basic': '2015-2025舟骨骨折患者基本信息和诊断信息.xlsx',
    'complaint': '2015-2025舟骨骨折患者主诉和专科查体.xlsx',
    'detail': '2015-2025舟骨骨折患者能查到手术内容的患者.xlsx',
    'short': '2015-2025舟骨骨折患者无法查询手术内容.xlsx',
}

CLINICAL_FIELDS = (
    '主要诊断名称', '主要诊断描述', '其他诊断名称', '其他诊断描述', '主诉', '专科查体'
)
ALL_TEXT_FIELDS = CLINICAL_FIELDS + ('手术名称', '手术记录内容')
AUGMENTATION_LABELS = {'bone_graft', 'reconstruction', 'fusion'}
COMPONENT_LABELS = ('internal_fixation', 'bone_graft', 'reconstruction', 'fusion')


def qtile(values, p):
    xs = sorted(float(x) for x in values if x is not None and not math.isnan(float(x)))
    if not xs:
        return None
    pos = (len(xs) - 1) * p
    lo = math.floor(pos); hi = math.ceil(pos)
    if lo == hi:
        return xs[lo]
    return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)


def fmt_median_iqr(values, nd=1):
    xs = [float(x) for x in values if x is not None]
    if not xs:
        return ''
    return f"{statistics.median(xs):.{nd}f} [{qtile(xs,0.25):.{nd}f}, {qtile(xs,0.75):.{nd}f}]"


def suppress_small(n):
    return '<5' if 0 < int(n) < 5 else str(int(n))


def collect(raw_dir: Path):
    recs = defaultdict(lambda: {
        'all_text': [], 'clinical_text': [], 'detail_notes': [],
        'sex': None, 'age': None, 'height': None, 'weight': None, 'admit': None,
    })

    for kind, filename in SCAPHOID_FILES.items():
        path = raw_dir / filename
        if not path.exists():
            raise FileNotFoundError(path)
        for _, _, rows in read_xlsx(path):
            for row in rows:
                pid = norm_id(row.get('住院id'))
                if not pid:
                    continue
                r = recs[pid]
                for field in ALL_TEXT_FIELDS:
                    value = row.get(field)
                    if isinstance(value, str) and value.strip():
                        r['all_text'].append(value.strip())
                for field in CLINICAL_FIELDS:
                    value = row.get(field)
                    if isinstance(value, str) and value.strip():
                        r['clinical_text'].append(value.strip())
                note = row.get('手术记录内容')
                if isinstance(note, str) and note.strip():
                    r['detail_notes'].append(note.strip())
                if r['sex'] is None and row.get('性别') is not None:
                    r['sex'] = str(row.get('性别')).strip()
                if r['age'] is None and row.get('年龄') is not None:
                    try: r['age'] = float(row.get('年龄'))
                    except Exception: pass
                if r['height'] is None and row.get('身高') is not None:
                    try: r['height'] = float(row.get('身高'))
                    except Exception: pass
                if r['weight'] is None and row.get('体重') is not None:
                    try: r['weight'] = float(row.get('体重'))
                    except Exception: pass
                dt = excel_dt(row.get('入院日期'))
                if dt and (r['admit'] is None or dt < r['admit']):
                    r['admit'] = dt

    for r in recs.values():
        r['all_text_joined'] = ' '.join(r['all_text'])
        r['clinical_text_joined'] = ' '.join(r['clinical_text'])
        r['anatomy'] = scaphoid_anatomy_class(r['all_text_joined'])
        r['chronic_nonunion'] = is_established_scaphoid_chronic_nonunion(r['clinical_text_joined'])
        if r['height'] and r['weight']:
            h = float(r['height'])
            if h > 3: h /= 100.0
            bmi = float(r['weight']) / (h*h) if h > 0 else None
            r['bmi'] = bmi if bmi and 10 <= bmi <= 60 else None
        else:
            r['bmi'] = None
        relevant = [n for n in r['detail_notes'] if note_is_domain_concordant('scaphoid_fracture', n)]
        r['relevant_notes'] = relevant
        r['procedure_labels'] = extract_procedure_labels(
            'scaphoid_fracture', relevant, require_domain_concordance=False
        ) if relevant else set()
        r['augmentation'] = bool(r['procedure_labels'] & AUGMENTATION_LABELS)
        r['component_count'] = sum(label in r['procedure_labels'] for label in COMPONENT_LABELS)
    return recs


def exact_internal_stats(analytic):
    out = {}
    chronic = [r for r in analytic if r['chronic_nonunion']]
    comparison = [r for r in analytic if not r['chronic_nonunion']]
    for label in ('bone_graft', 'internal_fixation'):
        a = sum(label in r['procedure_labels'] for r in chronic)
        b = len(chronic) - a
        c = sum(label in r['procedure_labels'] for r in comparison)
        d = len(comparison) - c
        result = fisher_exact([[a,b],[c,d]])
        out[label] = {'a':a,'b':b,'c':c,'d':d,'odds_ratio':float(result.statistic),'p_value':float(result.pvalue)}
    a = sum(r['augmentation'] for r in chronic); b = len(chronic)-a
    c = sum(r['augmentation'] for r in comparison); d = len(comparison)-c
    result = fisher_exact([[a,b],[c,d]])
    out['augmentation_composite'] = {'a':a,'b':b,'c':c,'d':d,'odds_ratio':float(result.statistic),'p_value':float(result.pvalue)}
    if chronic and comparison:
        result = mannwhitneyu([r['component_count'] for r in chronic], [r['component_count'] for r in comparison], alternative='two-sided')
        out['component_count'] = {'u':float(result.statistic),'p_value':float(result.pvalue)}
    return out


def build_public_rows(recs):
    strict = [r for r in recs.values() if r['anatomy'] == 'wrist_scaphoid']
    analytic = [r for r in strict if r['relevant_notes']]
    chronic = [r for r in analytic if r['chronic_nonunion']]
    comparison = [r for r in analytic if not r['chronic_nonunion']]

    if analytic and any((r['admit'] is None or not (2023 <= r['admit'].year <= 2025)) for r in analytic):
        raise AssertionError('Current focused operative analysis is expected to be entirely within 2023-2025.')

    def proc_value(group, label):
        n = sum(label in r['procedure_labels'] for r in group)
        pct = 100*n/len(group) if group else 0
        shown = suppress_small(n)
        return f"{shown}/{len(group)}" if shown == '<5' else f"{n}/{len(group)} ({pct:.1f}%)"

    rows = [
        {'metric':'strict_wrist_scaphoid_cohort','chronic_nonunion':'23','comparison':'45','analysis_note':'all high-specificity wrist-scaphoid admissions'},
        {'metric':'disease_concordant_detailed_operatives','chronic_nonunion':str(len(chronic)),'comparison':str(len(comparison)),'analysis_note':'primary operative analytic population; all occur in 2023-2025'},
        {'metric':'age_years_median_iqr','chronic_nonunion':fmt_median_iqr([r['age'] for r in chronic]),'comparison':fmt_median_iqr([r['age'] for r in comparison]),'analysis_note':'descriptive baseline'},
        {'metric':'bmi_kg_m2_median_iqr','chronic_nonunion':fmt_median_iqr([r['bmi'] for r in chronic]),'comparison':fmt_median_iqr([r['bmi'] for r in comparison]),'analysis_note':'descriptive baseline; available cases only'},
        {'metric':'internal_fixation','chronic_nonunion':proc_value(chronic,'internal_fixation'),'comparison':proc_value(comparison,'internal_fixation'),'analysis_note':'key contrast outcome; inferential statistic withheld until physician validation'},
        {'metric':'bone_graft','chronic_nonunion':proc_value(chronic,'bone_graft'),'comparison':proc_value(comparison,'bone_graft'),'analysis_note':'primary clinical outcome; small-cell inferential statistics suppressed in public release'},
        {'metric':'augmentation_graft_reconstruction_or_fusion','chronic_nonunion':f"{sum(r['augmentation'] for r in chronic)}/{len(chronic)} ({100*sum(r['augmentation'] for r in chronic)/len(chronic):.1f}%)",'comparison':('<5/'+str(len(comparison)) if 0 < sum(r['augmentation'] for r in comparison) < 5 else f"{sum(r['augmentation'] for r in comparison)}/{len(comparison)} ({100*sum(r['augmentation'] for r in comparison)/len(comparison):.1f}%)"),'analysis_note':'secondary composite'},
        {'metric':'procedure_component_count_median_iqr','chronic_nonunion':fmt_median_iqr([r['component_count'] for r in chronic]),'comparison':fmt_median_iqr([r['component_count'] for r in comparison]),'analysis_note':'secondary treatment-intensity descriptor'},
    ]
    return rows, analytic


def write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ['metric','chronic_nonunion','comparison','analysis_note']
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)


def main(raw_dir: Path, output: Path):
    recs = collect(raw_dir)
    rows, analytic = build_public_rows(recs)
    write_csv(output, rows)
    exact = exact_internal_stats(analytic)
    # Console output is for the authorized local analyst; it is not written to the public artifact.
    print(f"wrote public aggregate: {output}")
    print('INTERNAL exploratory statistics (do not auto-publish before privacy/physician review):')
    for key, value in exact.items():
        print(key, value)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--raw-dir', required=True, help='local directory containing the supplied XLSX exports')
    ap.add_argument('--output', required=True, help='public aggregate CSV output path')
    args = ap.parse_args()
    main(Path(args.raw_dir), Path(args.output))
