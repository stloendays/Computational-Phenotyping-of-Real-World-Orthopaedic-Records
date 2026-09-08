#!/usr/bin/env python3
"""Generate journal-style PRIVATE final scaphoid figures after physician Gold freeze.

The generator reads only adjudicated Gold files plus the private exact manuscript
analysis JSON. It never reads raw free text. Because final group sizes and individual
durations can be small, these SVGs are manuscript-private by default and must not be
committed to the public repository without an explicit privacy review.

Figures
-------
Figure 1: physician-defined cohort flow.
Figure 2: internal fixation and bone-graft proportions by presentation state,
          plus the primary conditional OR/95% CI when finite.
Figure 3: individual physician-adjudicated duration values within established
          chronic/nonunion, stratified by graft status, on a log time axis.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import csv
import html
import json
import math

from duration_rules import convert_duration_to_days
from freeze_scaph_reference_v0_1 import build_final_manifest

CHRONIC_STATES = {
    'established_chronic_fracture',
    'established_nonunion',
    'chronic_nonunion_not_distinguishable',
}
ACUTE_STATE = 'acute_or_new_fracture'


def read_map(path: Path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return {r['study_id'].strip(): r for r in csv.DictReader(f)}


def esc(text):
    return html.escape(str(text), quote=True)


def svg_start(width, height):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#111} .small{font-size:12px}.body{font-size:14px}.label{font-size:16px;font-weight:700}.panel{font-size:18px;font-weight:700}</style>',
    ]


def text(lines, x, y, value, cls='body', anchor='middle'):
    lines.append(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{esc(value)}</text>')


def box(lines, x, y, w, h, title, subtitle=''):
    lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="white" stroke="#333" stroke-width="1.2"/>')
    text(lines, x+w/2, y+26, title, 'label')
    if subtitle:
        text(lines, x+w/2, y+49, subtitle, 'body')


def arrow(lines, x1, y1, x2, y2):
    lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#555" stroke-width="1.2"/>')
    angle = math.atan2(y2-y1, x2-x1)
    size = 7
    a1 = angle + 2.55; a2 = angle - 2.55
    p1 = (x2 + size*math.cos(a1), y2 + size*math.sin(a1))
    p2 = (x2 + size*math.cos(a2), y2 + size*math.sin(a2))
    lines.append(f'<polygon points="{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="#555"/>')


def state_group(value):
    if value in CHRONIC_STATES:
        return 'chronic'
    if value == ACUTE_STATE:
        return 'acute'
    return 'other'


def load_gold(review_dir: Path):
    # Full population/vocabulary validation; raises before any figure is produced.
    build_final_manifest(review_dir)
    anatomy = read_map(review_dir/'scaphoid_anatomy_adjudicated.csv')
    state = read_map(review_dir/'scaphoid_state_adjudicated.csv')
    proc = read_map(review_dir/'scaphoid_procedure_adjudicated.csv')
    return anatomy, state, proc


def cohort_counts(anatomy, state, proc):
    wrist = {sid for sid, r in anatomy.items() if r.get('gold_anatomy_label','').strip() == 'wrist_scaphoid'}
    state_counts = {'chronic':0, 'acute':0, 'other':0}
    for sid in wrist:
        g = state_group(state[sid].get('gold_scaphoid_state','').strip())
        state_counts[g] += 1
    detailed = set(proc)
    relevant = {sid for sid, r in proc.items() if r.get('gold_target_disease_procedure_present','').strip() == 'yes'}
    analytic = {'chronic':0, 'acute':0}
    for sid in relevant:
        g = state_group(state[sid].get('gold_scaphoid_state','').strip())
        if g in analytic:
            analytic[g] += 1
    return {
        'broad': len(anatomy),
        'wrist': len(wrist),
        'foot': sum(r.get('gold_anatomy_label','').strip() == 'foot_navicular' for r in anatomy.values()),
        'other_uncertain_anatomy': sum(r.get('gold_anatomy_label','').strip() in {'other','uncertain'} for r in anatomy.values()),
        'state': state_counts,
        'detailed': len(detailed),
        'relevant': len(relevant),
        'analytic': analytic,
    }


def figure1_cohort_flow(counts, path: Path):
    lines = svg_start(900, 590)
    text(lines, 28, 32, 'A', 'panel', 'start')
    box(lines, 300, 40, 300, 70, f"Broad scaphoid candidates, n={counts['broad']}")
    arrow(lines, 450, 110, 450, 145)
    box(lines, 300, 145, 300, 70, f"Physician-confirmed wrist scaphoid, n={counts['wrist']}",
        f"Foot navicular={counts['foot']}; other/uncertain anatomy={counts['other_uncertain_anatomy']}")
    arrow(lines, 450, 215, 450, 250)

    box(lines, 70, 250, 270, 78, f"Established chronic/nonunion, n={counts['state']['chronic']}")
    box(lines, 560, 250, 270, 78, f"Acute/new fracture, n={counts['state']['acute']}")
    text(lines, 450, 285, f"State uncertain/excluded, n={counts['state']['other']}", 'small')
    arrow(lines, 205, 328, 205, 380)
    arrow(lines, 695, 328, 695, 380)

    box(lines, 70, 380, 270, 78, f"Target-disease operative analysis, n={counts['analytic']['chronic']}")
    box(lines, 560, 380, 270, 78, f"Target-disease operative analysis, n={counts['analytic']['acute']}")
    text(lines, 450, 500, f"Detailed operative-note records among physician wrist cohort: n={counts['detailed']}", 'small')
    text(lines, 450, 522, f"Adjudicated target-disease operations: n={counts['relevant']}", 'small')
    text(lines, 450, 554, 'Final state-based analysis excludes insufficient/uncertain state and non-target operations.', 'small')
    lines.append('</svg>')
    path.write_text('\n'.join(lines), encoding='utf-8')


def pct(item, group):
    t = item['table']
    if group == 'chronic':
        yes = t['chronic_yes']; den = item['chronic_evaluable']
    else:
        yes = t['acute_yes']; den = item['acute_evaluable']
    return (100.0*yes/den if den else None, yes, den)


def figure2_composition(result, path: Path):
    lines = svg_start(980, 520)
    text(lines, 25, 30, 'A', 'panel', 'start')
    metrics = [
        ('Internal fixation', result['key_contrast_internal_fixation']),
        ('Bone-graft augmentation', result['primary_bone_graft']),
    ]
    groups = [('Established chronic/nonunion','chronic'), ('Acute/new fracture','acute')]
    x0 = 115; plot_w = 520
    # axes
    lines.append(f'<line x1="{x0}" y1="430" x2="{x0+plot_w}" y2="430" stroke="#333" stroke-width="1"/>')
    for p in (0,25,50,75,100):
        x = x0 + plot_w*p/100
        lines.append(f'<line x1="{x}" y1="90" x2="{x}" y2="430" stroke="#e0e0e0" stroke-width="1"/>')
        text(lines, x, 454, str(p), 'small')
    text(lines, x0+plot_w/2, 480, 'Patients with operative component (%)', 'body')

    ys = [160, 320]
    offsets = [-20, 20]
    fills = {'chronic':'#333333','acute':'#b0b0b0'}
    for (label, item), y in zip(metrics, ys):
        text(lines, 35, y+4, label, 'body', 'start')
        for (glabel, gkey), off in zip(groups, offsets):
            percent, yes, den = pct(item, gkey)
            yy = y+off
            if percent is not None:
                x = x0 + plot_w*percent/100
                lines.append(f'<line x1="{x0}" y1="{yy}" x2="{x}" y2="{yy}" stroke="{fills[gkey]}" stroke-width="12"/>')
                lines.append(f'<circle cx="{x}" cy="{yy}" r="5" fill="{fills[gkey]}"/>')
                text(lines, x+10, yy+4, f'{percent:.1f}% ({yes}/{den})', 'small', 'start')
    # legend
    lines.append('<rect x="115" y="58" width="14" height="14" fill="#333333"/>')
    text(lines, 137, 70, 'Established chronic/nonunion', 'small', 'start')
    lines.append('<rect x="325" y="58" width="14" height="14" fill="#b0b0b0"/>')
    text(lines, 347, 70, 'Acute/new fracture', 'small', 'start')

    # primary OR panel
    text(lines, 700, 30, 'B', 'panel', 'start')
    item = result['primary_bone_graft']
    orv = item.get('odds_ratio_conditional'); lo = item.get('ci95_low'); hi = item.get('ci95_high')
    text(lines, 815, 90, 'Bone-graft association', 'label')
    if orv is not None and lo is not None and hi is not None and all(math.isfinite(v) and v > 0 for v in (orv,lo,hi)):
        log_min = math.log10(min(0.1, lo)/1.2); log_max = math.log10(max(10,hi)*1.2)
        fx0=700; fx1=945; fy=245
        def xpos(v): return fx0 + (math.log10(v)-log_min)/(log_max-log_min)*(fx1-fx0)
        lines.append(f'<line x1="{fx0}" y1="{fy}" x2="{fx1}" y2="{fy}" stroke="#333"/>')
        x1=xpos(lo); x2=xpos(hi); xm=xpos(orv); xref=xpos(1)
        lines.append(f'<line x1="{xref}" y1="150" x2="{xref}" y2="330" stroke="#999" stroke-dasharray="4,4"/>')
        lines.append(f'<line x1="{x1}" y1="{fy}" x2="{x2}" y2="{fy}" stroke="#222" stroke-width="2"/>')
        lines.append(f'<circle cx="{xm}" cy="{fy}" r="6" fill="#222"/>')
        text(lines, 815, 285, f'Conditional OR {orv:.2f} (95% CI {lo:.2f}-{hi:.2f})', 'small')
        text(lines, 815, 307, f"Fisher two-sided P={item['fisher_two_sided_p']:.4g}", 'small')
    else:
        text(lines, 815, 235, 'Finite conditional OR/CI not estimable', 'body')
        if item.get('fisher_two_sided_p') is not None:
            text(lines, 815, 265, f"Fisher two-sided P={item['fisher_two_sided_p']:.4g}", 'small')
    lines.append('</svg>')
    path.write_text('\n'.join(lines), encoding='utf-8')


def duration_points(state, proc):
    out = {'yes': [], 'no': []}
    for sid, prow in proc.items():
        if prow.get('gold_target_disease_procedure_present','').strip() != 'yes':
            continue
        srow = state.get(sid)
        if not srow or srow.get('gold_scaphoid_state','').strip() not in CHRONIC_STATES:
            continue
        graft = prow.get('gold_bone_graft','').strip()
        if graft not in out:
            continue
        if srow.get('gold_relevant_duration_present','').strip() != 'yes':
            continue
        try:
            value = float(srow.get('gold_relevant_duration_value','').strip())
            unit = srow.get('gold_relevant_duration_unit','').strip()
            days = convert_duration_to_days(value, unit)
        except Exception:
            continue
        if days > 0:
            out[graft].append(days)
    return out


def quantile(xs, p):
    ys=sorted(xs)
    if not ys: return None
    pos=(len(ys)-1)*p; lo=math.floor(pos); hi=math.ceil(pos)
    if lo==hi: return ys[lo]
    return ys[lo]+(ys[hi]-ys[lo])*(pos-lo)


def figure3_duration(points, path: Path):
    lines = svg_start(760, 520)
    text(lines, 25, 30, 'A', 'panel', 'start')
    allv = points['yes'] + points['no']
    if not allv:
        text(lines, 380, 260, 'No physician-valid duration values available.', 'body')
        lines.append('</svg>'); path.write_text('\n'.join(lines),encoding='utf-8'); return
    vmin=max(0.1,min(allv)/1.5); vmax=max(allv)*1.5
    logmin=math.log10(vmin); logmax=math.log10(vmax)
    y0=430; y1=70
    def ypos(v): return y0 - (math.log10(v)-logmin)/(logmax-logmin)*(y0-y1)
    # reference ticks
    ticks=[1,7,30.4375,180,365.25,730.5]
    labels=['1 d','1 wk','1 mo','6 mo','1 y','2 y']
    for v,lbl in zip(ticks,labels):
        if vmin <= v <= vmax:
            y=ypos(v)
            lines.append(f'<line x1="120" y1="{y:.1f}" x2="650" y2="{y:.1f}" stroke="#e5e5e5"/>')
            text(lines,105,y+4,lbl,'small','end')
    lines.append(f'<line x1="120" y1="{y1}" x2="120" y2="{y0}" stroke="#333"/>')
    xs={'yes':260,'no':510}
    labelsx={'yes':'Bone graft present','no':'Bone graft absent'}
    for key in ('yes','no'):
        vals=sorted(points[key])
        x=xs[key]
        # deterministic symmetric jitter, no random seed needed
        for i,v in enumerate(vals):
            offset=((i%5)-2)*9
            lines.append(f'<circle cx="{x+offset}" cy="{ypos(v):.1f}" r="4.5" fill="#555" fill-opacity="0.8"/>')
        if vals:
            med=quantile(vals,.5); q1=quantile(vals,.25); q3=quantile(vals,.75)
            lines.append(f'<line x1="{x}" y1="{ypos(q1):.1f}" x2="{x}" y2="{ypos(q3):.1f}" stroke="#111" stroke-width="3"/>')
            lines.append(f'<line x1="{x-28}" y1="{ypos(med):.1f}" x2="{x+28}" y2="{ypos(med):.1f}" stroke="#111" stroke-width="3"/>')
            text(lines,x,466,f"{labelsx[key]} (n={len(vals)})",'body')
            text(lines,x,488,f"Median {med:.1f} days",'small')
        else:
            text(lines,x,466,f"{labelsx[key]} (n=0)",'body')
    text(lines,28,250,'Documented wrist-related duration (log scale)','body','middle')
    lines.append('</svg>')
    path.write_text('\n'.join(lines),encoding='utf-8')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--review-dir',required=True)
    ap.add_argument('--private-analysis-json',required=True)
    ap.add_argument('--output-dir',required=True)
    args=ap.parse_args()
    review_dir=Path(args.review_dir)
    anatomy,state,proc=load_gold(review_dir)
    result=json.loads(Path(args.private_analysis_json).read_text(encoding='utf-8'))
    out=Path(args.output_dir);out.mkdir(parents=True,exist_ok=True)
    figure1_cohort_flow(cohort_counts(anatomy,state,proc),out/'Figure1_physician_cohort_flow.svg')
    figure2_composition(result,out/'Figure2_oper operative_composition.svg'.replace(' ',''))
    figure3_duration(duration_points(state,proc),out/'Figure3_duration_by_graft.svg')
    print(f'wrote private manuscript figures to {out}')


if __name__=='__main__':
    main()
