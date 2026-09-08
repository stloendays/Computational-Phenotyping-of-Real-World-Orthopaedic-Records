#!/usr/bin/env python3
"""Generate LOCAL-ONLY deterministic baseline predictions from annotation packets.

The predictor consumes source-text columns and writes study-ID-level predictions.
It never reads columns whose names begin with ``gold_``. Prediction files remain
private because study IDs are pseudonymous row-level identifiers.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import csv
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rules import HALLUX_RE, CMC_RE, SCAPHOID_CHRONIC_RE, scaphoid_anatomy_class
from procedure_rules import note_is_domain_concordant, extract_procedure_labels


def read_source_rows(path: Path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    # Guardrail: expose only non-gold fields to downstream prediction functions.
    return [
        {k: v for k, v in row.items() if not k.startswith('gold_')}
        for row in rows
    ]


def write_rows(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


def disease_anatomy_predictions(rows):
    out = []
    for row in rows:
        domain = row['domain']
        text = ' '.join([
            row.get('diagnosis_text', ''), row.get('complaint_text', ''),
            row.get('physical_exam_text', ''),
        ])
        if domain == 'hallux_valgus':
            pred = 'yes' if HALLUX_RE.search(text) else 'no'
        elif domain == 'first_cmc_oa':
            pred = 'yes' if CMC_RE.search(text) else 'no'
        elif domain == 'scaphoid_fracture':
            cls = scaphoid_anatomy_class(text)
            pred = {'wrist_scaphoid':'wrist_scaphoid',
                    'foot_navicular':'foot_navicular',
                    'ambiguous':'uncertain'}[cls]
        else:
            raise ValueError(f'unknown domain: {domain}')
        out.append({'study_id':row['study_id'],'domain':domain,'pred_disease_anatomy_label':pred})
    return out


def scaphoid_state_predictions(rows):
    out=[]
    for row in rows:
        text=' '.join([row.get('diagnosis_text',''),row.get('complaint_text',''),row.get('physical_exam_text','')])
        pred='established_chronic_or_nonunion' if SCAPHOID_CHRONIC_RE.search(text) else 'other_wrist_scaphoid'
        out.append({'study_id':row['study_id'],'pred_scaphoid_state_binary':pred})
    return out


def procedure_predictions(rows):
    out=[]
    for row in rows:
        domain=row['domain']
        # Detailed note is the primary relevance source. The operation-name field is
        # kept separate for physician review and is not required by this baseline.
        note=row.get('operation_note_text','')
        relevant=note_is_domain_concordant(domain,note)
        labels=extract_procedure_labels(domain,[note],require_domain_concordance=True) if relevant else set()
        out.append({
            'study_id':row['study_id'],
            'domain':domain,
            'pred_target_disease_procedure_present':'yes' if relevant else 'no',
            'pred_procedure_labels':'|'.join(sorted(labels)),
        })
    return out


def build(annotation_dir: Path, output_dir: Path):
    disease = read_source_rows(annotation_dir/'disease_anatomy_annotation.csv')
    state = read_source_rows(annotation_dir/'scaphoid_state_annotation.csv')
    procedure = read_source_rows(annotation_dir/'procedure_annotation.csv')

    write_rows(output_dir/'rule_disease_anatomy_predictions.csv',
               disease_anatomy_predictions(disease),
               ['study_id','domain','pred_disease_anatomy_label'])
    write_rows(output_dir/'rule_scaphoid_state_predictions.csv',
               scaphoid_state_predictions(state),
               ['study_id','pred_scaphoid_state_binary'])
    write_rows(output_dir/'rule_procedure_predictions.csv',
               procedure_predictions(procedure),
               ['study_id','domain','pred_target_disease_procedure_present','pred_procedure_labels'])


if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--annotation-dir',required=True,help='local annotations/private directory')
    ap.add_argument('--output-dir',required=True,help='local private prediction directory')
    args=ap.parse_args()
    build(Path(args.annotation_dir),Path(args.output_dir))
