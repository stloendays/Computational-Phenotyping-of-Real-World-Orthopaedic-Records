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
    out = {
        'n': len(gold), 'accuracy': accuracy, 'macro_f1': macro_f1,
        'cohen_kappa': cohen_kappa(gold, pred), 'per_label': per_label,
    }
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
        per_label[label] = {
            'support': tp + fn, 'tp': tp, 'fp': fp, 'fn': fn,
            'precision': precision, 'recall': recall, 'f1': f1,
        }
        total_tp += tp; total_fp += fp; total_fn += fn
    micro_precision = _safe_div(total_tp, total_tp + total_fp)
    micro_recall = _safe_div(total_tp, total_tp + total_fn)
    micro_f1 = _safe_div(2 * micro_precision * micro_recall, micro_precision + micro_recall)
    macro_f1 = _safe_div(sum(v['f1'] for v in per_label.values()), len(per_label))
    exact = _safe_div(sum(g == p for g, p in zip(gold_sets, pred_sets)), len(gold_sets))
    cardinality_error = _safe_div(
        sum(abs(len(g) - len(p)) for g, p in zip(gold_sets, pred_sets)), len(gold_sets)
    )
    return {
        'n': len(gold_sets), 'labels': label_space,
        'micro_precision': micro_precision, 'micro_recall': micro_recall,
        'micro_f1': micro_f1, 'macro_f1': macro_f1,
        'exact_set_match': exact,
        'mean_absolute_label_cardinality_error': cardinality_error,
        'per_label': per_label,
    }


def _load_label_file(path, id_col, label_col):
    with open(path, encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    out = {}
    for row in rows:
        sid = row[id_col].strip()
        if sid in out:
            raise ValueError(f'duplicate study_id in {path}: {sid}')
        out[sid] = row[label_col].strip()
    return out


def load_joined(gold_path, pred_path, id_col, gold_label_col, pred_label_col,
                gold_label_map=None):
    gold = _load_label_file(gold_path, id_col, gold_label_col)
    pred = _load_label_file(pred_path, id_col, pred_label_col)
    common = sorted(set(gold) & set(pred))
    if not common:
        raise ValueError('no overlapping study IDs')

    blank_gold_ids = [sid for sid in common if not gold[sid]]
    common = [sid for sid in common if gold[sid]]

    mapped_out_ids = []
    if gold_label_map is not None:
        mapped = {}
        for sid in common:
            label = gold[sid]
            if label not in gold_label_map:
                raise ValueError(f'gold label missing from supplied mapping: {label!r}')
            new_label = gold_label_map[label]
            if new_label is None:
                mapped_out_ids.append(sid)
            else:
                mapped[sid] = str(new_label)
        gold = mapped
        common = [sid for sid in common if sid in gold]

    if not common:
        raise ValueError('no evaluable study IDs after blank/mapping exclusions')

    return {
        'ids': common,
        'gold': gold,
        'pred': pred,
        'missing_prediction_ids': sorted(set(gold) - set(pred)),
        'extra_prediction_ids': sorted(set(pred) - set(gold)),
        'blank_gold_ids_excluded': blank_gold_ids,
        'mapped_out_gold_ids_excluded': mapped_out_ids,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gold', required=True)
    ap.add_argument('--pred', required=True)
    ap.add_argument('--id-col', default='study_id')
    ap.add_argument('--label-col', help='legacy shortcut when gold and prediction columns have the same name')
    ap.add_argument('--gold-label-col')
    ap.add_argument('--pred-label-col')
    ap.add_argument('--gold-map-json', help='JSON object mapping gold labels to evaluation labels; null excludes a class')
    ap.add_argument('--mode', choices=['categorical', 'multilabel'], required=True)
    ap.add_argument('--positive-label')
    ap.add_argument('--labels', help='pipe-separated fixed multilabel vocabulary')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    gold_col = args.gold_label_col or args.label_col
    pred_col = args.pred_label_col or args.label_col
    if not gold_col or not pred_col:
        ap.error('specify --gold-label-col and --pred-label-col, or use --label-col when names match')

    gold_map = json.loads(args.gold_map_json) if args.gold_map_json else None
    joined = load_joined(args.gold, args.pred, args.id_col, gold_col, pred_col, gold_map)
    ids = joined['ids']; gold = joined['gold']; pred = joined['pred']

    if args.mode == 'categorical':
        metrics = categorical_metrics([gold[x] for x in ids], [pred[x] for x in ids], args.positive_label)
    else:
        labels = args.labels.split('|') if args.labels else None
        metrics = multilabel_metrics(
            [_parse_multilabel(gold[x]) for x in ids],
            [_parse_multilabel(pred[x]) for x in ids],
            labels,
        )

    metrics['matched_ids'] = len(ids)
    metrics['missing_prediction_ids'] = len(joined['missing_prediction_ids'])
    metrics['extra_prediction_ids'] = len(joined['extra_prediction_ids'])
    metrics['blank_gold_ids_excluded'] = len(joined['blank_gold_ids_excluded'])
    metrics['mapped_out_gold_ids_excluded'] = len(joined['mapped_out_gold_ids_excluded'])
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
