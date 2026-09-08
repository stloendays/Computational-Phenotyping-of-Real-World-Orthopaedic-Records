#!/usr/bin/env python3
"""Audit disease-concordant operative notes and regenerate procedure summaries.

This analysis separates two concepts that are otherwise easy to conflate:
1. a detailed operative-note module exists for the admission;
2. at least one detailed note actually documents surgery for the target disease.

Only aggregate privacy-preserving outputs are written.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import argparse
import csv
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_v0_1 as base
from procedure_rules import PROCEDURE_PATTERNS, disease_concordant_bodies, extract_procedure_labels
from rules import HALLUX_RE, CMC_RE, is_wrist_scaphoid, SCAPHOID_CHRONIC_RE, has_bilateral_mention


def strict_sets_v0_3(recs):
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


def write_csv(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


def labels_for_record(domain, record):
    return extract_procedure_labels(domain, record['operation_note_texts'], require_domain_concordance=True)


def has_concordant_note(domain, record):
    return bool(disease_concordant_bodies(domain, record['operation_note_texts']))


def build(raw_dir: Path, out_dir: Path):
    recs, _ = base.collect(raw_dir)
    strict = strict_sets_v0_3(recs)
    agg = out_dir / 'data' / 'aggregate'
    agg.mkdir(parents=True, exist_ok=True)

    relevance = []
    for domain in ('hallux_valgus','scaphoid_fracture','first_cmc_oa'):
        records = recs[domain]
        ids = strict[domain]
        module_ids = [p for p in ids if records[p]['operation_note_texts']]
        concordant_ids = [p for p in ids if has_concordant_note(domain, records[p])]
        relevance.append({
            'domain': domain,
            'strict_phenotype_admissions': len(ids),
            'detailed_note_module_admissions': len(module_ids),
            'disease_concordant_note_admissions': len(concordant_ids),
            'detailed_notes_in_module': sum(len(records[p]['operation_note_texts']) for p in module_ids),
            'disease_concordant_notes': sum(len(disease_concordant_bodies(domain, records[p]['operation_note_texts'])) for p in concordant_ids),
        })
    write_csv(agg/'procedure_note_relevance_audit.csv', relevance,
              ['domain','strict_phenotype_admissions','detailed_note_module_admissions','disease_concordant_note_admissions','detailed_notes_in_module','disease_concordant_notes'])

    proc_rows=[]; label_sets={}; concordant_ids_by_domain={}
    for domain in ('hallux_valgus','scaphoid_fracture','first_cmc_oa'):
        records=recs[domain]
        concordant=[p for p in strict[domain] if has_concordant_note(domain, records[p])]
        concordant_ids_by_domain[domain]=concordant
        label_sets[domain]={p:labels_for_record(domain, records[p]) for p in concordant}
        denom=len(concordant)
        for label in PROCEDURE_PATTERNS[domain]:
            n=sum(label in label_sets[domain][p] for p in concordant)
            proc_rows.append({'disease':domain,'procedure_phenotype':label,'n':base.suppress_n(n),
                              'denominator_disease_concordant_notes':denom,'percent':base.suppress_pct(n,denom)})
    write_csv(agg/'procedure_phenotype_counts_concordant.csv',proc_rows,
              ['disease','procedure_phenotype','n','denominator_disease_concordant_notes','percent'])

    domain='hallux_valgus'; records=recs[domain]; ids=concordant_ids_by_domain[domain]; vectors=label_sets[domain]
    combos=Counter(tuple(sorted(vectors[p])) for p in ids)
    combo_rows=[]; rare=0
    for labels,n in combos.most_common():
        if n<5:
            rare+=n; continue
        combo_rows.append({'procedure_combination':'+'.join(labels) if labels else 'none_detected','n':n,'percent':f'{100*n/len(ids):.1f}%'})
    if rare:
        combo_rows.append({'procedure_combination':'other_or_rare_combinations_(each_<5)','n':rare,'percent':f'{100*rare/len(ids):.1f}%'})
    write_csv(agg/'hallux_procedure_combinations_concordant.csv',combo_rows,['procedure_combination','n','percent'])

    contrast_rows=[]
    for target in ('chevron','fusion'):
        positive=[p for p in ids if target in vectors[p]]; negative=[p for p in ids if target not in vectors[p]]
        for variable,fn in [('age_years',base.numeric_age),('bmi_kg_m2',base.numeric_bmi)]:
            a=[fn(records[p]) for p in positive]; b=[fn(records[p]) for p in negative]
            contrast_rows.append({'target_procedure':target,'variable':variable,
                'procedure_positive':base.fmt_med_iqr(a),'procedure_negative':base.fmt_med_iqr(b),
                'effect_measure':'Mann-Whitney U','effect_estimate':'','ci95':'','p_value':base.fmt_num(base.mw_p(a,b),3),
                'analysis_population':f'disease-concordant notes; n={len(positive)} vs {len(negative)}'})
        for variable,pred in [('female',lambda r:base.female(r)==1),('bilateral_mention',lambda r:has_bilateral_mention(base.clinical_text(r)))]:
            a=sum(pred(records[p]) for p in positive); b=len(positive)-a
            c=sum(pred(records[p]) for p in negative); d=len(negative)-c
            safe=base.inferential_cell_safe(a,b,c,d); orv,lo,hi=base.fisher_or_ci(a,b,c,d)
            contrast_rows.append({'target_procedure':target,'variable':variable,
                'procedure_positive':base.safe_n_pct(a,len(positive)),'procedure_negative':base.safe_n_pct(c,len(negative)),
                'effect_measure':'odds ratio','effect_estimate':base.fmt_num(orv,2) if safe else 'suppressed',
                'ci95':f'{lo:.2f}-{hi:.2f}' if safe else 'suppressed',
                'p_value':base.fmt_num(base.fisher_p(a,b,c,d),3) if safe else 'suppressed',
                'analysis_population':f'disease-concordant notes; n={len(positive)} vs {len(negative)}'})
    write_csv(agg/'hallux_treatment_pattern_contrasts_concordant.csv',contrast_rows,
              ['target_procedure','variable','procedure_positive','procedure_negative','effect_measure','effect_estimate','ci95','p_value','analysis_population'])

    domain='scaphoid_fracture'; records=recs[domain]; all_ids=strict[domain]
    chronic={p for p in all_ids if SCAPHOID_CHRONIC_RE.search(base.clinical_text(records[p]))}; comparison=all_ids-chronic
    scaph_rows=[]
    for group_name,group in [('established_chronic_or_nonunion',chronic),('other_wrist_scaphoid',comparison)]:
        ids=[p for p in group if has_concordant_note(domain,records[p])]
        vectors={p:labels_for_record(domain,records[p]) for p in ids}
        for label in PROCEDURE_PATTERNS[domain]:
            n=sum(label in vectors[p] for p in ids)
            scaph_rows.append({'phenotype_group':group_name,'procedure_phenotype':label,'n':base.suppress_n(n),
                               'denominator_disease_concordant_notes':len(ids),'percent':base.suppress_pct(n,len(ids))})
        n=sum(bool({'bone_graft','reconstruction','fusion'} & vectors[p]) for p in ids)
        scaph_rows.append({'phenotype_group':group_name,'procedure_phenotype':'complex_reconstruction_marker','n':base.suppress_n(n),
                           'denominator_disease_concordant_notes':len(ids),'percent':base.suppress_pct(n,len(ids))})
    write_csv(agg/'scaphoid_procedure_by_group_concordant.csv',scaph_rows,
              ['phenotype_group','procedure_phenotype','n','denominator_disease_concordant_notes','percent'])

    return relevance


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--raw-dir',required=True); parser.add_argument('--out-dir',required=True)
    args=parser.parse_args(); build(Path(args.raw_dir),Path(args.out_dir))
