#!/usr/bin/env python3
"""Generate LOCAL-ONLY deterministic baseline predictions from annotation packets.

The input annotation packets contain protected clinical text and must remain local.
This script writes study-ID-level prediction files intended for local evaluation;
those prediction files also remain private. Only aggregate evaluation metrics may
be released publicly.
"""
from __future__ import annotations
from pathlib import Path
import argparse, csv, re, sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rules import (
    HALLUX_RE,
    CMC_RE,
    SCAPHOID_CHRONIC_RE,
    scaphoid_anatomy_class,
)

PROCEDURE_PATTERNS = {
    'hallux_valgus': {
        'osteotomy': re.compile(r'截骨|osteotomy', re.I),
        'chevron': re.compile(r'Chevron', re.I),
        'akin': re.compile(r'Akin', re.I),
        'scarf': re.compile(r'Scarf', re.I),
        'fusion': re.compile(r'融合|fusion|arthrodesis', re.I),
        'k_wire': re.compile(r'克氏针|钢针|K[- ]?wire|Kirschner', re.I),
        'resection': re.compile(r'切除|resection', re.I),
        'soft_tissue': re.compile(r'软组织|肌腱|韧带|关节囊|松解|tendon|ligament', re.I),
    },
    'scaphoid_fracture': {
        'internal_fixation': re.compile(r'内固定|螺钉|空心钉|钢针|screw', re.I),
        'bone_graft': re.compile(r'植骨|取骨|bone graft', re.I),
        'reconstruction': re.compile(r'重建|reconstruction', re.I),
        'fusion': re.compile(r'融合|arthrodesis', re.I),
        'hardware_removal': re.compile(r'取出内固定|内固定.*去除|hardware removal', re.I),
        'debridement': re.compile(r'清创|病灶清除|debridement', re.I),
    },
    'first_cmc_oa': {
        'trapeziectomy': re.compile(r'大多角骨.*切除|切除.*大多角骨|trapeziectomy', re.I),
        'tendon_procedure': re.compile(r'肌腱|tendon', re.I),
        'ligament_procedure': re.compile(r'韧带|ligament', re.I),
        'arthroplasty': re.compile(r'关节成形|关节置换|arthroplasty', re.I),
        'fusion': re.compile(r'融合|arthrodesis', re.I),
    },
}


def _join(*parts):
    return ' '.join((x or '').strip() for x in parts if (x or '').strip())


def predict_disease_anatomy(domain, diagnosis_text='', complaint_text='', physical_exam_text=''):
    text = _join(diagnosis_text, complaint_text, physical_exam_text)
    if domain == 'hallux_valgus':
        return 'yes' if HALLUX_RE.search(text) else 'no'
    if domain == 'first_cmc_oa':
        return 'yes' if CMC_RE.search(text) else 'no'
    if domain == 'scaphoid_fracture':
        label = scaphoid_anatomy_class(text)
        return 'uncertain' if label == 'ambiguous' else label
    raise ValueError(f'unsupported domain: {domain}')


def predict_scaphoid_binary_state(diagnosis_text='', complaint_text='', physical_exam_text=''):
    """Return the frozen v0.3 binary scaphoid-state baseline.

    This intentionally uses non-operative clinical text only. It does not attempt
    to infer the finer physician multi-class state when documentation is absent.
    """
    text = _join(diagnosis_text, complaint_text, physical_exam_text)
    if SCAPHOID_CHRONIC_RE.search(text):
        return 'established_chronic_or_nonunion'
    return 'not_established_chronic_or_nonunion'


def predict_procedure_labels(domain, operation_name_text='', operation_note_text=''):
    text = _join(operation_name_text, operation_note_text)
    patterns = PROCEDURE_PATTERNS.get(domain)
    if patterns is None:
        raise ValueError(f'unsupported domain: {domain}')
    return {label for label, pattern in patterns.items() if pattern.search(text)}


def _read(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def _write(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


def build(annotation_dir: Path, output_dir: Path):
    disease_rows = []
    for row in _read(annotation_dir / 'disease_anatomy_annotation.csv'):
        disease_rows.append({
            'study_id': row['study_id'],
            'domain': row['domain'],
            'pred_disease_anatomy_label': predict_disease_anatomy(
                row['domain'],
                row.get('diagnosis_text', ''),
                row.get('complaint_text', ''),
                row.get('physical_exam_text', ''),
            ),
        })
    _write(
        output_dir / 'deterministic_disease_anatomy_predictions.csv',
        disease_rows,
        ['study_id', 'domain', 'pred_disease_anatomy_label'],
    )

    state_rows = []
    for row in _read(annotation_dir / 'scaphoid_state_annotation.csv'):
        state_rows.append({
            'study_id': row['study_id'],
            'pred_scaphoid_state_binary': predict_scaphoid_binary_state(
                row.get('diagnosis_text', ''),
                row.get('complaint_text', ''),
                row.get('physical_exam_text', ''),
            ),
        })
    _write(
        output_dir / 'deterministic_scaphoid_state_binary_predictions.csv',
        state_rows,
        ['study_id', 'pred_scaphoid_state_binary'],
    )

    procedure_rows = []
    for row in _read(annotation_dir / 'procedure_annotation.csv'):
        labels = sorted(predict_procedure_labels(
            row['domain'],
            row.get('operation_name_text', ''),
            row.get('operation_note_text', ''),
        ))
        procedure_rows.append({
            'study_id': row['study_id'],
            'domain': row['domain'],
            'pred_procedure_labels': '|'.join(labels),
        })
    _write(
        output_dir / 'deterministic_procedure_predictions.csv',
        procedure_rows,
        ['study_id', 'domain', 'pred_procedure_labels'],
    )


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--annotation-dir', required=True)
    ap.add_argument('--output-dir', required=True)
    args = ap.parse_args()
    build(Path(args.annotation_dir), Path(args.output_dir))
