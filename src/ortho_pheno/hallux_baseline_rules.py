"""Conservative deterministic hallux-valgus baseline phenotype rules.

These rules intentionally preserve documentation missingness. Absence of a
positive keyword is not converted into a clinical negative phenotype.
"""
from __future__ import annotations

import re

BILATERAL = re.compile(r'双足|双侧.{0,12}(?:拇|踇|足)|(?:左足.{0,40}右足|右足.{0,40}左足)')
LEFT = re.compile(r'左足|左侧.{0,12}(?:拇|踇|足)')
RIGHT = re.compile(r'右足|右侧.{0,12}(?:拇|踇|足)')

PAIN_NEG = re.compile(r'无(?:明显)?(?:疼痛|痛)|未诉(?:明显)?(?:疼痛|痛)|疼痛不明显')
PAIN_POS = re.compile(r'疼痛|痛')

FUNCTION_NEG = re.compile(r'活动(?:正常|自如)|无(?:明显)?活动受限|功能(?:正常|良好)|行走(?:正常|无明显受限)')
FUNCTION_POS = re.compile(r'活动受限|功能受限|行走受限|影响行走|活动障碍')


def predict_laterality(text: str) -> str:
    text=text or ''
    if BILATERAL.search(text):
        return 'bilateral'
    left=bool(LEFT.search(text)); right=bool(RIGHT.search(text))
    if left and right:
        return 'bilateral'
    if left:
        return 'left'
    if right:
        return 'right'
    return 'undocumented'


def predict_bilateral_disease_mention(text: str) -> str:
    return 'present' if predict_laterality(text)=='bilateral' else 'undocumented'


def predict_pain(text: str) -> str:
    text=text or ''
    if PAIN_NEG.search(text):
        return 'absent'
    if PAIN_POS.search(text):
        return 'present'
    return 'undocumented'


def predict_functional_limitation(text: str) -> str:
    text=text or ''
    if FUNCTION_NEG.search(text):
        return 'absent'
    if FUNCTION_POS.search(text):
        return 'present'
    return 'undocumented'
