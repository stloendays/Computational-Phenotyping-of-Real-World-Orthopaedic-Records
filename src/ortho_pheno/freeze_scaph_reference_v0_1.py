#!/usr/bin/env python3
"""Validate and cryptographically freeze the scaphoid physician reference standard.

This tool is intentionally independent of the clinical extraction/model code. It
checks controlled vocabularies, duration-field consistency, procedure-label
consistency, row uniqueness, and reviewer-2 subset completion before generating a
SHA-256 manifest.

The manifest contains file names, row counts, and hashes only. It never contains
study IDs, labels, or clinical text.
"""
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import argparse
import csv
import hashlib
import json

ANATOMY_ALLOWED = {'wrist_scaphoid','foot_navicular','other','uncertain'}
STATE_ALLOWED = {
    'acute_or_new_fracture',
    'established_chronic_fracture',
    'established_nonunion',
    'chronic_nonunion_not_distinguishable',
    'insufficient_or_uncertain',
}
DURATION_PRESENT_ALLOWED = {'yes','no','uncertain'}
DURATION_UNIT_ALLOWED = {'hours','days','weeks','months','years'}
DURATION_BASIS_ALLOWED = {'injury_since_event','wrist_symptom_duration','both','uncertain'}
RELEVANCE_ALLOWED = {'yes','no','uncertain'}
COMPONENT_ALLOWED = {'yes','no','uncertain'}

PRIMARY_FILES = (
    'scaphoid_anatomy_review.csv',
    'scaphoid_state_review.csv',
    'scaphoid_procedure_review.csv',
)
REVIEWER2_FILES = (
    'scaphoid_anatomy_review_reviewer2.csv',
    'scaphoid_state_review_reviewer2.csv',
    'scaphoid_procedure_review_reviewer2.csv',
)


def read_rows(path: Path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def sha256_file(path: Path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def require_unique_ids(rows, file_name):
    ids = [row.get('study_id','').strip() for row in rows]
    if any(not sid for sid in ids):
        raise ValueError(f'{file_name}: blank study_id')
    if len(ids) != len(set(ids)):
        raise ValueError(f'{file_name}: duplicate study_id')


def validate_duration_fields(row, prefix, context):
    present = row.get(f'{prefix}gold_relevant_duration_present','').strip()
    value = row.get(f'{prefix}gold_relevant_duration_value','').strip()
    unit = row.get(f'{prefix}gold_relevant_duration_unit','').strip()
    basis = row.get(f'{prefix}gold_duration_basis','').strip()

    if present not in DURATION_PRESENT_ALLOWED:
        raise ValueError(f'{context}: invalid/blank duration-present label {present!r}')

    if present == 'yes':
        try:
            numeric = float(value)
        except Exception as exc:
            raise ValueError(f'{context}: duration present=yes requires numeric value') from exc
        if not numeric > 0:
            raise ValueError(f'{context}: duration value must be > 0')
        if unit not in DURATION_UNIT_ALLOWED:
            raise ValueError(f'{context}: invalid duration unit {unit!r}')
        if basis not in DURATION_BASIS_ALLOWED:
            raise ValueError(f'{context}: invalid duration basis {basis!r}')
    elif present == 'no':
        if value or unit or basis:
            raise ValueError(f'{context}: duration present=no requires blank value/unit/basis')
    else:  # uncertain
        if value or unit:
            raise ValueError(f'{context}: duration present=uncertain requires blank value/unit')
        if basis not in ('', 'uncertain'):
            raise ValueError(f'{context}: uncertain duration may only have blank/uncertain basis')


def validate_anatomy(rows, prefix=''):
    require_unique_ids(rows, f'{prefix or "primary"} anatomy')
    field = f'{prefix}gold_anatomy_label'
    for i,row in enumerate(rows,2):
        label = row.get(field,'').strip()
        if label not in ANATOMY_ALLOWED:
            raise ValueError(f'anatomy row {i}: invalid/blank label {label!r}')


def validate_state(rows, prefix=''):
    require_unique_ids(rows, f'{prefix or "primary"} state')
    field = f'{prefix}gold_scaphoid_state'
    for i,row in enumerate(rows,2):
        label = row.get(field,'').strip()
        if label not in STATE_ALLOWED:
            raise ValueError(f'state row {i}: invalid/blank state {label!r}')
        validate_duration_fields(row, prefix, f'state row {i}')


def validate_procedure(rows, prefix=''):
    require_unique_ids(rows, f'{prefix or "primary"} procedure')
    relevance_field = f'{prefix}gold_target_disease_procedure_present'
    component_fields = [
        f'{prefix}gold_internal_fixation',
        f'{prefix}gold_bone_graft',
        f'{prefix}gold_reconstruction',
        f'{prefix}gold_fusion',
    ]
    for i,row in enumerate(rows,2):
        relevance = row.get(relevance_field,'').strip()
        if relevance not in RELEVANCE_ALLOWED:
            raise ValueError(f'procedure row {i}: invalid/blank relevance {relevance!r}')
        values = [row.get(field,'').strip() for field in component_fields]
        if relevance == 'yes':
            bad = [v for v in values if v not in COMPONENT_ALLOWED]
            if bad:
                raise ValueError(f'procedure row {i}: relevance=yes requires yes/no/uncertain for every component')
        else:
            if any(values):
                raise ValueError(f'procedure row {i}: component labels must be blank when relevance is not yes')


def ensure_subset(primary_rows, reviewer2_rows, layer):
    primary_ids = {r['study_id'].strip() for r in primary_rows}
    reviewer2_ids = {r['study_id'].strip() for r in reviewer2_rows}
    if not reviewer2_ids <= primary_ids:
        raise ValueError(f'{layer}: reviewer-2 IDs are not a subset of primary review IDs')
    if not reviewer2_ids:
        raise ValueError(f'{layer}: reviewer-2 packet is empty')


def build_manifest(review_dir: Path):
    paths = {name: review_dir / name for name in PRIMARY_FILES + REVIEWER2_FILES}
    missing = [name for name,path in paths.items() if not path.exists()]
    if missing:
        raise FileNotFoundError(f'missing reference-standard files: {missing}')

    rows = {name: read_rows(path) for name,path in paths.items()}

    validate_anatomy(rows['scaphoid_anatomy_review.csv'])
    validate_state(rows['scaphoid_state_review.csv'])
    validate_procedure(rows['scaphoid_procedure_review.csv'])

    validate_anatomy(rows['scaphoid_anatomy_review_reviewer2.csv'], prefix='reviewer2_')
    validate_state(rows['scaphoid_state_review_reviewer2.csv'], prefix='reviewer2_')
    validate_procedure(rows['scaphoid_procedure_review_reviewer2.csv'], prefix='reviewer2_')

    ensure_subset(rows['scaphoid_anatomy_review.csv'], rows['scaphoid_anatomy_review_reviewer2.csv'], 'anatomy')
    ensure_subset(rows['scaphoid_state_review.csv'], rows['scaphoid_state_review_reviewer2.csv'], 'state')
    ensure_subset(rows['scaphoid_procedure_review.csv'], rows['scaphoid_procedure_review_reviewer2.csv'], 'procedure')

    if len(rows['scaphoid_anatomy_review.csv']) != 88:
        raise ValueError('Stage-1 anatomy Gold must retain all 88 frozen candidate rows')

    return {
        'manifest_version':'scaphoid-reference-v0.1',
        'reference_standard_status':'frozen',
        'study_design':'two-stage physician-defined scaphoid cohort',
        'analysis_plan':'SCAPHOID_ANALYSIS_PLAN_V0_3',
        'duration_secondary_hypothesis':'SCAPHOID_DURATION_SECONDARY_HYPOTHESIS_V0_1',
        'created_at_utc':datetime.now(timezone.utc).isoformat(),
        'files':{
            name:{
                'row_count':len(rows[name]),
                'sha256':sha256_file(paths[name]),
            }
            for name in PRIMARY_FILES + REVIEWER2_FILES
        },
    }


def verify_manifest(review_dir: Path, manifest_path: Path):
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('reference_standard_status') != 'frozen':
        raise ValueError('reference standard manifest is not frozen')
    for name,meta in manifest.get('files',{}).items():
        path = review_dir / name
        if not path.exists():
            raise FileNotFoundError(name)
        if sha256_file(path) != meta.get('sha256'):
            raise ValueError(f'reference-standard hash mismatch: {name}')
    return True


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--review-dir', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    manifest = build_manifest(Path(args.review_dir))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'frozen scaphoid reference standard: {out}')
