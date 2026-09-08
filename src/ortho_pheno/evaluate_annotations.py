#!/usr/bin/env python3
"""Evaluate frozen phenotype annotations against extraction-system predictions.

This module is independent of the raw EHR parser. It operates on study IDs and
labels and writes aggregate metrics only.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import argparse, csv, json


def _safe_div(a, b):
    return a / b if b else 0.0


def cohen_kappa(a, b):
    if len(a) != len(b):
        raise ValueError('label vectors must have equal length')
    if not a:
        return 0.0
    labels = sorted(set(a) | set(b))
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    expected = sum((ca[l] / n) * (cb[l] / n) for l in labels)
    return _safe_div(observed - expected, 1.0 - expected) if expected < 1 else 1.0


def categorical_metrics(gold, pred, positive_label=None):
    if len(gold) != len(pred):
        raise ValueError('gold and prediction vectors must have equal length')
    labels = sorted(set(gold) | set(pred))
    per_label = {}
    for label in labels:
        tp = sum(g == label and p == label for g, p in zip(gold, pred))
        fp = sum(g != label and p == label for g, p in zip(gold, pred))
        fn = sum(g == label and p != label for g, p in zip(gold, pred))
        tn = len(gold) - tp - fp - fn
        precision = _safe_div(tp, tp + fp)
        recall = _safe_div(tp, tp + fn)
        f1 = _safe_div(2 * precision * recall, precision + recall)
        per_label[label] = {
            'support': tp + fn, 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn,
            'precision': precision, 'recall': recall, 'f1': f1,
        }
    accuracy = _safe_div(sum(g == p for g, p in zip(gold, pred)), len(gold))
    macro_f1 = _safe_div(sum(v['f1'] for v in per_label.values()), len(per_label))
    out = {'n': len(gold), 'accuracy': accuracy, 'macro_f1': macro_f1,
           'cohen_kappa': cohen_kappa(gold, pred), 'per_label': per_label}
    if positive_label is not None:
        if positive_label not in per_label:
            raise ValueError(f'positive label {positive_label!r} not present')
        m = per_label[positive_label]
        out.update({
            'binary_positive_label': positive_label,
            'sensitivity': m['recall'],
            'specificity': _safe_div(m['tn'], m['tn'] + m['fp']),
            'ppv': m['precision'],
            'npv': _safe_div(m['tn'], m['tn'] + m['fn']),
            'f1': m['f1'],
        })
    return out


def _parse_multilabel(value):
    if value is None or not value.strip():
        return set()
    return {x.strip() for x in value.split('|') if x.strip()}


def multilabel_metrics(gold_sets, pred_sets, label_space=None):
    if len(gold_sets) != len(pred_sets):
        raise ValueError('gold and prediction vectors must have equal length')
    if label_space is None:
        label_space = sorted(set().union(*gold_sets, *pred_sets)) if gold_sets else []
    else:
        label_space = list(label_space)
    per_label = {}; total_tp = total_fp = total_fn = 0
    for label in label_space:
        tp = sum(label in g and label in p for g, p in zip(gold_sets, pred_sets))
        fp = sum(label not in g and label in p for g, p in zip(gold_sets, pred_sets))
        fn = sum(label in g and label not in p for g, p in zip(gold_sets, pred_sets))
        precision = _safe_div(tp, tp + fp); recall = _safe_div(tp, tp + fn)
        f1 = _safe_div(2 * precision * recall, precision + recall)
        per_label[label] = {'support': tp + fn, 'tp': tp, 'fp': fp, 'fn': fn,
                            'precision': precision, 'recall': recall, 'f1': f1}
        total_tp += tp; total_fp += fp; total_fn += fn
    micro_precision = _safe_div(total_tp, total_tp + total_fp)
    micro_recall = _safe_div(total_tp, total_tp + total_fn)
    micro_f1 = _safe_div(2 * micro_precision * micro_recall, micro_precision + micro_recall)
    macro_f1 = _safe_div(sum(v['f1'] for v in per_label.values()), len(per_label))
    exact = _safe_div(sum(g == p for g, p in zip(gold_sets, pred_sets)), len(gold_sets))
    cardinality_error = _safe_div(sum(abs(len(g) - len(p)) for g, p in zip(gold_sets, pred_sets)), len(gold_sets))
    return {
        'n': len(gold_sets), 'labels': label_space,
        'micro_precision': micro_precision, 'micro_recall': micro_recall,
        'micro_f1': micro_f1, 'macro_f1': macro_f1,
        'exact_set_match': exact,
        'mean_absolute_label_cardinality_error': cardinality_error,
        'per_label': per_label,
    }


def _load_joined(gold_path, pred_path, id_col, label_col):
    def load(path):
        with open(path, encoding='utf-8-sig', newline='') as f:
            rows = list(csv.DictReader(f))
        out = {}
        for r in rows:
            sid = r[id_col].strip()
            if sid in out:
                raise ValueError(f'duplicate study_id in {path}: {sid}')
            out[sid] = r[label_col].strip()
        return out
    g, p = load(gold_path), load(pred_path)
    common = sorted(set(g) & set(p))
    if not common:
        raise ValueError('no overlapping study IDs')
    return common, g, p, sorted(set(g)-set(p)), sorted(set(p)-set(g))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gold', required=True)
    ap.add_argument('--pred', required=True)
    ap.add_argument('--id-col', default='study_id')
    ap.add_argument('--label-col', required=True)
    ap.add_argument('--mode', choices=['categorical','multilabel'], required=True)
    ap.add_argument('--positive-label')
    ap.add_argument('--labels', help='pipe-separated fixed multilabel vocabulary')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    common, g, p, missing_pred, extra_pred = _load_joined(args.gold, args.pred, args.id_col, args.label_col)
    if args.mode == 'categorical':
        metrics = categorical_metrics([g[x] for x in common], [p[x] for x in common], args.positive_label)
    else:
        labels = args.labels.split('|') if args.labels else None
        metrics = multilabel_metrics([_parse_multilabel(g[x]) for x in common], [_parse_multilabel(p[x]) for x in common], labels)
    metrics['matched_ids'] = len(common)
    metrics['missing_prediction_ids'] = len(missing_pred)
    metrics['extra_prediction_ids'] = len(extra_pred)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
