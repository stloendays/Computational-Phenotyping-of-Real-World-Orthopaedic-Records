#!/usr/bin/env python3
"""Build LOCAL-ONLY adjudication templates for the scaphoid physician review.

Reviewer-1 and Reviewer-2 files are preserved unchanged. Final Gold labels are
written to separate adjudication files so inter-rater agreement remains fully
reconstructable after disagreements are resolved.

For records without second review, the Reviewer-1 label is copied into final Gold.
For double-reviewed records with complete agreement, the agreed label set is copied.
For any disagreement, final Gold fields are left blank and require adjudication.

All outputs contain pseudonymous study IDs and must remain private.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import csv


def read_rows(path: Path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


def unique_map(rows, filename):
    out = {}
    for i, row in enumerate(rows, 2):
        sid = row.get('study_id', '').strip()
        if not sid:
            raise ValueError(f'{filename} row {i}: blank study_id')
        if sid in out:
            raise ValueError(f'{filename}: duplicate study_id {sid}')
        out[sid] = row
    return out


def build_anatomy(review_dir: Path):
    primary = read_rows(review_dir / 'scaphoid_anatomy_review.csv')
    reviewer2 = unique_map(read_rows(review_dir / 'scaphoid_anatomy_review_reviewer2.csv'), 'anatomy reviewer2')
    rows = []
    for row in primary:
        sid = row['study_id'].strip()
        r1 = row.get('gold_anatomy_label', '').strip()
        r2 = reviewer2.get(sid, {}).get('reviewer2_gold_anatomy_label', '').strip()
        double = sid in reviewer2
        agree = (not double) or (r1 == r2 and bool(r1))
        rows.append({
            'study_id': sid,
            'reviewer1_anatomy_label': r1,
            'reviewer2_anatomy_label': r2,
            'double_reviewed': 'yes' if double else 'no',
            'reviewer_agreement': 'yes' if agree else 'no',
            'gold_anatomy_label': r1 if agree else '',
            'adjudicator_comment': '',
        })
    out = review_dir / 'scaphoid_anatomy_adjudicated.csv'
    write_rows(out, rows, list(rows[0]))
    return out, len(rows), sum(r['reviewer_agreement'] == 'no' for r in rows)


def _all_equal(primary_row, reviewer2_row, pairs):
    for pfield, r2field in pairs:
        if primary_row.get(pfield, '').strip() != reviewer2_row.get(r2field, '').strip():
            return False
    return True


def build_state(review_dir: Path):
    primary = read_rows(review_dir / 'scaphoid_state_review.csv')
    reviewer2 = unique_map(read_rows(review_dir / 'scaphoid_state_review_reviewer2.csv'), 'state reviewer2')
    pairs = [
        ('gold_scaphoid_state', 'reviewer2_gold_scaphoid_state'),
        ('gold_relevant_duration_present', 'reviewer2_gold_relevant_duration_present'),
        ('gold_relevant_duration_value', 'reviewer2_gold_relevant_duration_value'),
        ('gold_relevant_duration_unit', 'reviewer2_gold_relevant_duration_unit'),
        ('gold_duration_basis', 'reviewer2_gold_duration_basis'),
    ]
    rows = []
    for row in primary:
        sid = row['study_id'].strip()
        r2row = reviewer2.get(sid)
        double = r2row is not None
        agree = (not double) or _all_equal(row, r2row, pairs)
        outrow = {
            'study_id': sid,
            'reviewer1_scaphoid_state': row.get('gold_scaphoid_state', '').strip(),
            'reviewer2_scaphoid_state': r2row.get('reviewer2_gold_scaphoid_state', '').strip() if double else '',
            'double_reviewed': 'yes' if double else 'no',
            'reviewer_agreement': 'yes' if agree else 'no',
            'gold_scaphoid_state': row.get('gold_scaphoid_state', '').strip() if agree else '',
            'gold_relevant_duration_present': row.get('gold_relevant_duration_present', '').strip() if agree else '',
            'gold_relevant_duration_value': row.get('gold_relevant_duration_value', '').strip() if agree else '',
            'gold_relevant_duration_unit': row.get('gold_relevant_duration_unit', '').strip() if agree else '',
            'gold_duration_basis': row.get('gold_duration_basis', '').strip() if agree else '',
            'adjudicator_comment': '',
        }
        rows.append(outrow)
    out = review_dir / 'scaphoid_state_adjudicated.csv'
    write_rows(out, rows, list(rows[0]))
    return out, len(rows), sum(r['reviewer_agreement'] == 'no' for r in rows)


def build_procedure(review_dir: Path):
    primary = read_rows(review_dir / 'scaphoid_procedure_review.csv')
    reviewer2 = unique_map(read_rows(review_dir / 'scaphoid_procedure_review_reviewer2.csv'), 'procedure reviewer2')
    pairs = [
        ('gold_target_disease_procedure_present', 'reviewer2_gold_target_disease_procedure_present'),
        ('gold_internal_fixation', 'reviewer2_gold_internal_fixation'),
        ('gold_bone_graft', 'reviewer2_gold_bone_graft'),
        ('gold_reconstruction', 'reviewer2_gold_reconstruction'),
        ('gold_fusion', 'reviewer2_gold_fusion'),
    ]
    rows = []
    for row in primary:
        sid = row['study_id'].strip()
        r2row = reviewer2.get(sid)
        double = r2row is not None
        agree = (not double) or _all_equal(row, r2row, pairs)
        rows.append({
            'study_id': sid,
            'reviewer1_target_disease_procedure_present': row.get('gold_target_disease_procedure_present', '').strip(),
            'reviewer2_target_disease_procedure_present': r2row.get('reviewer2_gold_target_disease_procedure_present', '').strip() if double else '',
            'double_reviewed': 'yes' if double else 'no',
            'reviewer_agreement': 'yes' if agree else 'no',
            'gold_target_disease_procedure_present': row.get('gold_target_disease_procedure_present', '').strip() if agree else '',
            'gold_internal_fixation': row.get('gold_internal_fixation', '').strip() if agree else '',
            'gold_bone_graft': row.get('gold_bone_graft', '').strip() if agree else '',
            'gold_reconstruction': row.get('gold_reconstruction', '').strip() if agree else '',
            'gold_fusion': row.get('gold_fusion', '').strip() if agree else '',
            'adjudicator_comment': '',
        })
    out = review_dir / 'scaphoid_procedure_adjudicated.csv'
    write_rows(out, rows, list(rows[0]))
    return out, len(rows), sum(r['reviewer_agreement'] == 'no' for r in rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--review-dir', required=True)
    ap.add_argument('--layer', choices=('anatomy', 'state', 'procedure', 'all'), default='all')
    args = ap.parse_args()
    review_dir = Path(args.review_dir)
    builders = {'anatomy': build_anatomy, 'state': build_state, 'procedure': build_procedure}
    selected = builders if args.layer == 'all' else {args.layer: builders[args.layer]}
    for name, builder in selected.items():
        path, n, disagreements = builder(review_dir)
        print(f'{name}: rows={n}; rows_requiring_adjudication={disagreements}; output={path}')


if __name__ == '__main__':
    main()
