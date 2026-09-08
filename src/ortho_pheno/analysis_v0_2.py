#!/usr/bin/env python3
"""Current aggregate analysis entrypoint for phenotype v0.3.

This wrapper deliberately reuses the privacy-preserving output machinery in
``analysis_v0_1`` while replacing its historical scaphoid cohort constructor
with the frozen v0.3 anatomy rules. Keeping the historical module intact makes
rule-version changes auditable while ensuring current results are regenerated
from the same cohort logic used elsewhere in the repository.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_v0_1 as base
from rules import HALLUX_RE, CMC_RE, is_wrist_scaphoid


def strict_sets_v0_3(recs):
    """Return strict admission sets using the frozen phenotype-v0.3 rules."""
    out = {k: set() for k in base.DISEASES}
    for domain, records in recs.items():
        for admission_key, record in records.items():
            text = base.all_text(record)
            if domain == 'hallux_valgus' and HALLUX_RE.search(text):
                out[domain].add(admission_key)
            elif domain == 'first_cmc_oa' and CMC_RE.search(text):
                out[domain].add(admission_key)
            elif domain == 'scaphoid_fracture' and is_wrist_scaphoid(text):
                out[domain].add(admission_key)
    return out


def build_outputs(raw_dir: Path, out_dir: Path):
    # Replace the historical constructor only for this versioned entrypoint.
    base.strict_sets = strict_sets_v0_3
    return base.build_outputs(raw_dir, out_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw-dir', required=True)
    parser.add_argument('--out-dir', required=True)
    args = parser.parse_args()
    build_outputs(Path(args.raw_dir), Path(args.out_dir))
