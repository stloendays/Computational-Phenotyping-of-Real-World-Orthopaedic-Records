"""Deterministic phenotype rules used by the public research pipeline.

This module contains no patient data and is intentionally dependency-free so that
core anatomical/source-scope logic can be tested in CI.
"""
from __future__ import annotations
import re

HALLUX_RE = re.compile(r'拇外翻|踇外翻|足母.?外翻|拇囊炎|踇囊炎|足母.?囊炎|(?:拇|踇)趾外翻|第一足趾外翻')
CMC_RE = re.compile(r'第一腕掌关节|第[一1]腕掌关节|拇指腕掌关节|拇指.?CMC|大多角骨.*(?:关节|切除)')
SCAPHOID_WRIST_RE = re.compile(r'(?:左|右|双)?腕.{0,6}舟骨|(?:左|右|双)?手.{0,6}舟骨|舟骨.{0,8}(?:腕|手)|舟骨(?:腰部|近极|远极)')
SCAPHOID_FOOT_RE = re.compile(r'足舟骨|足部.{0,8}舟骨|踝.{0,8}舟骨|跗骨.{0,8}舟骨')
SCAPHOID_CHRONIC_RE = re.compile(r'骨不连|不连接|不愈合|陈旧性|陈旧|慢性|SNAC', re.I)
BILATERAL_RE = re.compile(r'双足|双侧|双拇|双趾|双手|双腕')


def is_hallux_valgus(text: str) -> bool:
    return bool(HALLUX_RE.search(text or ''))


def is_first_cmc_oa(text: str) -> bool:
    return bool(CMC_RE.search(text or ''))


def is_wrist_scaphoid(text: str) -> bool:
    text = text or ''
    wrist = bool(SCAPHOID_WRIST_RE.search(text))
    foot_only = bool(SCAPHOID_FOOT_RE.search(text)) and not bool(re.search(r'腕|手', text))
    return wrist and not foot_only


def is_established_scaphoid_chronic_nonunion(clinical_text: str) -> bool:
    """Assign chronic/nonunion status from non-operative clinical text only.

    The caller must pass diagnosis/complaint/examination text, not operative text.
    This source-scope restriction prevents circularity when treatment is the
    downstream comparison variable.
    """
    return bool(SCAPHOID_CHRONIC_RE.search(clinical_text or ''))


def has_bilateral_mention(clinical_text: str) -> bool:
    return bool(BILATERAL_RE.search(clinical_text or ''))
