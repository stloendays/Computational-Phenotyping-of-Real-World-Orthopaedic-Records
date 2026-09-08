#!/usr/bin/env python3
"""Current scaphoid reference-standard freeze entrypoint.

The v0.1 validator contains the tested vocabulary/ID/hash logic. This wrapper keeps
that validation unchanged while aligning the frozen manifest metadata with the
current manuscript analysis plan (SCAPHOID_ANALYSIS_PLAN_V0_3).
"""
from __future__ import annotations

from pathlib import Path
import argparse
import json

from freeze_scaph_reference_v0_1 import (
    build_stage1_manifest as _build_stage1_manifest,
    build_final_manifest as _build_final_manifest,
    verify_manifest,
)


def build_stage1_manifest(review_dir: Path):
    manifest = _build_stage1_manifest(review_dir)
    manifest['analysis_plan'] = 'SCAPHOID_ANALYSIS_PLAN_V0_3'
    return manifest


def build_final_manifest(review_dir: Path):
    manifest = _build_final_manifest(review_dir)
    manifest['analysis_plan'] = 'SCAPHOID_ANALYSIS_PLAN_V0_3'
    manifest['primary_comparison'] = 'established_chronic_nonunion_vs_physician_confirmed_acute_new'
    manifest['primary_outcome'] = 'bone_graft_augmentation'
    return manifest


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
