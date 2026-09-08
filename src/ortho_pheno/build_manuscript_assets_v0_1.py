#!/usr/bin/env python3
"""Generate pre-gold manuscript figures and Table 1 from public aggregate data only.

This script intentionally depends only on privacy-preserving aggregate CSV files
already committed to the repository. It never reads raw EHR exports, study IDs,
free text, or physician gold labels.

Outputs
-------
figures/pre_gold/Figure1_validation_first_framework.svg
figures/pre_gold/Figure2_cohort_reconstruction.svg
figures/pre_gold/Figure3_procedure_attribution.svg
results/tables/TABLE1_SOURCE_ARCHITECTURE_V0_1.csv
results/tables/TABLE1_SOURCE_ARCHITECTURE_V0_1.md
"""
from __future__ import annotations

from pathlib import Path
import argparse
import csv
import html

DOMAIN_LABELS = {
    "hallux_valgus": "Hallux valgus",
    "scaphoid_fracture": "Scaphoid retrieval",
    "first_cmc_oa": "First-CMC OA",
}


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def esc(value):
    return html.escape(str(value))


def svg_header(width, height, title, desc):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title>
<desc id="desc">{esc(desc)}</desc>
<style>
text {{ font-family: Arial, Helvetica, sans-serif; fill: #111; }}
.title {{ font-size: 24px; font-weight: 700; }}
.subtitle {{ font-size: 14px; fill: #555; }}
.label {{ font-size: 14px; font-weight: 600; }}
.small {{ font-size: 12px; fill: #444; }}
.tiny {{ font-size: 10px; fill: #555; }}
.box {{ fill: #fff; stroke: #111; stroke-width: 1.5; }}
.soft {{ fill: #f3f3f3; stroke: #777; stroke-width: 1.2; }}
.dark {{ fill: #222; stroke: #111; stroke-width: 1.2; }}
.white {{ fill: #fff; }}
.rule {{ stroke: #111; stroke-width: 1.5; fill: none; }}
.dash {{ stroke: #777; stroke-width: 1.2; stroke-dasharray: 5 4; fill: none; }}
</style>
'''


def text(x, y, value, cls="label", anchor="start"):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{esc(value)}</text>\n'


def rect(x, y, w, h, cls="box", rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>\n'


def line(x1, y1, x2, y2, cls="rule"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"/>\n'


def arrow(x1, y1, x2, y2):
    # small publication-safe arrowhead
    s = line(x1, y1, x2, y2)
    s += f'<polygon points="{x2},{y2} {x2-8},{y2-4} {x2-8},{y2+4}" fill="#111"/>\n'
    return s


def write_figure1(path: Path):
    width, height = 1500, 760
    s = svg_header(width, height,
                   "Validation-first computational phenotyping framework",
                   "Fixed-data orthopaedic EHR workflow separating private clinical data from public aggregate outputs and freezing model comparison after physician adjudication.")
    s += text(60, 55, "Figure 1. Validation-first computational phenotyping framework", "title")
    s += text(60, 82, "Fixed local data; no additional hospital data assumed", "subtitle")

    # Private zone
    s += rect(40, 115, 1050, 555, "soft", 12)
    s += text(65, 145, "PRIVATE ANALYTIC ZONE", "label")
    s += text(65, 168, "Raw records, clinical text, pseudonymous study IDs and physician labels never enter the public repository", "small")

    stages = [
        (75, 220, 170, 90, "18 raw exports", "12 XLSX + 6 legacy XLS"),
        (295, 220, 190, 90, "Admission reconstruction", "deduplicate repeated diagnosis rows"),
        (535, 220, 190, 90, "Disease / anatomy", "explicit uncertain states"),
        (775, 220, 190, 90, "Clinical state", "source-restricted phenotypes"),
    ]
    for x,y,w,h,a,b in stages:
        s += rect(x,y,w,h,"box")
        s += text(x+w/2,y+35,a,"label","middle")
        s += text(x+w/2,y+60,b,"small","middle")
    for i in range(len(stages)-1):
        x1=stages[i][0]+stages[i][2]; x2=stages[i+1][0]
        s += arrow(x1+5,265,x2-8,265)

    s += rect(235, 375, 220, 105, "box")
    s += text(345, 410, "Procedure relevance", "label", "middle")
    s += text(345, 435, "Does this operation treat", "small", "middle")
    s += text(345, 454, "the target disease?", "small", "middle")

    s += rect(505, 375, 220, 105, "box")
    s += text(615, 410, "Procedure components", "label", "middle")
    s += text(615, 435, "multi-label operative", "small", "middle")
    s += text(615, 454, "phenotype extraction", "small", "middle")
    s += arrow(460,428,495,428)

    s += rect(775, 375, 250, 105, "dark")
    s += text(900, 409, "Physician reference standard", "label white", "middle")
    s += text(900, 435, "primary review + ~20%", "small white", "middle")
    s += text(900, 454, "independent second review", "small white", "middle")
    s += arrow(730,428,765,428)

    # Frozen comparison layer
    s += rect(200, 545, 250, 78, "box")
    s += text(325, 578, "Pre-gold deterministic baseline", "label", "middle")
    s += text(325, 601, "SHA-256 frozen before gold", "small", "middle")
    s += rect(505, 545, 210, 78, "box")
    s += text(610, 578, "LLM-assisted", "label", "middle")
    s += text(610, 601, "same locked labels", "small", "middle")
    s += rect(770, 545, 210, 78, "box")
    s += text(875, 578, "Hybrid system", "label", "middle")
    s += text(875, 601, "same locked labels", "small", "middle")
    s += line(900,480,900,520)
    s += line(325,520,875,520)
    for cx in (325,610,875): s += line(cx,520,cx,545)

    # Public zone
    s += rect(1130, 115, 330, 555, "box", 12)
    s += text(1155, 145, "PUBLIC REPRODUCIBILITY ZONE", "label")
    public_items = [
        "Versioned code + tests",
        "Aggregate cohort audits",
        "Small-cell suppression",
        "Figure / table generators",
        "Freeze manifests + hashes",
        "No row-level clinical data",
    ]
    y=205
    for item in public_items:
        s += rect(1160,y-25,265,44,"soft",6)
        s += text(1292,y+2,item,"small","middle")
        y += 68
    s += arrow(1080,390,1120,390)
    s += text(1100,375,"aggregate only","tiny","middle")

    s += "</svg>\n"
    path.write_text(s, encoding="utf-8")


def write_figure2(path: Path, cohort_rows, duplication_rows, anatomy_rows, transition_rows):
    width, height = 1600, 900
    cohort={r['disease']:r for r in cohort_rows}
    dup={r['disease']:r for r in duplication_rows if r['module']=='demographics_diagnoses'}
    anatomy={r['anatomy_class']:r for r in anatomy_rows}
    transition={r['transition']:r for r in transition_rows}
    s=svg_header(width,height,
                 "Cohort reconstruction and scaphoid anatomy disambiguation",
                 "Four-panel audit showing raw-row inflation, candidate-to-strict cohort reduction, scaphoid anatomy partition, and rule-version transition.")
    s += text(55,50,"Figure 2. Cohort reconstruction and anatomy disambiguation","title")

    # Panel A
    s += text(65,105,"A   Raw-row inflation in diagnosis/demographics exports","label")
    max_ratio=max(float(dup[d]['rows_per_admission']) for d in DOMAIN_LABELS)
    y=155
    for d in ('hallux_valgus','first_cmc_oa','scaphoid_fracture'):
        ratio=float(dup[d]['rows_per_admission'])
        w=420*ratio/max_ratio
        s += text(70,y+18,DOMAIN_LABELS[d],"small")
        s += rect(260,y,w,30,"dark",3)
        s += text(270+w,y+21,f"{ratio:.2f} rows/admission","small")
        y += 72
    s += text(70,365,"Raw diagnosis rows are not independent analytical units.","small")

    # Panel B
    s += text(830,105,"B   Broad candidate retrieval → deterministic strict phenotype","label")
    y=155
    for d in ('hallux_valgus','first_cmc_oa','scaphoid_fracture'):
        cand=int(cohort[d]['candidate_admissions']); strict=int(cohort[d]['strict_phenotype_admissions'])
        s += text(835,y+18,DOMAIN_LABELS[d],"small")
        s += rect(1035,y,230,30,"soft",3)
        s += rect(1035,y,230*strict/cand,30,"dark",3)
        s += text(1280,y+21,f"{strict}/{cand} ({100*strict/cand:.1f}%)","small")
        y += 72
    s += text(835,365,"Strict counts remain algorithmic outputs until physician adjudication.","small")

    # Panel C
    s += text(65,455,"C   Scaphoid candidate anatomy under phenotype v0.3","label")
    total=sum(int(r['n']) for r in anatomy_rows)
    classes=[('wrist_scaphoid','Wrist scaphoid','#222'),('foot_navicular','Foot navicular','#777'),('ambiguous','Ambiguous','#d9d9d9')]
    x0=70; full=650; x=x0
    for key,label,color in classes:
        n=int(anatomy[key]['n']); w=full*n/total
        s += f'<rect x="{x}" y="500" width="{w}" height="70" fill="{color}" stroke="#111" stroke-width="1"/>\n'
        tclass='small white' if key!='ambiguous' else 'small'
        s += text(x+w/2,530,label,tclass,'middle')
        s += text(x+w/2,552,f"{n}/{total} ({100*n/total:.1f}%)",tclass,'middle')
        x += w
    s += text(70,605,"Seven ambiguous episodes are preserved for physician adjudication rather than forced into a binary class.","small")

    # Panel D
    s += text(830,455,"D   Superseded heuristic → phenotype v0.3","label")
    s += rect(875,505,235,70,"soft")
    s += text(992,535,"Previous wrist selection","label","middle")
    s += text(992,558,"72 episodes","small","middle")
    s += rect(1250,485,245,70,"dark")
    s += text(1372,516,"Retained wrist scaphoid","label white","middle")
    s += text(1372,539,"68 episodes","small white","middle")
    s += rect(1250,595,245,70,"soft")
    s += text(1372,626,"Removed as foot navicular","label","middle")
    s += text(1372,649,"4 episodes","small","middle")
    s += arrow(1115,530,1240,520)
    s += arrow(1115,548,1240,625)
    s += text(1170,505,"68","small","middle")
    s += text(1170,610,"4","small","middle")
    s += text(875,720,"New wrist additions relative to the superseded heuristic: 0", "small")
    s += text(875,745,"The revision removed explicit anatomical contamination rather than increasing sample size.","small")

    s += text(65,855,"All panels use public aggregate audit outputs; no patient-level data are shown.","tiny")
    s += "</svg>\n"
    path.write_text(s,encoding="utf-8")


def write_figure3(path: Path, relevance_rows):
    width,height=1600,900
    rel={r['domain']:r for r in relevance_rows}
    s=svg_header(width,height,
                 "Procedure attribution as a distinct EHR phenotyping problem",
                 "Three-panel figure separating module availability, target-disease procedure relevance, and procedure-component extraction.")
    s += text(55,50,"Figure 3. Procedure attribution exposes a second hidden EHR error mode","title")

    # Panel A schematic
    s += text(65,105,"A   Why generic procedure keywords can leak across anatomy","label")
    s += rect(80,150,310,120,"soft")
    s += text(235,185,"One admission episode","label","middle")
    s += text(235,213,"Target disease + another orthopaedic problem","small","middle")
    s += text(235,237,"Detailed note module available","small","middle")
    s += rect(500,135,280,85,"box")
    s += text(640,170,"Target-disease operation","label","middle")
    s += text(640,194,"e.g. hallux osteotomy","small","middle")
    s += rect(500,255,280,85,"box")
    s += text(640,290,"Other-anatomy operation","label","middle")
    s += text(640,314,"generic terms may overlap","small","middle")
    s += arrow(395,200,490,178)
    s += arrow(395,220,490,296)
    s += rect(885,165,300,120,"dark")
    s += text(1035,198,"Relevance gate","label white","middle")
    s += text(1035,224,"Does the procedure treat", "small white","middle")
    s += text(1035,244,"the target study disease?", "small white","middle")
    s += arrow(785,178,875,210)
    s += arrow(785,296,875,245)
    s += rect(1280,165,250,120,"box")
    s += text(1405,202,"Only then extract", "label","middle")
    s += text(1405,228,"procedure components", "label","middle")
    s += text(1405,252,"(multi-label)", "small","middle")
    s += arrow(1195,225,1270,225)

    # Panel B
    s += text(65,415,"B   Detailed-note module availability versus disease-concordant procedure-note availability","label")
    y=475
    maxn=max(int(rel[d]['detailed_note_module_admissions']) for d in rel)
    for d in ('hallux_valgus','scaphoid_fracture','first_cmc_oa'):
        mod=int(rel[d]['detailed_note_module_admissions']); con=int(rel[d]['disease_concordant_note_admissions'])
        scale=520/maxn
        s += text(70,y+20,DOMAIN_LABELS[d],"small")
        s += rect(290,y,mod*scale,22,"soft",2)
        s += rect(290,y+30,con*scale,22,"dark",2)
        s += text(305+mod*scale,y+17,f"module {mod}","small")
        s += text(305+con*scale,y+47,f"target-disease {con}","small")
        if mod>con:
            s += text(830,y+35,f"{mod-con} admission(s) excluded from target-disease prevalence", "tiny")
        y += 92
    s += text(290,755,"light = detailed-note module available", "tiny")
    s += text(535,755,"dark = disease-concordant procedure note", "tiny")

    # Panel C
    s += text(970,415,"C   Prespecified hierarchical evaluation","label")
    boxes=[
        (995,470,500,66,"1. Procedure relevance","yes / no / uncertain"),
        (995,565,500,66,"2. Components conditional on gold relevance=yes","Does extraction work once attribution is known?"),
        (995,660,500,66,"3. End-to-end components","Relevance errors and component errors both count"),
    ]
    for x,y,w,h,a,b in boxes:
        s += rect(x,y,w,h,"box")
        s += text(x+20,y+27,a,"label")
        s += text(x+20,y+50,b,"small")
    s += arrow(1245,538,1245,555)
    s += arrow(1245,633,1245,650)
    s += text(995,785,"This prevents a high component F1 from hiding wrong-disease attribution.","small")

    s += text(65,855,"Counts are deterministic audit outputs and remain provisional clinical labels until physician validation.","tiny")
    s += "</svg>\n"
    path.write_text(s,encoding="utf-8")


def write_table1(csv_path: Path, md_path: Path, cohort_rows, duplication_rows, relevance_rows):
    cohort={r['disease']:r for r in cohort_rows}
    dup={r['disease']:r for r in duplication_rows if r['module']=='demographics_diagnoses'}
    rel={r['domain']:r for r in relevance_rows}
    fields=[
        'domain','candidate_admissions','deterministic_strict_phenotype','diagnosis_rows_per_admission',
        'female_percent','age_median_iqr','bmi_median','complaint_available_n','physical_exam_available_n',
        'detailed_note_module_n','disease_concordant_procedure_note_n','exam_record_available_n',
        'cbc_available_n','coagulation_available_n'
    ]
    rows=[]
    for d in ('hallux_valgus','scaphoid_fracture','first_cmc_oa'):
        c=cohort[d]
        rows.append({
            'domain':DOMAIN_LABELS[d],
            'candidate_admissions':c['candidate_admissions'],
            'deterministic_strict_phenotype':c['strict_phenotype_admissions'],
            'diagnosis_rows_per_admission':dup[d]['rows_per_admission'],
            'female_percent':c['female_percent'],
            'age_median_iqr':f"{c['age_median']} [{c['age_q1']}, {c['age_q3']}]",
            'bmi_median':c['bmi_median'],
            'complaint_available_n':c['with_complaint'],
            'physical_exam_available_n':c['with_physical_exam'],
            'detailed_note_module_n':rel[d]['detailed_note_module_admissions'],
            'disease_concordant_procedure_note_n':rel[d]['disease_concordant_note_admissions'],
            'exam_record_available_n':c['with_any_exam_record'],
            'cbc_available_n':c['with_cbc'],
            'coagulation_available_n':c['with_coagulation'],
        })
    csv_path.parent.mkdir(parents=True,exist_ok=True)
    with csv_path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

    header=['Domain','Candidates','Strict phenotype*','Dx rows/admission','Female, %','Age, median [IQR]','BMI, median','Complaint n','Exam n','Detailed note module n','Target-disease procedure note n','Imaging/exam record n','CBC n','Coagulation n']
    md=[]
    md.append('# Table 1. Source architecture and deterministic cohort reconstruction\n')
    md.append('| ' + ' | '.join(header) + ' |')
    md.append('|' + '|'.join(['---'] + ['---:']*(len(header)-1)) + '|')
    for r in rows:
        vals=[r['domain'],r['candidate_admissions'],r['deterministic_strict_phenotype'],r['diagnosis_rows_per_admission'],r['female_percent'],r['age_median_iqr'],r['bmi_median'],r['complaint_available_n'],r['physical_exam_available_n'],r['detailed_note_module_n'],r['disease_concordant_procedure_note_n'],r['exam_record_available_n'],r['cbc_available_n'],r['coagulation_available_n']]
        md.append('| ' + ' | '.join(str(x) for x in vals) + ' |')
    md.append('')
    md.append('*Strict phenotype counts are deterministic phenotype-v0.3 outputs and are not physician-confirmed ground truth until the reference standard is frozen.*')
    md.append('')
    md.append('**Interpretation notes.** The analytical unit is the reconstructed admission episode. `Dx rows/admission` quantifies raw diagnosis/demographics row inflation. `Detailed note module n` measures availability of a detailed operative-note export; `Target-disease procedure note n` additionally requires anatomy-aware relevance to the study disease. Missing module availability is not interpreted as clinical absence.')
    md_path.write_text('\n'.join(md)+'\n',encoding='utf-8')


def build(repo_root: Path):
    agg=repo_root/'data/aggregate'
    cohort=read_csv(agg/'cohort_overview.csv')
    duplication=read_csv(agg/'source_duplication_audit.csv')
    anatomy=read_csv(agg/'scaphoid_anatomy_audit.csv')
    transition=read_csv(agg/'scaphoid_rule_version_transition.csv')
    relevance=read_csv(agg/'procedure_note_relevance_audit.csv')

    figdir=repo_root/'figures/pre_gold'; figdir.mkdir(parents=True,exist_ok=True)
    tabdir=repo_root/'results/tables'; tabdir.mkdir(parents=True,exist_ok=True)
    write_figure1(figdir/'Figure1_validation_first_framework.svg')
    write_figure2(figdir/'Figure2_cohort_reconstruction.svg',cohort,duplication,anatomy,transition)
    write_figure3(figdir/'Figure3_procedure_attribution.svg',relevance)
    write_table1(tabdir/'TABLE1_SOURCE_ARCHITECTURE_V0_1.csv',
                 tabdir/'TABLE1_SOURCE_ARCHITECTURE_V0_1.md',
                 cohort,duplication,relevance)


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo-root',default='.')
    args=ap.parse_args()
    build(Path(args.repo_root).resolve())
