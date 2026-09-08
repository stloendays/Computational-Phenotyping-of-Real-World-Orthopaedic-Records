#!/usr/bin/env python3
"""Validate and cryptographically freeze the LOCAL physician reference standard.

The output manifest contains only file names, SHA-256 hashes and row counts. It
contains no study IDs, labels or clinical text and can therefore be archived as
an aggregate reproducibility artifact after local privacy review.
"""
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import argparse
import csv
import hashlib
import json

DISEASE_ALLOWED = {
    'hallux_valgus': {'yes','no','uncertain'},
    'scaphoid_fracture': {'wrist_scaphoid','foot_navicular','other','uncertain'},
    'first_cmc_oa': {'yes','no','uncertain'},
}
SCAPHOID_STATE_ALLOWED = {
    'acute_or_new_fracture','established_chronic_fracture','established_nonunion',
    'chronic_nonunion_not_distinguishable','insufficient_or_uncertain',
}
PROCEDURE_RELEVANCE_ALLOWED = {'yes','no','uncertain'}
PROCEDURE_LABELS = {
    'hallux_valgus': {'osteotomy','chevron','akin','scarf','fusion','k_wire','resection','soft_tissue'},
    'scaphoid_fracture': {'internal_fixation','bone_graft','reconstruction','fusion','hardware_removal','debridement'},
    'first_cmc_oa': {'trapeziectomy','tendon_procedure','ligament_procedure','arthroplasty','fusion'},
}
REQUIRED_FILES = (
    'disease_anatomy_annotation.csv',
    'scaphoid_state_annotation.csv',
    'procedure_annotation.csv',
)


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()


def read_rows(path: Path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))


def parse_set(v):
    return {x.strip() for x in (v or '').split('|') if x.strip()}


def require_unique_ids(rows,path):
    ids=[r.get('study_id','').strip() for r in rows]
    if any(not x for x in ids):
        raise ValueError(f'{path.name}: blank study_id')
    if len(ids)!=len(set(ids)):
        raise ValueError(f'{path.name}: duplicate study_id')


def validate_disease(rows):
    require_unique_ids(rows,Path('disease_anatomy_annotation.csv'))
    for i,row in enumerate(rows,2):
        domain=row.get('domain','').strip(); label=row.get('gold_disease_anatomy_label','').strip()
        if domain not in DISEASE_ALLOWED:
            raise ValueError(f'disease row {i}: unknown domain {domain!r}')
        if label not in DISEASE_ALLOWED[domain]:
            raise ValueError(f'disease row {i}: invalid/blank gold label {label!r} for {domain}')


def validate_state(rows):
    require_unique_ids(rows,Path('scaphoid_state_annotation.csv'))
    for i,row in enumerate(rows,2):
        label=row.get('gold_scaphoid_state','').strip()
        if label not in SCAPHOID_STATE_ALLOWED:
            raise ValueError(f'scaphoid-state row {i}: invalid/blank label {label!r}')


def validate_procedure(rows):
    require_unique_ids(rows,Path('procedure_annotation.csv'))
    for i,row in enumerate(rows,2):
        domain=row.get('domain','').strip(); rel=row.get('gold_target_disease_procedure_present','').strip()
        if domain not in PROCEDURE_LABELS:
            raise ValueError(f'procedure row {i}: unknown domain {domain!r}')
        if rel not in PROCEDURE_RELEVANCE_ALLOWED:
            raise ValueError(f'procedure row {i}: invalid/blank relevance {rel!r}')
        labels=parse_set(row.get('gold_procedure_labels',''))
        invalid=labels-PROCEDURE_LABELS[domain]
        if invalid:
            raise ValueError(f'procedure row {i}: invalid labels {sorted(invalid)}')
        if rel=='no' and labels:
            raise ValueError(f'procedure row {i}: relevance=no but target-disease procedure labels are present')


def build_manifest(gold_dir: Path):
    paths={name:gold_dir/name for name in REQUIRED_FILES}
    missing=[name for name,p in paths.items() if not p.exists()]
    if missing:
        raise FileNotFoundError(f'missing gold files: {missing}')
    rows={name:read_rows(p) for name,p in paths.items()}
    validate_disease(rows['disease_anatomy_annotation.csv'])
    validate_state(rows['scaphoid_state_annotation.csv'])
    validate_procedure(rows['procedure_annotation.csv'])
    return {
        'manifest_version':'v0.1',
        'reference_standard_status':'frozen',
        'annotation_protocol':'ANNOTATION_PROTOCOL_V0_2',
        'phenotype_dependency':'phenotypes_v0.3',
        'created_at_utc':datetime.now(timezone.utc).isoformat(),
        'files':{
            name:{'sha256':sha256_file(paths[name]),'row_count':len(rows[name])}
            for name in REQUIRED_FILES
        },
    }


def verify_manifest(gold_dir: Path, manifest_path: Path):
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('reference_standard_status')!='frozen':
        raise ValueError('reference standard manifest is not frozen')
    for name,meta in manifest.get('files',{}).items():
        p=gold_dir/name
        if not p.exists():
            raise FileNotFoundError(name)
        actual=sha256_file(p)
        if actual!=meta.get('sha256'):
            raise ValueError(f'gold file hash mismatch: {name}')
    return True


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--gold-dir',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    manifest=build_manifest(Path(args.gold_dir))
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'frozen reference standard: {out}')
