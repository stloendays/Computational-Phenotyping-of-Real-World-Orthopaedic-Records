#!/usr/bin/env python3
"""Aggregate cohort audit and exploratory analyses for the fixed dataset.

Raw clinical files are read locally; only privacy-preserving aggregate outputs are written.
"""
from collections import Counter, defaultdict
from pathlib import Path
import argparse, csv, math, re, statistics, sys
from scipy.stats import fisher_exact, mannwhitneyu

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_safe_release import norm_id, excel_dt, read_xlsx, classify_file, disease_key_from_name, DISEASES
from legacy_xls import parse_biff
from rules import HALLUX_RE, CMC_RE, SCAPHOID_CHRONIC_RE, is_wrist_scaphoid, BILATERAL_RE

PROC = {
 'hallux_valgus': {
  'osteotomy':r'截骨|osteotomy','chevron':r'Chevron','akin':r'Akin','scarf':r'Scarf',
  'fusion':r'融合|fusion|arthrodesis','k_wire':r'克氏针|钢针|K[- ]?wire|Kirschner',
  'soft_tissue':r'软组织|肌腱|韧带|关节囊|松解|tendon|ligament','resection':r'切除|resection'},
 'scaphoid_fracture': {
  'internal_fixation':r'内固定|螺钉|空心钉|钢针|screw','bone_graft':r'植骨|取骨|bone graft',
  'reconstruction':r'重建|reconstruction','fusion':r'融合|arthrodesis'}
}
CMC_COMPETING={
 'radiocarpal_arthritis':r'桡腕关节炎','ulnocarpal_arthritis':r'尺腕关节炎',
 'rheumatoid_wrist':r'类风湿.*腕|腕.*类风湿','gouty_wrist':r'痛风.*腕|腕.*痛风',
 'traumatic_wrist':r'创伤性.*腕关节炎|腕关节.*创伤性','synovitis':r'滑膜炎',
 'generic_wrist_arthritis':r'腕关节炎','generic_carpometacarpal':r'腕掌关节炎'}

def record():
 return {'diag':[],'complaint':[],'exam':[],'opname':[],'opnote':[],'sex':None,'age':None,'height':None,'weight':None,'admit':None,'mods':set(),'labs':set()}

def collect(root):
 R={k:defaultdict(record) for k in DISEASES}; audit=[]
 for p in sorted(root.glob('*.xlsx')):
  dk=disease_key_from_name(p.name); mod=classify_file(p.name); ids=set(); rows=0
  for _,_,batch in read_xlsx(p):
   for d in batch:
    rows+=1; pid=norm_id(d.get('住院id'))
    if pid: ids.add(pid)
    if dk not in R or not pid: continue
    r=R[dk][pid]; r['mods'].add(mod)
    for key,slot in [('主要诊断名称','diag'),('主要诊断描述','diag'),('其他诊断名称','diag'),('其他诊断描述','diag'),('主诉','complaint'),('专科查体','exam'),('手术名称','opname'),('手术记录内容','opnote')]:
     v=d.get(key)
     if isinstance(v,str) and v.strip(): r[slot].append(v.strip())
    r['sex']=r['sex'] or d.get('性别'); r['age']=r['age'] if r['age'] is not None else d.get('年龄')
    r['height']=r['height'] if r['height'] is not None else d.get('身高'); r['weight']=r['weight'] if r['weight'] is not None else d.get('体重')
    for k in ('入院日期','入院时间'):
     dt=excel_dt(d.get(k));
     if dt and (r['admit'] is None or dt<r['admit']): r['admit']=dt
  audit.append((dk,mod,p.name,rows,len(ids)))
 for p in sorted(root.glob('*.xls')):
  dk=disease_key_from_name(p.name); mod=classify_file(p.name); ids=set(); rows=0
  for s,tab in parse_biff(p).items():
   if not tab: continue
   h=tab[0]; idx={x:i for i,x in enumerate(h)}; ic=idx.get('住院流水号'); rows+=max(0,len(tab)-1)
   for row in tab[1:]:
    pid=norm_id(row[ic]) if ic is not None and ic<len(row) else None
    if not pid: continue
    ids.add(pid)
    if dk in R:
     R[dk][pid]['mods'].add(mod)
     if mod=='laboratory':
      cat='coagulation' if '凝血' in s else 'cbc' if '血常规' in s else 'esr' if '红细胞沉' in s else 'crp' if 'C反应蛋白' in s else 'liver_function' if '肝功' in s else 'kidney_function' if '肾功' in s else 'electrolytes' if '离子' in s else 'other'
      R[dk][pid]['labs'].add(cat)
  audit.append((dk,mod,p.name,rows,len(ids)))
 return R,audit

def txt(r,scope='all'):
 if scope=='clinical': return ' '.join(r['diag']+r['complaint']+r['exam'])
 if scope=='op': return ' '.join(r['opname']+r['opnote'])
 return ' '.join(r['diag']+r['complaint']+r['exam']+r['opname']+r['opnote'])

def strict(R):
 out={k:set() for k in DISEASES}
 for dk,rs in R.items():
  for pid,r in rs.items():
   t=txt(r)
   if dk=='hallux_valgus' and HALLUX_RE.search(t): out[dk].add(pid)
   elif dk=='first_cmc_oa' and CMC_RE.search(t): out[dk].add(pid)
   elif dk=='scaphoid_fracture' and is_wrist_scaphoid(t): out[dk].add(pid)
 return out

def age(r):
 try:
  x=float(r['age']); return x if 0<x<120 else None
 except: return None

def bmi(r):
 try:
  h=float(r['height']); w=float(r['weight']); h=h/100 if h>3 else h; x=w/h**2; return x if 10<x<60 else None
 except: return None

def female(r):
 if r['sex'] is None:return None
 return 1 if str(r['sex']).strip() in ('女','女性','F','Female') else 0

def era(dt):
 if not dt:return None
 return '2015-2018' if 2015<=dt.year<=2018 else '2019-2022' if 2019<=dt.year<=2022 else '2023-2025' if 2023<=dt.year<=2025 else None

def q(v,p):
 v=sorted(x for x in v if x is not None)
 if not v:return None
 z=(len(v)-1)*p; lo=math.floor(z); hi=math.ceil(z); return v[lo] if lo==hi else v[lo]+(v[hi]-v[lo])*(z-lo)

def miq(v):
 v=[x for x in v if x is not None]
 return '' if not v else f'{statistics.median(v):.1f} [{q(v,.25):.1f}, {q(v,.75):.1f}]'

def sup(n): return '<5' if 0<n<5 else str(n)
def spct(n,d): return '<5' if 0<n<5 else (f'{100*n/d:.1f}%' if d else '')
def npct(n,d): return '<5' if 0<n<5 else (f'{n} ({100*n/d:.1f}%)' if d else str(n))
def safe4(a,b,c,d): return not any(0<x<5 for x in (a,b,c,d))
def fp(a,b,c,d): return fisher_exact([[a,b],[c,d]]).pvalue

def orci(a,b,c,d):
 A,B,C,D=map(float,(a,b,c,d))
 if min(A,B,C,D)==0:A+=.5;B+=.5;C+=.5;D+=.5
 o=A*D/(B*C); se=math.sqrt(1/A+1/B+1/C+1/D); return o,math.exp(math.log(o)-1.96*se),math.exp(math.log(o)+1.96*se)

def mw(a,b):
 a=[x for x in a if x is not None]; b=[x for x in b if x is not None]
 return mannwhitneyu(a,b,alternative='two-sided').pvalue if a and b else None

def write(path,rows,fields):
 path.parent.mkdir(parents=True,exist_ok=True)
 with open(path,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

def add_binary(rows,label,A,B,pred,pop='all'):
 if pop=='detailed_note': A=[p for p in A if p[1]['opnote']]; B=[p for p in B if p[1]['opnote']]
 a=sum(pred(r) for _,r in A); b=len(A)-a; c=sum(pred(r) for _,r in B); d=len(B)-c; o,lo,hi=orci(a,b,c,d); s=safe4(a,b,c,d)
 rows.append({'variable':label,'case_group':npct(a,len(A)),'comparison_group':npct(c,len(B)),'effect_measure':'odds ratio','effect_estimate':f'{o:.2f}' if s else 'suppressed','ci95':f'{lo:.2f}-{hi:.2f}' if s else 'suppressed','p_value':f'{fp(a,b,c,d):.3f}' if s else 'suppressed','analysis_population':f'{pop}; n={len(A)} vs {len(B)}'})

def main(root,out):
 R,audit=collect(root); S=strict(R); agg=out/'data/aggregate'; agg.mkdir(parents=True,exist_ok=True)
 write(agg/'source_duplication_audit.csv',[{'disease':a,'module':b,'source_file':c,'data_rows':d,'unique_admission_keys':e,'rows_per_admission':f'{d/e:.2f}' if e else ''} for a,b,c,d,e in audit],['disease','module','source_file','data_rows','unique_admission_keys','rows_per_admission'])
 er=[]
 for dk in DISEASES:
  for E in ('2015-2018','2019-2022','2023-2025'):
   P=[R[dk][p] for p in S[dk] if era(R[dk][p]['admit'])==E]; d=len(P); row={'disease':dk,'era':E,'strict_admissions':sup(d)}
   for name,mod in [('complaint_exam','complaint_exam'),('detailed_operating_note','detailed_operating_note'),('surgery_name_only','surgery_name_only'),('imaging_exam','imaging_exam'),('laboratory','laboratory')]:
    n=sum(mod in r['mods'] for r in P); row[name+'_n']=sup(n) if d>=5 else ('0' if d==0 and n==0 else '<5'); row[name+'_percent']=spct(n,d) if d>=5 else ''
   er.append(row)
 fields=['disease','era','strict_admissions']+sum(([x+'_n',x+'_percent'] for x in ['complaint_exam','detailed_operating_note','surgery_name_only','imaging_exam','laboratory']),[]); write(agg/'era_module_coverage.csv',er,fields)
 rs=R['scaphoid_fracture']; P=S['scaphoid_fracture']; C=[(p,rs[p]) for p in P if SCAPHOID_CHRONIC_RE.search(txt(rs[p],'clinical'))]; O=[(p,rs[p]) for p in P if p not in {x for x,_ in C}]
 tab=[]
 for lab,fun in [('age_years',age),('bmi_kg_m2',bmi)]:
  a=[fun(r) for _,r in C]; b=[fun(r) for _,r in O]; tab.append({'variable':lab,'case_group':miq(a),'comparison_group':miq(b),'effect_measure':'Mann-Whitney U','effect_estimate':'','ci95':'','p_value':f'{mw(a,b):.3f}','analysis_population':'all strict wrist-scaphoid records with nonmissing variable'})
 for lab,pred in [('female',lambda r:female(r)==1),('complaint_available',lambda r:bool(r['complaint'])),('physical_exam_available',lambda r:bool(r['exam'])),('any_surgery_record',lambda r:bool(r['opname'] or r['opnote'])),('detailed_operating_note',lambda r:bool(r['opnote'])),('imaging_exam_record',lambda r:'imaging_exam' in r['mods']),('cbc_record',lambda r:'cbc' in r['labs'])]: add_binary(tab,lab,C,O,pred)
 spr={k:re.compile(v,re.I) for k,v in PROC['scaphoid_fracture'].items()}; complex_rg=re.compile(r'植骨|取骨|bone graft|重建|reconstruction|融合|arthrodesis',re.I)
 for lab,rg in spr.items(): add_binary(tab,'procedure_'+lab,C,O,lambda r,rg=rg:bool(rg.search(txt(r,'op'))),'detailed_note')
 add_binary(tab,'procedure_complex_reconstruction_marker',C,O,lambda r:bool(complex_rg.search(txt(r,'op'))),'detailed_note')
 write(agg/'scaphoid_comparative_table.csv',tab,['variable','case_group','comparison_group','effect_measure','effect_estimate','ci95','p_value','analysis_population'])
 eraout=[]
 for g,X in [('established_chronic_or_nonunion',C),('other_wrist_scaphoid',O)]:
  for E in ('2015-2018','2019-2022','2023-2025'):
   n=sum(era(r['admit'])==E for _,r in X); eraout.append({'phenotype_group':g,'era':E,'n':sup(n),'group_denominator':len(X),'percent':spct(n,len(X))})
 write(agg/'scaphoid_era_distribution.csv',eraout,['phenotype_group','era','n','group_denominator','percent'])
 C23=[x for x in C if era(x[1]['admit'])=='2023-2025']; O23=[x for x in O if era(x[1]['admit'])=='2023-2025']; sen=[]
 for lab,fun in [('age_years',age),('bmi_kg_m2',bmi)]:
  a=[fun(r) for _,r in C23]; b=[fun(r) for _,r in O23]; sen.append({'variable':lab,'case_group':miq(a),'comparison_group':miq(b),'effect_measure':'Mann-Whitney U','effect_estimate':'','ci95':'','p_value':f'{mw(a,b):.3f}','analysis_population':f'2023-2025; n={len(C23)} vs {len(O23)}'})
 for lab,pred in [('female',lambda r:female(r)==1),('detailed_operating_note',lambda r:bool(r['opnote'])),('imaging_exam_record',lambda r:'imaging_exam' in r['mods'])]: add_binary(sen,lab,C23,O23,pred)
 for lab,rg in spr.items(): add_binary(sen,'procedure_'+lab,C23,O23,lambda r,rg=rg:bool(rg.search(txt(r,'op'))),'detailed_note')
 add_binary(sen,'procedure_complex_reconstruction_marker',C23,O23,lambda r:bool(complex_rg.search(txt(r,'op'))),'detailed_note')
 for r in sen:r['analysis_population']='2023-2025 '+r['analysis_population'] if not r['analysis_population'].startswith('2023-2025') else r['analysis_population']
 write(agg/'scaphoid_2023_2025_sensitivity.csv',sen,['variable','case_group','comparison_group','effect_measure','effect_estimate','ci95','p_value','analysis_population'])
 pg=[]
 for g,X in [('established_chronic_or_nonunion',C),('other_wrist_scaphoid',O)]:
  D=[r for _,r in X if r['opnote']]
  for lab,rg in spr.items():
   n=sum(bool(rg.search(txt(r,'op'))) for r in D); pg.append({'phenotype_group':g,'procedure_phenotype':lab,'n':sup(n),'denominator_detailed_notes':len(D),'percent':spct(n,len(D))})
  n=sum(bool(complex_rg.search(txt(r,'op'))) for r in D); pg.append({'phenotype_group':g,'procedure_phenotype':'complex_reconstruction_marker','n':sup(n),'denominator_detailed_notes':len(D),'percent':spct(n,len(D))})
 write(agg/'scaphoid_procedure_by_group.csv',pg,['phenotype_group','procedure_phenotype','n','denominator_detailed_notes','percent'])
 hr=R['hallux_valgus']; H=[(p,hr[p]) for p in S['hallux_valgus'] if hr[p]['opnote']]; hp={k:re.compile(v,re.I) for k,v in PROC['hallux_valgus'].items()}; vec={p:{k for k,rg in hp.items() if rg.search(txt(r,'op'))} for p,r in H}; cc=Counter(tuple(sorted(vec[p])) for p,_ in H); combos=[]; rare=0
 for labs,n in cc.most_common():
  if n<5: rare+=n
  else: combos.append({'procedure_combination':'+'.join(labs) if labs else 'none_detected','n':n,'percent':f'{100*n/len(H):.1f}%'})
 if rare:combos.append({'procedure_combination':'other_or_rare_combinations_(each_<5)','n':rare,'percent':f'{100*rare/len(H):.1f}%'})
 write(agg/'hallux_procedure_combinations.csv',combos,['procedure_combination','n','percent'])
 labs=list(hp); co=[]
 for i,a in enumerate(labs):
  for b in labs[i+1:]:
   n=sum(a in vec[p] and b in vec[p] for p,_ in H); co.append({'procedure_a':a,'procedure_b':b,'cooccurrence_n':sup(n),'denominator_detailed_notes':len(H),'percent':spct(n,len(H))})
 write(agg/'hallux_procedure_cooccurrence.csv',co,['procedure_a','procedure_b','cooccurrence_n','denominator_detailed_notes','percent'])
 hc=[]
 for target in ('chevron','fusion'):
  A=[x for x in H if target in vec[x[0]]]; B=[x for x in H if target not in vec[x[0]]]
  for lab,fun in [('age_years',age),('bmi_kg_m2',bmi)]:
   a=[fun(r) for _,r in A]; b=[fun(r) for _,r in B]; hc.append({'target_procedure':target,'variable':lab,'procedure_positive':miq(a),'procedure_negative':miq(b),'effect_measure':'Mann-Whitney U','effect_estimate':'','ci95':'','p_value':f'{mw(a,b):.3f}','analysis_population':f'detailed notes; n={len(A)} vs {len(B)}'})
  for lab,pred in [('female',lambda r:female(r)==1),('bilateral_mention',lambda r:bool(BILATERAL_RE.search(txt(r,'clinical'))))]:
   a=sum(pred(r) for _,r in A); b=len(A)-a; c=sum(pred(r) for _,r in B); d=len(B)-c; o,lo,hi=orci(a,b,c,d); s=safe4(a,b,c,d); hc.append({'target_procedure':target,'variable':lab,'procedure_positive':npct(a,len(A)),'procedure_negative':npct(c,len(B)),'effect_measure':'odds ratio','effect_estimate':f'{o:.2f}' if s else 'suppressed','ci95':f'{lo:.2f}-{hi:.2f}' if s else 'suppressed','p_value':f'{fp(a,b,c,d):.3f}' if s else 'suppressed','analysis_population':f'detailed notes; n={len(A)} vs {len(B)}'})
 write(agg/'hallux_treatment_pattern_contrasts.csv',hc,['target_procedure','variable','procedure_positive','procedure_negative','effect_measure','effect_estimate','ci95','p_value','analysis_population'])
 cr=R['first_cmc_oa']; CS=S['first_cmc_oa']; NS=[p for p in cr if p not in CS]; ca=[]
 for lab,pat in CMC_COMPETING.items():
  rg=re.compile(pat,re.I); ca.append({'term_category':lab,'strict_first_cmc_n':sup(sum(bool(rg.search(txt(cr[p]))) for p in CS)),'non_strict_candidate_n':sup(sum(bool(rg.search(txt(cr[p]))) for p in NS)),'non_strict_candidate_denominator':len(NS)})
 ca.append({'term_category':'strict_first_cmc_phenotype','strict_first_cmc_n':len(CS),'non_strict_candidate_n':'','non_strict_candidate_denominator':len(NS)})
 write(agg/'first_cmc_disambiguation_audit.csv',ca,['term_category','strict_first_cmc_n','non_strict_candidate_n','non_strict_candidate_denominator'])

if __name__=='__main__':
 ap=argparse.ArgumentParser(); ap.add_argument('--raw-dir',required=True); ap.add_argument('--out-dir',required=True); x=ap.parse_args(); main(Path(x.raw_dir),Path(x.out_dir))
