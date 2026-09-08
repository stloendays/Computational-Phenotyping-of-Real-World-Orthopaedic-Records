#!/usr/bin/env python3
"""Current private post-Gold figure entrypoint for the focused scaphoid paper.

Uses the tested plotting functions from v0.1 but fixes manuscript output names and
requires an explicitly supplied output directory (recommended: `outputs/private/`).
Final figures can contain small-group counts or individual duration points and are
therefore private until manuscript/privacy review is complete.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import json

from build_scaph_final_figures_v0_1 import (
    load_gold,
    cohort_counts,
    figure1_cohort_flow,
    figure2_composition,
    duration_points,
    figure3_duration,
)


def build(review_dir: Path, private_analysis_json: Path, output_dir: Path):
    anatomy, state, procedure = load_gold(review_dir)
    result = json.loads(private_analysis_json.read_text(encoding='utf-8'))
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        'figure1': output_dir / 'Figure1_physician_cohort_flow.svg',
        'figure2': output_dir / 'Figure2_operative_composition.svg',
        'figure3': output_dir / 'Figure3_duration_by_graft.svg',
    }
    figure1_cohort_flow(cohort_counts(anatomy, state, procedure), paths['figure1'])
    figure2_composition(result, paths['figure2'])
    figure3_duration(duration_points(state, procedure), paths['figure3'])
    return paths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--review-dir', required=True)
    ap.add_argument('--private-analysis-json', required=True)
    ap.add_argument('--output-dir', required=True)
    args = ap.parse_args()
    paths = build(Path(args.review_dir), Path(args.private_analysis_json), Path(args.output_dir))
    for key, path in paths.items():
        print(f'{key}: {path}')


if __name__ == '__main__':
    main()
