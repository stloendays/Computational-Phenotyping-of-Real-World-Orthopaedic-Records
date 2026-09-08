"""Deterministic phenotype rules used by the public research pipeline.

This module contains no patient data and is intentionally dependency-free so that
core anatomical/source-scope logic can be tested in CI.
"""
from __future__ import annotations
import re

HALLUX_RE = re.compile(r'拇外翻|踇外翻|足母.?外翻|拇囊炎|踇囊炎|足母.?囊炎|(?:拇|踇)趾外翻|第一足趾外翻')
CMC_RE = re.compile(r'第一腕掌关节|第[一1]腕掌关节|拇指腕掌关节|拇指.?CMC|大多角骨.*(?:关节|切除)')

# High-specificity wrist-scaphoid evidence. "手" is never used as a generic
# standalone context because common words such as "手术" and "手法" caused
# false wrist assignments in the initial audit.
SCAPHOID_STRONG_WRIST_RE = re.compile(
    r'(?:左|右|双)?腕.{0,10}舟骨|'
    r'(?:左|右|双)?手(?:部|腕)?舟骨|'
    r'舟骨.{0,10}腕|'
    r'舟骨(?:腰部|近极|远极)|'
    r'鼻烟窝.{0,20}舟骨|舟骨.{0,20}鼻烟窝'
)
SCAPHOID_FOOT_RE = re.compile(
    r'足舟骨|足舟状骨|足部.{0,10}舟骨|踝.{0,10}舟骨|跗骨.{0,10}舟骨|足背.{0,20}舟骨'
)
SCAPHOID_GENERIC_RE = re.compile(
    r'舟骨(?:骨折|骨不连|骨折不连接|骨折不愈合)|舟骨.*(?:骨折|不连接|不愈合)'
)
SCAPHOID_WRIST_CONTEXT_RE = re.compile(r'腕部|左腕|右腕|腕关节|腕掌|鼻烟窝')
SCAPHOID_CHRONIC_RE = re.compile(r'骨不连|不连接|不愈合|陈旧性|陈旧|慢性|SNAC', re.I)
BILATERAL_RE = re.compile(r'双足|双侧|双拇|双趾|双手|双腕')


def is_hallux_valgus(text: str) -> bool:
    return bool(HALLUX_RE.search(text or ''))


def is_first_cmc_oa(text: str) -> bool:
    return bool(CMC_RE.search(text or ''))


def scaphoid_anatomy_class(text: str) -> str:
    """Return high-specificity anatomy class for a candidate record.

    Classes:
      - wrist_scaphoid: strong wrist evidence, or generic scaphoid evidence
        plus explicit wrist context in the absence of explicit foot-navicular evidence;
      - foot_navicular: explicit foot-navicular evidence without strong wrist evidence;
      - ambiguous: generic or otherwise insufficient evidence.

    If an admission genuinely documents both a foot navicular lesion and explicit
    wrist/hand scaphoid disease, the strong wrist evidence is retained. This avoids
    losing multi-site trauma while preventing generic words such as "手术" from
    being interpreted as hand anatomy.
    """
    text = text or ''
    if SCAPHOID_STRONG_WRIST_RE.search(text):
        return 'wrist_scaphoid'
    if SCAPHOID_FOOT_RE.search(text):
        return 'foot_navicular'
    if SCAPHOID_GENERIC_RE.search(text) and SCAPHOID_WRIST_CONTEXT_RE.search(text):
        return 'wrist_scaphoid'
    return 'ambiguous'


def is_wrist_scaphoid(text: str) -> bool:
    return scaphoid_anatomy_class(text) == 'wrist_scaphoid'


def is_established_scaphoid_chronic_nonunion(clinical_text: str) -> bool:
    """Assign chronic/nonunion status from non-operative clinical text only.

    The caller must pass diagnosis/complaint/examination text, not operative text.
    This source-scope restriction prevents circularity when treatment is the
    downstream comparison variable.
    """
    return bool(SCAPHOID_CHRONIC_RE.search(clinical_text or ''))


def has_bilateral_mention(clinical_text: str) -> bool:
    return bool(BILATERAL_RE.search(clinical_text or ''))
