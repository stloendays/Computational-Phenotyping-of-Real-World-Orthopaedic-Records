#!/usr/bin/env python3
"""Exploratory pre-validation audit of documented wrist-injury/symptom duration.

This analysis asks whether, within deterministic established chronic/nonunion
scaphoid operative records, bone-graft use is concentrated among records with a
longer explicitly documented injury/symptom duration.

It is a secondary, hypothesis-generating audit. Duration phrases require physician
validation before manuscript interpretation.

Only privacy-preserving aggregate outputs are written.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import csv
import math
import re
import statistics
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_safe_release import read_xlsx, norm_id
from scaphoid_augmentation_analysis_v0_1 import collect

COMPLAINT_FILE = '2015-2025舟骨骨折患者主诉和专科查体.xlsx'

CN = {'一':1,'二':2,'两':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}
NUM = r'(?:\d+(?:\.\d+)?|[一二三四五六七八九十两]+)'

# Order matters: half-unit expressions must be consumed before generic units.
DURATION_PATTERNS = (
    (re.compile(fr'({NUM})\s*年半'),lambda v:(v+0.5)*365.25),
    (re.compile(fr'({NUM})\s*个?半月'),lambda v:(v+0.5)*30.44),
    (re.compile(r'半年'),lambda v:0.5*365.25),
    (re.compile(fr'({NUM})\s*年'),lambda v:v*365.25),
    (re.compile(fr'({NUM})\s*个?月'),lambda v:v*30.44),
    (re.compile(fr'({NUM})\s*(?:周|星期)'),lambda v:v*7),
    (re.compile(fr'({NUM})\s*(?:天|日)'),lambda v:v),
    (re.compile(fr'({NUM})\s*小时'),lambda v:v/24),
)


def cn_number(text: str):
    try:
        return float(text)
    except Exception:
        pass
    if '十' in text:
        left,right = text.split('十',1)
        tens = CN.get(left,1) if left else 1
        ones = CN.get(right,0) if right else 0
        return 10*tens + ones
    return CN.get(text)


def extract_duration_days(text: str):
    values=[]
    occupied=[]
    for pattern,convert in DURATION_PATTERNS:
        for match in pattern.finditer(text or ''):
            if any(not (match.end() <= a or match.start() >= b) for a,b in occupied):
                continue
            raw = match.group(1) if match.lastindex else None
            value = 0.5 if raw is None else cn_number(raw)
            if value is None:
                continue
            values.append(float(convert(value)))
            occupied.append((match.start(),match.end()))
    return values


def qtile(values,p):
    xs=sorted(float(x) for x in values)
    if not xs:
        return None
    pos=(len(xs)-1)*p
    lo=math.floor(pos); hi=math.ceil(pos)
    if lo==hi:
        return xs[lo]
    return xs[lo]+(xs[hi]-xs[lo])*(pos-lo)


def complaint_map(raw_dir: Path):
    out={}
    path=raw_dir/COMPLAINT_FILE
    for _,_,rows in read_xlsx(path):
        for row in rows:
            key=norm_id(row.get('住院id'))
            if not key:
                continue
            text=row.get('主诉')
            if isinstance(text,str) and text.strip():
                out.setdefault(key,[]).append(text.strip())
    return out


def build(raw_dir: Path):
    recs=collect(raw_dir)
    complaints=complaint_map(raw_dir)

    # collect() is keyed by raw local admission ID; this script remains local.
    strict=[]
    for key,rec in recs.items():
        if rec['anatomy']!='wrist_scaphoid' or not rec['chronic_nonunion'] or not rec['relevant_notes']:
            continue
        durations=extract_duration_days(' '.join(complaints.get(key,[])))
        max_duration=max(durations) if durations else None
        strict.append({
            'graft':'bone_graft' in rec['procedure_labels'],
            'duration_days':max_duration,
        })

    if len(strict)!=15:
        raise AssertionError(f'expected 15 deterministic chronic/nonunion disease-concordant operative records, got {len(strict)}')

    rows=[]
    for graft,label in ((True,'bone_graft_present'),(False,'bone_graft_absent')):
        subset=[r for r in strict if r['graft']==graft]
        durations=[r['duration_days'] for r in subset if r['duration_days'] is not None]
        rows.append({
            'deterministic_group':label,
            'operative_records':len(subset),
            'records_with_explicit_duration':len(durations),
            'duration_median_days':f'{statistics.median(durations):.1f}' if durations else '',
            'duration_q1_days':f'{qtile(durations,0.25):.1f}' if durations else '',
            'duration_q3_days':f'{qtile(durations,0.75):.1f}' if durations else '',
            'status':'pre-validation exploratory; duration semantics require physician adjudication',
        })
    return rows


def main(raw_dir: Path,output: Path):
    rows=build(raw_dir)
    output.parent.mkdir(parents=True,exist_ok=True)
    fields=['deterministic_group','operative_records','records_with_explicit_duration','duration_median_days','duration_q1_days','duration_q3_days','status']
    with output.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    print(f'wrote aggregate duration audit: {output}')


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--raw-dir',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    main(Path(args.raw_dir),Path(args.output))
