#!/usr/bin/env python3
"""Validate and cryptographically freeze the scaphoid-only physician reference standard.

The main paper uses a two-stage physician-defined cohort. Reviewer-1, Reviewer-2
and adjudicated Gold files remain separate so inter-rater agreement is preserved.
The public manifest stores file names, row counts and SHA-256 hashes only.

`build_manifest()` is retained only as a backward-compatible validator for the
historical single-stage test fixture. The manuscript workflow must use
`build_stage1_manifest()` and `build_final_manifest()`.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import argparse
import csv
import hashlib
import json

ANATOMY_ALLOWED = {'wrist_scaphoid', 'foot_navicular', 'other', 'uncertain'}
STATE_ALLOWED = {
    'acute_or_new_fracture',
    'established_chronic_fracture',
    'established_nonunion',
    'chronic_nonunion_not_distinguishable',
    'insufficient_or_uncertain',
}
YES_NO_UNCERTAIN = {'yes', 'no', 'uncertain'}
DURATION_UNITS = {'hours', 'days', 'weeks', 'months', 'years'}
DURATION_BASIS = {'injury_since_event', 'wrist_symptom_duration', 'both', 'uncertain'}

STAGE1_PRIMARY = 'scaphoid_anatomy_review.csv'
STAGE1_REVIEWER2 = 'scaphoid_anatomy_review_reviewer2.csv'
STAGE1_MANIFEST = 'scaphoid_anatomy_double_review_manifest.csv'
STAGE1_FINAL = 'scaphoid_anatomy_adjudicated.csv'
STATE_PRIMARY = 'scaphoid_state_review.csv'
STATE_REVIEWER2 = 'scaphoid_state_review_reviewer2.csv'
PROCEDURE_PRIMARY = 'scaphoid_procedure_review.csv'
PROCEDURE_REVIEWER2 = 'scaphoid_procedure_review_reviewer2.csv'
DOWNSTREAM_MANIFEST = 'scaphoid_downstream_double_review_manifest.csv'
STATE_FINAL = 'scaphoid_state_adjudicated.csv'
PROCEDURE_FINAL = 'scaphoid_procedure_adjudicated.csv'


def read_rows(path: Path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def sha256_file(path: Path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def require_unique_ids(rows, filename):
    ids = [r.get('study_id', '').strip() for r in rows]
    if any(not x for x in ids):
        raise ValueError(f'{filename}: blank study_id')
    if len(ids) != len(set(ids)):
        raise ValueError(f'{filename}: duplicate study_id')
    return set(ids)


def require_allowed(value, allowed, context):
    if value not in allowed:
        raise ValueError(f'{context}: invalid/blank value {value!r}')


def validate_duration(row, prefix, context):
    present = row.get(f'{prefix}relevant_duration_present', '').strip()
    value = row.get(f'{prefix}relevant_duration_value', '').strip()
    unit = row.get(f'{prefix}relevant_duration_unit', '').strip()
    basis = row.get(f'{prefix}duration_basis', '').strip()
    require_allowed(present, YES_NO_UNCERTAIN, f'{context} duration-present')
    if present == 'yes':
        try:
            numeric = float(value)
        except ValueError as exc:
            raise ValueError(f'{context}: duration value must be numeric') from exc
        if numeric <= 0:
            raise ValueError(f'{context}: duration value must be >0')
        require_allowed(unit, DURATION_UNITS, f'{context} duration-unit')
        require_allowed(basis, DURATION_BASIS - {'uncertain'}, f'{context} duration-basis')
    elif present == 'no':
        if value or unit or basis:
            raise ValueError(f'{context}: duration value/unit/basis must be blank when present=no')
    else:
        if value or unit:
            raise ValueError(f'{context}: duration value/unit must be blank when present=uncertain')
        if basis not in ('', 'uncertain'):
            raise ValueError(f'{context}: uncertain duration basis must be blank or uncertain')


def manifest_ids(rows, layer):
    ids = {r.get('study_id', '').strip() for r in rows if r.get('layer', '').strip() == layer}
    if '' in ids:
        raise ValueError(f'{layer} manifest: blank study_id')
    return ids


def validate_anatomy_primary(rows):
    ids = require_unique_ids(rows, STAGE1_PRIMARY)
    if len(rows) != 88:
        raise ValueError(f'{STAGE1_PRIMARY}: expected 88 rows, found {len(rows)}')
    for i, row in enumerate(rows, 2):
        require_allowed(row.get('gold_anatomy_label', '').strip(), ANATOMY_ALLOWED, f'{STAGE1_PRIMARY} row {i}')
    return ids


def validate_anatomy_reviewer2(rows, expected_ids):
    ids = require_unique_ids(rows, STAGE1_REVIEWER2)
    if ids != expected_ids:
        raise ValueError(f'{STAGE1_REVIEWER2}: IDs must exactly match the frozen double-review manifest')
    for i, row in enumerate(rows, 2):
        require_allowed(row.get('reviewer2_gold_anatomy_label', '').strip(), ANATOMY_ALLOWED,
                        f'{STAGE1_REVIEWER2} row {i}')


def validate_anatomy_final(rows, candidate_ids):
    ids = require_unique_ids(rows, STAGE1_FINAL)
    if ids != candidate_ids:
        raise ValueError(f'{STAGE1_FINAL}: IDs must equal all 88 broad candidates')
    for i, row in enumerate(rows, 2):
        require_allowed(row.get('gold_anatomy_label', '').strip(), ANATOMY_ALLOWED, f'{STAGE1_FINAL} row {i}')
    return ids


def validate_state_primary(rows, wrist_ids):
    ids = require_unique_ids(rows, STATE_PRIMARY)
    if ids != wrist_ids:
        raise ValueError(f'{STATE_PRIMARY}: IDs must equal physician-confirmed wrist-scaphoid IDs')
    for i, row in enumerate(rows, 2):
        require_allowed(row.get('gold_scaphoid_state', '').strip(), STATE_ALLOWED, f'{STATE_PRIMARY} row {i}')
        validate_duration(row, 'gold_', f'{STATE_PRIMARY} row {i}')
    return ids


def validate_state_reviewer2(rows, expected_ids):
    ids = require_unique_ids(rows, STATE_REVIEWER2)
    if ids != expected_ids:
        raise ValueError(f'{STATE_REVIEWER2}: IDs must exactly match the state double-review manifest')
    for i, row in enumerate(rows, 2):
        require_allowed(row.get('reviewer2_gold_scaphoid_state', '').strip(), STATE_ALLOWED,
                        f'{STATE_REVIEWER2} row {i}')
        validate_duration(row, 'reviewer2_gold_', f'{STATE_REVIEWER2} row {i}')


def validate_procedure_row(row, prefix, context):
    rel = row.get(f'{prefix}target_disease_procedure_present', '').strip()
    require_allowed(rel, YES_NO_UNCERTAIN, f'{context} relevance')
    fields = ('internal_fixation', 'bone_graft', 'reconstruction', 'fusion')
    values = [row.get(f'{prefix}{name}', '').strip() for name in fields]
    if rel == 'yes':
        for name, value in zip(fields, values):
            require_allowed(value, YES_NO_UNCERTAIN, f'{context} {name}')
    elif any(values):
        raise ValueError(f'{context}: procedure components must be blank unless relevance=yes')


def validate_procedure_primary(rows, wrist_ids):
    ids = require_unique_ids(rows, PROCEDURE_PRIMARY)
    if not ids.issubset(wrist_ids):
        raise ValueError(f'{PROCEDURE_PRIMARY}: contains non-wrist study IDs')
    for i, row in enumerate(rows, 2):
        validate_procedure_row(row, 'gold_', f'{PROCEDURE_PRIMARY} row {i}')
    return ids


def validate_procedure_reviewer2(rows, expected_ids):
    ids = require_unique_ids(rows, PROCEDURE_REVIEWER2)
    if ids != expected_ids:
        raise ValueError(f'{PROCEDURE_REVIEWER2}: IDs must exactly match the procedure double-review manifest')
    for i, row in enumerate(rows, 2):
        validate_procedure_row(row, 'reviewer2_gold_', f'{PROCEDURE_REVIEWER2} row {i}')


def validate_state_final(rows, wrist_ids):
    ids = require_unique_ids(rows, STATE_FINAL)
    if ids != wrist_ids:
        raise ValueError(f'{STATE_FINAL}: IDs must equal physician-confirmed wrist-scaphoid IDs')
    for i, row in enumerate(rows, 2):
        require_allowed(row.get('gold_scaphoid_state', '').strip(), STATE_ALLOWED, f'{STATE_FINAL} row {i}')
        validate_duration(row, 'gold_', f'{STATE_FINAL} row {i}')


def validate_procedure_final(rows, procedure_ids):
    ids = require_unique_ids(rows, PROCEDURE_FINAL)
    if ids != procedure_ids:
        raise ValueError(f'{PROCEDURE_FINAL}: IDs must equal the Stage-2 procedure-review population')
    for i, row in enumerate(rows, 2):
        validate_procedure_row(row, 'gold_', f'{PROCEDURE_FINAL} row {i}')


def file_meta(path, rows):
    return {'row_count': len(rows), 'sha256': sha256_file(path)}


def build_stage1_manifest(review_dir: Path):
    names = (STAGE1_PRIMARY, STAGE1_REVIEWER2, STAGE1_MANIFEST, STAGE1_FINAL)
    paths = {name: review_dir / name for name in names}
    missing = [name for name, path in paths.items() if not path.exists()]
    if missing:
        raise FileNotFoundError(f'missing Stage-1 files: {missing}')
    rows = {name: read_rows(path) for name, path in paths.items()}
    candidate_ids = validate_anatomy_primary(rows[STAGE1_PRIMARY])
    reviewer2_ids = manifest_ids(rows[STAGE1_MANIFEST], 'anatomy')
    validate_anatomy_reviewer2(rows[STAGE1_REVIEWER2], reviewer2_ids)
    validate_anatomy_final(rows[STAGE1_FINAL], candidate_ids)
    return {
        'manifest_version': 'scaphoid-stage1-v0.1',
        'reference_standard_status': 'stage1_frozen',
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'files': {name: file_meta(paths[name], rows[name]) for name in names},
    }


def build_final_manifest(review_dir: Path):
    names = (
        STAGE1_FINAL,
        STATE_PRIMARY, STATE_REVIEWER2,
        PROCEDURE_PRIMARY, PROCEDURE_REVIEWER2,
        DOWNSTREAM_MANIFEST,
        STATE_FINAL, PROCEDURE_FINAL,
    )
    paths = {name: review_dir / name for name in names}
    missing = [name for name, path in paths.items() if not path.exists()]
    if missing:
        raise FileNotFoundError(f'missing final-reference files: {missing}')
    rows = {name: read_rows(path) for name, path in paths.items()}

    anatomy_ids = require_unique_ids(rows[STAGE1_FINAL], STAGE1_FINAL)
    if len(anatomy_ids) != 88:
        raise ValueError(f'{STAGE1_FINAL}: expected 88 rows')
    wrist_ids = set()
    for i, row in enumerate(rows[STAGE1_FINAL], 2):
        label = row.get('gold_anatomy_label', '').strip()
        require_allowed(label, ANATOMY_ALLOWED, f'{STAGE1_FINAL} row {i}')
        if label == 'wrist_scaphoid':
            wrist_ids.add(row['study_id'].strip())

    validate_state_primary(rows[STATE_PRIMARY], wrist_ids)
    procedure_ids = validate_procedure_primary(rows[PROCEDURE_PRIMARY], wrist_ids)
    state_r2_ids = manifest_ids(rows[DOWNSTREAM_MANIFEST], 'state')
    procedure_r2_ids = manifest_ids(rows[DOWNSTREAM_MANIFEST], 'procedure')
    validate_state_reviewer2(rows[STATE_REVIEWER2], state_r2_ids)
    validate_procedure_reviewer2(rows[PROCEDURE_REVIEWER2], procedure_r2_ids)
    validate_state_final(rows[STATE_FINAL], wrist_ids)
    validate_procedure_final(rows[PROCEDURE_FINAL], procedure_ids)

    return {
        'manifest_version': 'scaphoid-final-v0.1',
        'reference_standard_status': 'final_frozen',
        'analysis_plan': 'SCAPHOID_ANALYSIS_PLAN_V0_2',
        'duration_secondary_hypothesis': 'SCAPHOID_DURATION_SECONDARY_HYPOTHESIS_V0_1',
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'files': {name: file_meta(paths[name], rows[name]) for name in names},
    }


def build_manifest(review_dir: Path):
    """Backward-compatible single-stage validator for historical tests only.

    This function intentionally does not implement the manuscript freeze. It is
    retained so old regression tests continue to verify field-level constraints
    and hash mutation detection. New paper workflows must use the stage-specific
    functions above.
    """
    names = (
        STAGE1_PRIMARY, STAGE1_REVIEWER2,
        STATE_PRIMARY, STATE_REVIEWER2,
        PROCEDURE_PRIMARY, PROCEDURE_REVIEWER2,
    )
    paths = {name: review_dir / name for name in names}
    missing = [name for name, path in paths.items() if not path.exists()]
    if missing:
        raise FileNotFoundError(f'missing legacy reference files: {missing}')
    rows = {name: read_rows(path) for name, path in paths.items()}

    candidate_ids = validate_anatomy_primary(rows[STAGE1_PRIMARY])
    r2_anatomy_ids = require_unique_ids(rows[STAGE1_REVIEWER2], STAGE1_REVIEWER2)
    if not r2_anatomy_ids.issubset(candidate_ids):
        raise ValueError('legacy anatomy reviewer-2 IDs must be a subset of primary IDs')
    for i, row in enumerate(rows[STAGE1_REVIEWER2], 2):
        require_allowed(row.get('reviewer2_gold_anatomy_label', '').strip(), ANATOMY_ALLOWED,
                        f'{STAGE1_REVIEWER2} row {i}')

    require_unique_ids(rows[STATE_PRIMARY], STATE_PRIMARY)
    for i, row in enumerate(rows[STATE_PRIMARY], 2):
        require_allowed(row.get('gold_scaphoid_state', '').strip(), STATE_ALLOWED, f'{STATE_PRIMARY} row {i}')
        validate_duration(row, 'gold_', f'{STATE_PRIMARY} row {i}')
    r2_state_ids = require_unique_ids(rows[STATE_REVIEWER2], STATE_REVIEWER2)
    if not r2_state_ids.issubset({r['study_id'].strip() for r in rows[STATE_PRIMARY]}):
        raise ValueError('legacy state reviewer-2 IDs must be a subset of primary IDs')
    for i, row in enumerate(rows[STATE_REVIEWER2], 2):
        require_allowed(row.get('reviewer2_gold_scaphoid_state', '').strip(), STATE_ALLOWED,
                        f'{STATE_REVIEWER2} row {i}')
        validate_duration(row, 'reviewer2_gold_', f'{STATE_REVIEWER2} row {i}')

    require_unique_ids(rows[PROCEDURE_PRIMARY], PROCEDURE_PRIMARY)
    for i, row in enumerate(rows[PROCEDURE_PRIMARY], 2):
        validate_procedure_row(row, 'gold_', f'{PROCEDURE_PRIMARY} row {i}')
    r2_proc_ids = require_unique_ids(rows[PROCEDURE_REVIEWER2], PROCEDURE_REVIEWER2)
    if not r2_proc_ids.issubset({r['study_id'].strip() for r in rows[PROCEDURE_PRIMARY]}):
        raise ValueError('legacy procedure reviewer-2 IDs must be a subset of primary IDs')
    for i, row in enumerate(rows[PROCEDURE_REVIEWER2], 2):
        validate_procedure_row(row, 'reviewer2_gold_', f'{PROCEDURE_REVIEWER2} row {i}')

    return {
        'manifest_version': 'scaphoid-reference-legacy-v0.1',
        'reference_standard_status': 'frozen',
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'files': {name: file_meta(paths[name], rows[name]) for name in names},
    }


def verify_manifest(review_dir: Path, manifest_path: Path):
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    for name, meta in manifest.get('files', {}).items():
        path = review_dir / name
        if not path.exists():
            raise FileNotFoundError(name)
        if sha256_file(path) != meta.get('sha256'):
            raise ValueError(f'hash mismatch: {name}')
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--review-dir', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--stage', choices=('stage1', 'final'), required=True)
    args = ap.parse_args()
    review_dir = Path(args.review_dir)
    manifest = build_stage1_manifest(review_dir) if args.stage == 'stage1' else build_final_manifest(review_dir)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'frozen {args.stage} reference standard: {out}')


if __name__ == '__main__':
    main()
