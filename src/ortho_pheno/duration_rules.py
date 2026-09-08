"""Dependency-free Chinese clinical duration parsing helpers.

These rules support deterministic pre-validation auditing only. Final clinical
duration variables are physician adjudicated and are not defined by this parser.

A single conversion convention is shared with the physician-Gold analysis:
1 year = 365.25 days and 1 month = 365.25 / 12 days. This makes 12 months and
1 year numerically identical rather than introducing a trivial rounding mismatch.
"""
from __future__ import annotations

import re

DAYS_PER_YEAR = 365.25
DAYS_PER_MONTH = DAYS_PER_YEAR / 12.0
DAYS_PER_WEEK = 7.0
DAYS_PER_HOUR = 1.0 / 24.0

DURATION_UNIT_TO_DAYS = {
    'hours': DAYS_PER_HOUR,
    'days': 1.0,
    'weeks': DAYS_PER_WEEK,
    'months': DAYS_PER_MONTH,
    'years': DAYS_PER_YEAR,
}

CN = {
    '一':1, '二':2, '两':2, '三':3, '四':4, '五':5,
    '六':6, '七':7, '八':8, '九':9, '十':10,
}
NUM = r'(?:\d+(?:\.\d+)?|[一二三四五六七八九十两]+)'

# Order matters. Half-unit expressions must be consumed before generic units so
# that ``1个半月`` is not truncated to ``1个月`` and ``1年半`` is not truncated
# to ``1年``.
DURATION_PATTERNS = (
    (re.compile(fr'({NUM})\s*年半'), lambda v: (v + 0.5) * DAYS_PER_YEAR),
    (re.compile(fr'({NUM})\s*个?半月'), lambda v: (v + 0.5) * DAYS_PER_MONTH),
    (re.compile(r'半年'), lambda _v: 0.5 * DAYS_PER_YEAR),
    (re.compile(fr'({NUM})\s*年'), lambda v: v * DAYS_PER_YEAR),
    (re.compile(fr'({NUM})\s*个?月'), lambda v: v * DAYS_PER_MONTH),
    (re.compile(fr'({NUM})\s*(?:周|星期)'), lambda v: v * DAYS_PER_WEEK),
    (re.compile(fr'({NUM})\s*(?:天|日)'), lambda v: v),
    (re.compile(fr'({NUM})\s*小时'), lambda v: v * DAYS_PER_HOUR),
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


def convert_duration_to_days(value: float, unit: str):
    """Convert a physician-adjudicated duration value to days using the shared convention."""
    factor = DURATION_UNIT_TO_DAYS.get(unit)
    if factor is None:
        raise ValueError(f'unsupported duration unit: {unit!r}')
    return float(value) * factor


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
