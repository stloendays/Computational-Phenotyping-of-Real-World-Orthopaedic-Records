#!/usr/bin/env python3
"""Generate a LOCAL-ONLY physician annotation packet from the fixed source archive.

The packet contains clinical text and pseudonymous study IDs and MUST remain under
annotations/private/. Only an aggregate workload summary is suitable for GitHub.
"""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import argparse, csv, hashlib, re, sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_safe_release import norm_id, read_xlsx, disease_key_from_name
from rules import HALLUX_RE, CMC_RE, is_wrist_scaphoid

SEED = "ORTHOPHENO-VAL-2026-09-v0.1"
PHONE_RE = re.compile(r'(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)')
CN_ID_RE = re.compile(r'(?<![0-9A-Za-z])\d{17}[0-9Xx](?![0-9A-Za-z])')
LONG_NUM_RE = re.compile(r'(?<!\d)\d{9,}(?!\d)')


def study_id(domain: str, admission_key: str) -> str:
    h = hashlib.sha256(f"{SEED}|{domain}|{admission_key}".encode('utf-8')).hexdigest()
    return f"{domain[:3].upper()}-{h[:12]}"


def second_review_score(domain: str, admission_key: str) -> float:
    h = hashlib.sha256(f"{SEED}|double|{domain}|{admission_key}".encode('utf-8')).hexdigest()
    return int(h[:16], 16) / float(16**16 - 1)


def clean_text(value, patient_name=None):
    if value is None:
        return ''
    s = str(value).strip()
    if not s:
        return ''
    if patient_name:
        name = str(patient_name).strip()
        if name:
            s = s.replace(name, '[NAME]')
    s = PHONE_RE.sub('[PHONE]', s)
    s = CN_ID_RE.sub('[ID]', s)
    s = LONG_NUM_RE.sub('[LONG_NUMBER]', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def record():
    return {
        'name': None,
        'diagnosis': [],
        'complaint': [],
        'exam': [],
        'operation_name': [],
        'operation_note': [],
    }


def collect(root: Path):
    records = {k: defaultdict(record) for k in ('hallux_valgus','scaphoid_fracture','first_cmc_oa')}
    for path in sorted(root.glob('*.xlsx')):
        domain = disease_key_from_name(path.name)
        if domain not in records:
            continue
        for _, _, rows in read_xlsx(path):
            for row in rows:
                key = norm_id(row.get('住院id'))
                if not key:
                    continue
                r = records[domain][key]
                if not r['name'] and row.get('姓名'):
                    r['name'] = str(row.get('姓名')).strip()
                for field in ('主要诊断名称','主要诊断描述','其他诊断名称','其他诊断描述'):
                    t = clean_text(row.get(field), r['name'])
                    if t and t not in r['diagnosis']:
                        r['diagnosis'].append(t)
                for field, slot in [('主诉','complaint'),('专科查体','exam'),('手术名称','operation_name'),('手术记录内容','operation_note')]:
                    t = clean_text(row.get(field), r['name'])
                    if t and t not in r[slot]:
                        r[slot].append(t)
    return records


def all_text(r):
    return ' '.join(r['diagnosis'] + r['complaint'] + r['exam'] + r['operation_name'] + r['operation_note'])


def strict_status(domain, r):
    t = all_text(r)
    if domain == 'hallux_valgus':
        return bool(HALLUX_RE.search(t))
    if domain == 'first_cmc_oa':
        return bool(CMC_RE.search(t))
    if domain == 'scaphoid_fracture':
        return bool(is_wrist_scaphoid(t))
    return False


def join_parts(parts):
    return ' || '.join(x for x in parts if x)


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(rows)


def build(root: Path, out_root: Path):
    recs = collect(root)
    private_dir = out_root / 'annotations/private'
    aggregate_dir = out_root / 'data/aggregate'
    private_dir.mkdir(parents=True, exist_ok=True)
    aggregate_dir.mkdir(parents=True, exist_ok=True)

    disease_rows = []
    scaphoid_state_rows = []
    procedure_rows = []
    double_review_candidates = []
    candidate_counts = {}
    strict_counts = {}
    op_counts = {}

    for domain, rs in recs.items():
        candidate_counts[domain] = len(rs)
        strict_ids = {k for k, r in rs.items() if strict_status(domain, r)}
        strict_counts[domain] = len(strict_ids)
        op_counts[domain] = sum(bool(rs[k]['operation_note']) for k in strict_ids)

        for key, r in rs.items():
            sid = study_id(domain, key)
            disease_rows.append({
                'study_id': sid,
                'domain': domain,
                'diagnosis_text': join_parts(r['diagnosis']),
                'complaint_text': join_parts(r['complaint']),
                'physical_exam_text': join_parts(r['exam']),
                'gold_disease_anatomy_label': '',
                'gold_competing_diagnosis_labels': '',
                'reviewer_confidence': '',
                'reviewer_comment': '',
            })
            double_review_candidates.append((second_review_score(domain, key), 'disease_anatomy', domain, sid))

        if domain == 'scaphoid_fracture':
            for key in sorted(strict_ids):
                r = rs[key]; sid = study_id(domain, key)
                scaphoid_state_rows.append({
                    'study_id': sid,
                    'diagnosis_text': join_parts(r['diagnosis']),
                    'complaint_text': join_parts(r['complaint']),
                    'physical_exam_text': join_parts(r['exam']),
                    'gold_scaphoid_state': '',
                    'evidence_source': '',
                    'reviewer_confidence': '',
                    'reviewer_comment': '',
                })
                double_review_candidates.append((second_review_score(domain + '_state', key), 'scaphoid_state', domain, sid))

        for key in sorted(strict_ids):
            r = rs[key]
            if not r['operation_note']:
                continue
            sid = study_id(domain, key)
            procedure_rows.append({
                'study_id': sid,
                'domain': domain,
                'operation_name_text': join_parts(r['operation_name']),
                'operation_note_text': join_parts(r['operation_note']),
                'gold_target_disease_procedure_present': '',
                'gold_procedure_labels': '',
                'reviewer_confidence': '',
                'reviewer_comment': '',
            })
            double_review_candidates.append((second_review_score(domain + '_procedure', key), 'procedure', domain, sid))

    write_csv(private_dir/'disease_anatomy_annotation.csv', disease_rows,
              ['study_id','domain','diagnosis_text','complaint_text','physical_exam_text','gold_disease_anatomy_label','gold_competing_diagnosis_labels','reviewer_confidence','reviewer_comment'])
    write_csv(private_dir/'scaphoid_state_annotation.csv', scaphoid_state_rows,
              ['study_id','diagnosis_text','complaint_text','physical_exam_text','gold_scaphoid_state','evidence_source','reviewer_confidence','reviewer_comment'])
    write_csv(private_dir/'procedure_annotation.csv', procedure_rows,
              ['study_id','domain','operation_name_text','operation_note_text','gold_target_disease_procedure_present','gold_procedure_labels','reviewer_confidence','reviewer_comment'])

    by_stratum = defaultdict(list)
    for item in double_review_candidates:
        by_stratum[(item[1], item[2])].append(item)
    double_rows=[]
    for (layer,domain), items in sorted(by_stratum.items()):
        items=sorted(items)
        n=max(1, round(0.20*len(items)))
        for score, _, _, sid in items[:n]:
            double_rows.append({'study_id':sid,'layer':layer,'domain':domain,'hash_score':f'{score:.8f}'})
    write_csv(private_dir/'double_review_manifest.csv', double_rows, ['study_id','layer','domain','hash_score'])

    summary=[]
    for domain in ('hallux_valgus','scaphoid_fracture','first_cmc_oa'):
        summary.append({'annotation_layer':'disease_anatomy','domain':domain,'records_for_primary_review':candidate_counts[domain],
                        'records_for_double_review':sum(1 for x in double_rows if x['layer']=='disease_anatomy' and x['domain']==domain)})
    summary.append({'annotation_layer':'scaphoid_state','domain':'scaphoid_fracture','records_for_primary_review':strict_counts['scaphoid_fracture'],
                    'records_for_double_review':sum(1 for x in double_rows if x['layer']=='scaphoid_state')})
    for domain in ('hallux_valgus','scaphoid_fracture','first_cmc_oa'):
        summary.append({'annotation_layer':'procedure','domain':domain,'records_for_primary_review':op_counts[domain],
                        'records_for_double_review':sum(1 for x in double_rows if x['layer']=='procedure' and x['domain']==domain)})
    write_csv(aggregate_dir/'annotation_workload_summary.csv', summary,
              ['annotation_layer','domain','records_for_primary_review','records_for_double_review'])
    return summary


if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--raw-dir', required=True)
    ap.add_argument('--out-dir', required=True)
    args=ap.parse_args()
    summary=build(Path(args.raw_dir), Path(args.out_dir))
    for row in summary:
        print(row)
