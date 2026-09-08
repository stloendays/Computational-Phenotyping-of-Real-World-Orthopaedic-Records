#!/usr/bin/env python3
"""Generate the privacy-preserving v0.3 scaphoid anatomy audit.

Reads the local XLSX exports, reconstructs admission-level text internally, and
writes only aggregate wrist/foot/ambiguous counts. No admission identifiers or
clinical text are written.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import argparse
import csv
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_safe_release import DIRECT_IDS, disease_key_from_name, norm_id, read_xlsx
from rules import scaphoid_anatomy_class


def build(raw_dir: Path, output: Path):
    texts = defaultdict(list)
    for path in sorted(raw_dir.glob('*.xlsx')):
        if disease_key_from_name(path.name) != 'scaphoid_fracture':
            continue
        for _, _, rows in read_xlsx(path):
            for row in rows:
                admission_key = norm_id(row.get('住院id'))
                if not admission_key:
                    continue
                for key, value in row.items():
                    if key in DIRECT_IDS or value is None:
                        continue
                    if isinstance(value, str) and value.strip():
                        texts[admission_key].append(value.strip())

    counts = Counter(
        scaphoid_anatomy_class(' '.join(parts)) for parts in texts.values()
    )
    denominator = len(texts)
    roles = {
        'wrist_scaphoid': 'included_in_strict_wrist_scaphoid_analysis',
        'foot_navicular': 'excluded_from_wrist_scaphoid_analysis',
        'ambiguous': 'reserved_for_physician_adjudication',
    }
    rows = []
    for label in ('wrist_scaphoid', 'foot_navicular', 'ambiguous'):
        n = counts.get(label, 0)
        rows.append({
            'anatomy_class': label,
            'n': n,
            'candidate_denominator': denominator,
            'percent': f'{100*n/denominator:.1f}%' if denominator else '',
            'analysis_role': roles[label],
        })

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=['anatomy_class','n','candidate_denominator','percent','analysis_role'],
        )
        writer.writeheader()
        writer.writerows(rows)
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw-dir', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    build(Path(args.raw_dir), Path(args.output))
