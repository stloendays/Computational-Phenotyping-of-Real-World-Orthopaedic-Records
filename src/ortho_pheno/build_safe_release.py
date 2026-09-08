#!/usr/bin/env python3
"""Generate public aggregate artifacts from the local 18-file clinical archive.

The script NEVER writes patient-level rows, identifiers, raw notes, raw reports,
or raw laboratory records. Raw files remain local and are only read in memory.
"""

from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import csv
import math
import re
import statistics
import sys

from openpyxl import load_workbook

sys.path.insert(0, str(Path(__file__).resolve().parent))
from legacy_xls import parse_biff

DISEASES = {
    "hallux_valgus": "拇外翻",
    "first_cmc_oa": "腕掌关节炎",
    "scaphoid_fracture": "舟骨骨折",
}
DIRECT_IDS = {"姓名", "住院id", "住院流水号", "住院号", "病案号", "电话", "联系人电话", "就诊卡号", "申请单ID"}
STRICT = {
    "hallux_valgus": re.compile(r"拇外翻|踇外翻|足母.?外翻|拇囊炎|踇囊炎|足母.?囊炎|(?:拇|踇)趾外翻|第一足趾外翻"),
    "first_cmc_oa": re.compile(r"第一腕掌关节|第[一1]腕掌关节|拇指腕掌关节|拇指.?CMC|大多角骨.*(?:关节|切除)"),
    "scaphoid_fracture": re.compile(r"(?:左|右|双)?腕.{0,6}舟骨|(?:左|右|双)?手.{0,6}舟骨|舟骨.{0,8}(?:腕|手)"),
}
CHRONIC = re.compile(r"骨不连|不连接|不愈合|陈旧|SNAC")
PROCEDURES = {
    "hallux_valgus": {"osteotomy": r"截骨", "chevron": r"Chevron", "akin": r"Akin", "scarf": r"Scarf", "fusion": r"融合", "k_wire": r"克氏针|钢针", "soft_tissue": r"肌腱|韧带|关节囊|松解", "resection": r"切除"},
    "first_cmc_oa": {"trapeziectomy": r"大多角骨.*切除|切除.*大多角骨", "tendon_procedure": r"肌腱", "ligament_procedure": r"韧带", "arthroplasty": r"关节成形|关节置换", "fusion": r"融合"},
    "scaphoid_fracture": {"internal_fixation": r"内固定|螺钉|空心钉|钢针", "bone_graft": r"植骨|取骨", "fusion": r"融合", "debridement": r"清创|病灶清除", "hardware_removal": r"取出内固定|内固定.*去除"},
}


def norm_id(value):
    if value is None:
        return None
    text = str(value).strip()
    if text.endswith(".0") and text[:-2].isdigit():
        text = text[:-2]
    return text or None


def disease_from_filename(name):
    for key, label in DISEASES.items():
        if label in name or name.startswith(label.replace("患者", "")):
            return key
    if name.startswith("拇外翻"):
        return "hallux_valgus"
    if name.startswith("腕掌关节炎"):
        return "first_cmc_oa"
    if name.startswith("舟骨骨折"):
        return "scaphoid_fracture"
    return "unknown"


def module_from_filename(name):
    if name.endswith("检查.xls"):
        return "imaging_exam"
    if name.endswith("检验.xls"):
        return "laboratory"
    if "主诉和专科查体" in name:
        return "complaint_exam"
    if "基本信息和诊断信息" in name:
        return "demographics_diagnoses"
    if "能查到手术内容" in name:
        return "detailed_operating_note"
    if "无法查询手术内容" in name or "能无法查询手术内容" in name:
        return "surgery_name_only"
    return "other"


def iter_xlsx(path):
    wb = load_workbook(path, read_only=True, data_only=True)
    for ws in wb.worksheets:
        headers = [str(ws.cell(1, c).value).strip() if ws.cell(1, c).value is not None else "" for c in range(1, ws.max_column + 1)]
        rows = []
        for values in ws.iter_rows(min_row=2, values_only=True):
            rows.append({headers[i]: values[i] for i in range(len(headers)) if headers[i]})
        yield ws.title, headers, rows


def as_datetime(value):
    if isinstance(value, datetime):
        return value
    return None


def percentile(values, p):
    values = sorted(values)
    if not values:
        return None
    x = (len(values) - 1) * p
    lo, hi = math.floor(x), math.ceil(x)
    return values[lo] if lo == hi else values[lo] + (values[hi] - values[lo]) * (x - lo)


def suppress(n):
    return "<5" if 0 < n < 5 else str(n)


def write_csv(path, rows, columns):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def build(raw_dir, out_dir):
    raw_dir, out_dir = Path(raw_dir), Path(out_dir)
    records = {key: defaultdict(lambda: {"text": [], "sex": None, "age": None, "height": None, "weight": None, "admit": None, "complaint": False, "exam": False, "surgery": False, "detail": False, "surgery_text": []}) for key in DISEASES}
    inventory = []

    for path in sorted(raw_dir.glob("*.xlsx")):
        disease, module = disease_from_filename(path.name), module_from_filename(path.name)
        sheets, nrows, fields, ids = [], 0, set(), set()
        for sheet, headers, rows in iter_xlsx(path):
            sheets.append(sheet); nrows += len(rows); fields.update(headers)
            for row in rows:
                pid = norm_id(row.get("住院id"))
                if pid:
                    ids.add(pid)
                if disease == "unknown" or not pid:
                    continue
                rec = records[disease][pid]
                for key, value in row.items():
                    if key not in DIRECT_IDS and isinstance(value, str) and value.strip():
                        rec["text"].append(value.strip())
                rec["sex"] = rec["sex"] or row.get("性别")
                rec["age"] = rec["age"] if rec["age"] is not None else row.get("年龄")
                rec["height"] = rec["height"] if rec["height"] is not None else row.get("身高")
                rec["weight"] = rec["weight"] if rec["weight"] is not None else row.get("体重")
                for col in ("入院日期", "入院时间"):
                    dt = as_datetime(row.get(col))
                    if dt and (rec["admit"] is None or dt < rec["admit"]):
                        rec["admit"] = dt
                rec["complaint"] |= bool(row.get("主诉"))
                rec["exam"] |= bool(row.get("专科查体"))
                rec["surgery"] |= bool(row.get("手术时间") or row.get("手术名称") or row.get("手术记录内容"))
                if row.get("手术记录内容"):
                    rec["detail"] = True
                    rec["surgery_text"].append(str(row["手术记录内容"]))
                if row.get("手术名称"):
                    rec["surgery_text"].append(str(row["手术名称"]))
        inventory.append({"disease": disease, "module": module, "source_file": path.name, "format": "xlsx", "sheets": "|".join(sheets), "data_rows": nrows, "columns": len(fields), "unique_admission_keys": len(ids), "contains_direct_identifiers": "yes", "public_release": "no"})

    strict = {disease: {pid for pid, rec in recs.items() if STRICT[disease].search(" ".join(rec["text"]))} for disease, recs in records.items()}
    exam_coverage = {key: set() for key in DISEASES}
    lab_coverage = {key: defaultdict(set) for key in DISEASES}

    for path in sorted(raw_dir.glob("*.xls")):
        disease, module = disease_from_filename(path.name), module_from_filename(path.name)
        parsed = parse_biff(path)
        sheets, nrows, ncols, ids = [], 0, 0, set()
        for sheet, rows in parsed.items():
            sheets.append(sheet); nrows += max(0, len(rows) - 1); ncols = max(ncols, len(rows[0]) if rows else 0)
            if not rows or "住院流水号" not in rows[0]:
                continue
            idx = rows[0].index("住院流水号")
            for row in rows[1:]:
                pid = norm_id(row[idx]) if idx < len(row) else None
                if not pid:
                    continue
                ids.add(pid)
                if module == "imaging_exam":
                    exam_coverage[disease].add(pid)
                elif module == "laboratory":
                    if "凝血" in sheet: category = "coagulation"
                    elif "血常规" in sheet: category = "cbc"
                    elif "红细胞沉" in sheet: category = "esr"
                    elif "C反应蛋白" in sheet: category = "crp"
                    elif "肝功" in sheet: category = "liver_function"
                    elif "肾功" in sheet: category = "kidney_function"
                    elif "离子" in sheet: category = "electrolytes"
                    else: category = "other"
                    lab_coverage[disease][category].add(pid)
        inventory.append({"disease": disease, "module": module, "source_file": path.name, "format": "xls", "sheets": "|".join(sheets), "data_rows": nrows, "columns": ncols, "unique_admission_keys": len(ids), "contains_direct_identifiers": "yes", "public_release": "no"})

    write_csv(out_dir / "data/schema/source_inventory.csv", inventory, list(inventory[0]))

    overview = []
    for disease, recs in records.items():
        ids = strict[disease]
        ages, bmis, female, sex_n = [], [], 0, 0
        for pid in ids:
            rec = recs[pid]
            try:
                age = float(rec["age"])
                if 0 < age < 120: ages.append(age)
            except Exception: pass
            if rec["sex"] is not None:
                sex_n += 1; female += str(rec["sex"]).strip() in {"女", "女性", "F", "Female"}
            try:
                height, weight = float(rec["height"]), float(rec["weight"])
                if height > 3: height /= 100
                bmi = weight / (height * height)
                if 10 < bmi < 60: bmis.append(bmi)
            except Exception: pass
        overview.append({
            "disease": disease, "candidate_admissions": len(recs), "strict_phenotype_admissions": len(ids),
            "female_percent": f"{100*female/sex_n:.1f}" if sex_n else "", "age_median": f"{statistics.median(ages):.1f}" if ages else "", "age_q1": f"{percentile(ages,.25):.1f}" if ages else "", "age_q3": f"{percentile(ages,.75):.1f}" if ages else "", "bmi_median": f"{statistics.median(bmis):.1f}" if bmis else "",
            "with_complaint": sum(recs[pid]["complaint"] for pid in ids), "with_physical_exam": sum(recs[pid]["exam"] for pid in ids), "with_any_surgery_record": sum(recs[pid]["surgery"] for pid in ids), "with_detailed_operating_note": sum(recs[pid]["detail"] for pid in ids), "with_any_exam_record": len(ids & exam_coverage[disease]),
            "with_cbc": len(ids & lab_coverage[disease]["cbc"]), "with_coagulation": len(ids & lab_coverage[disease]["coagulation"]), "with_esr": len(ids & lab_coverage[disease]["esr"]), "with_crp": len(ids & lab_coverage[disease]["crp"]), "with_liver_function": len(ids & lab_coverage[disease]["liver_function"]), "with_kidney_function": len(ids & lab_coverage[disease]["kidney_function"]), "with_electrolytes": len(ids & lab_coverage[disease]["electrolytes"]),
        })
    write_csv(out_dir / "data/aggregate/cohort_overview.csv", overview, list(overview[0]))

    years = []
    for disease, recs in records.items():
        counts = Counter(recs[pid]["admit"].year for pid in strict[disease] if recs[pid]["admit"])
        years.extend({"disease": disease, "year": year, "strict_admissions": suppress(counts.get(year, 0))} for year in range(2015, 2026))
    write_csv(out_dir / "data/aggregate/year_distribution.csv", years, ["disease", "year", "strict_admissions"])

    procedures = []
    for disease, patterns in PROCEDURES.items():
        denominator = sum(records[disease][pid]["detail"] for pid in strict[disease])
        for label, pattern in patterns.items():
            regex = re.compile(pattern, re.I)
            n = sum(records[disease][pid]["detail"] and regex.search(" ".join(records[disease][pid]["surgery_text"])) is not None for pid in strict[disease])
            procedures.append({"disease": disease, "procedure_phenotype": label, "n": suppress(n), "denominator_detailed_notes": denominator, "percent": "<5" if 0 < n < 5 else (f"{100*n/denominator:.1f}" if denominator else "")})
    write_csv(out_dir / "data/aggregate/procedure_phenotype_counts.csv", procedures, ["disease", "procedure_phenotype", "n", "denominator_detailed_notes", "percent"])

    scaphoid = strict["scaphoid_fracture"]
    chronic_n = sum(CHRONIC.search(" ".join(records["scaphoid_fracture"][pid]["text"])) is not None for pid in scaphoid)
    groups = [
        {"phenotype_group": "established_chronic_or_nonunion", "n": chronic_n, "interpretation": "Text-supported established chronic/nonunion phenotype; not necessarily incident nonunion observed longitudinally."},
        {"phenotype_group": "other_wrist_scaphoid", "n": len(scaphoid) - chronic_n, "interpretation": "Wrist-scaphoid cases without the preregistered chronic/nonunion terms in currently available text."},
    ]
    write_csv(out_dir / "data/aggregate/scaphoid_phenotype_groups.csv", groups, ["phenotype_group", "n", "interpretation"])


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    build(args.raw_dir, args.out_dir)
