"""Canonical deterministic procedure rules and disease-note relevance filters.

The distinction between *module availability* and *disease-concordant note
availability* prevents an unrelated operation documented during the same
admission from being misclassified as treatment of the target orthopaedic
condition.
"""
from __future__ import annotations

import re

PROCEDURE_PATTERNS = {
    'hallux_valgus': {
        'osteotomy': r'截骨|osteotomy',
        'chevron': r'Chevron|chevron',
        'akin': r'Akin|AKIN|akin',
        'scarf': r'Scarf|SCARF|scarf',
        'fusion': r'融合|fusion|arthrodesis',
        'k_wire': r'克氏针|钢针|K[- ]?wire|Kirschner',
        'resection': r'切除|resection',
        'soft_tissue': r'肌腱|韧带|关节囊|松解|tendon|ligament',
    },
    'scaphoid_fracture': {
        'internal_fixation': r'内固定|螺钉|空心钉|钢针|screw',
        'bone_graft': r'植骨|取骨|bone graft',
        'reconstruction': r'重建|reconstruction',
        'fusion': r'融合|arthrodesis',
        'hardware_removal': r'取出内固定|内固定.*去除|内固定.*取出|取出.*螺钉',
        'debridement': r'清创|病灶清除|清除.*病灶',
    },
    'first_cmc_oa': {
        'trapeziectomy': r'大多角骨.*切除|切除.*大多角骨|trapeziectomy',
        'tendon_procedure': r'肌腱|tendon',
        'ligament_procedure': r'韧带|ligament',
        'arthroplasty': r'关节成形|关节置换|arthroplasty',
        'fusion': r'融合|arthrodesis',
    },
}

DOMAIN_PROCEDURE_ANCHORS = {
    'hallux_valgus': re.compile(
        r'拇外翻|踇外翻|拇趾|踇趾|第一跖|跖骨|跖趾|足|Chevron|Akin|Scarf', re.I
    ),
    'scaphoid_fracture': re.compile(
        r'舟骨|腕部|腕关节|左腕|右腕|鼻烟窝', re.I
    ),
    'first_cmc_oa': re.compile(
        r'第一腕掌|腕掌关节|CMC|大多角骨|第一掌骨|拇指', re.I
    ),
}


def procedure_body(note: str) -> str:
    """Drop header/diagnostic material when a structured operation marker exists."""
    note = note or ''
    i = note.find('手术名称')
    return note[i:] if i >= 0 else note


def note_is_domain_concordant(domain: str, note: str) -> bool:
    if domain not in DOMAIN_PROCEDURE_ANCHORS:
        raise KeyError(f'unknown domain: {domain}')
    return bool(DOMAIN_PROCEDURE_ANCHORS[domain].search(procedure_body(note)))


def disease_concordant_bodies(domain: str, notes) -> list[str]:
    return [procedure_body(n) for n in (notes or []) if note_is_domain_concordant(domain, n)]


def extract_procedure_labels(domain: str, notes, require_domain_concordance: bool = True) -> set[str]:
    if domain not in PROCEDURE_PATTERNS:
        raise KeyError(f'unknown domain: {domain}')
    bodies = disease_concordant_bodies(domain, notes) if require_domain_concordance else [procedure_body(n) for n in (notes or [])]
    text = ' '.join(bodies)
    labels = set()
    for label, pattern in PROCEDURE_PATTERNS[domain].items():
        if re.search(pattern, text, re.I):
            labels.add(label)
    return labels
