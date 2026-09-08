"""Dependency-free Chinese clinical duration parsing helpers.

These rules support deterministic pre-validation auditing only. Final clinical
duration variables are physician adjudicated and are not defined by this parser.
"""
from __future__ import annotations

import re

CN = {
    '一':1, '二':2, '两':2, '三':3, '四':4, '五':5,
    '六':6, '七':7, '八':8, '九':9, '十':10,
}
NUM = r'(?:\d+(?:\.\d+)?|[一二三四五六七八九十两]+)'

# Order matters. Half-unit expressions must be consumed before generic units so
# that ``1个半月`` is not truncated to ``1个月`` and ``1年半`` is not truncated
# to ``1年``.
DURATION_PATTERNS = (
    (re.compile(fr'({NUM})\s*年半'), lambda v: (v + 0.5) * 365.25),
    (re.compile(fr'({NUM})\s*个?半月'), lambda v: (v + 0.5) * 30.44),
    (re.compile(r'半年'), lambda _v: 0.5 * 365.25),
    (re.compile(fr'({NUM})\s*年'), lambda v: v * 365.25),
    (re.compile(fr'({NUM})\s*个?月'), lambda v: v * 30.44),
    (re.compile(fr'({NUM})\s*(?:周|星期)'), lambda v: v * 7),
    (re.compile(fr'({NUM})\s*(?:天|日)'), lambda v: v),
    (re.compile(fr'({NUM})\s*小时'), lambda v: v / 24),
)


def cn_number(text: str):
    """Parse a small Arabic/Chinese integer or decimal used in duration phrases."""
    try:
        return float(text)
    except Exception:
        pass
    if '十' in text:
        left, right = text.split('十', 1)
        tens = CN.get(left, 1) if left else 1
        ones = CN.get(right, 0) if right else 0
        return 10 * tens + ones
    return CN.get(text)


def extract_duration_days(text: str):
    """Return all non-overlapping duration expressions converted to days."""
    values = []
    occupied = []
    for pattern, convert in DURATION_PATTERNS:
        for match in pattern.finditer(text or ''):
            if any(not (match.end() <= a or match.start() >= b) for a, b in occupied):
                continue
            raw = match.group(1) if match.lastindex else None
            value = 0.5 if raw is None else cn_number(raw)
            if value is None:
                continue
            values.append(float(convert(value)))
            occupied.append((match.start(), match.end()))
    return values
