#!/usr/bin/env python3
"""Official scoring entrypoint for a cryptographically frozen reference standard."""
from __future__ import annotations

from pathlib import Path
import argparse
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from freeze_reference_standard import verify_manifest
from evaluate_reference_benchmark import build
from evaluate_hallux_baseline import evaluate as evaluate_hallux_baseline


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--gold-dir',required=True)
    ap.add_argument('--freeze-manifest',required=True)
    ap.add_argument('--pred-dir',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()

    gold_dir=Path(args.gold_dir)
    pred_dir=Path(args.pred_dir)
    verify_manifest(gold_dir,Path(args.freeze_manifest))
    metrics=build(gold_dir,pred_dir)
    metrics['hallux_baseline']=evaluate_hallux_baseline(
        gold_dir/'disease_anatomy_annotation.csv',
        pred_dir/'rule_disease_anatomy_predictions.csv',
    )
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'scored frozen reference standard: {out}')
