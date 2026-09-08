"""Dependency-free statistics for small 2x2 clinical comparisons.

The scaphoid manuscript has a sparse operative sample, so its primary binary
analyses use Fisher's exact test rather than asymptotic chi-square tests. This
module implements the fixed-margin two-sided Fisher test, crude odds ratio, and a
simple log-Wald 95% confidence interval when all four cells are non-zero.

No continuity correction is silently applied. When a zero cell prevents a finite
crude OR/CI, the returned value is 0/inf/None as appropriate and the caller must
report the sparse table rather than substitute a corrected estimate without an
explicitly prespecified method.
"""
from __future__ import annotations

import math


def _log_choose(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float('-inf')
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def _hypergeom_probability(a: int, row1: int, row2: int, col1: int, total: int) -> float:
    """Probability of the top-left cell ``a`` under fixed margins."""
    b = row1 - a
    c = col1 - a
    d = row2 - c
    if min(a, b, c, d) < 0:
        return 0.0
    logp = _log_choose(col1, a) + _log_choose(total - col1, b) - _log_choose(total, row1)
    return math.exp(logp)


def fisher_exact_two_sided(a: int, b: int, c: int, d: int) -> float:
    """Return the standard probability-ordering two-sided Fisher exact P value.

    Tables with the same row/column margins whose hypergeometric probability is
    less than or equal to the observed table probability are summed. This matches
    the conventional two-sided definition used by common statistical packages.
    """
    cells = (a, b, c, d)
    if any(int(x) != x or x < 0 for x in cells):
        raise ValueError('2x2 cell counts must be non-negative integers')
    a, b, c, d = map(int, cells)
    row1 = a + b
    row2 = c + d
    col1 = a + c
    total = row1 + row2
    if total == 0:
        raise ValueError('empty 2x2 table')

    observed = _hypergeom_probability(a, row1, row2, col1, total)
    low = max(0, row1 - (total - col1))
    high = min(row1, col1)
    tolerance = max(1e-15, observed * 1e-12)
    p = 0.0
    for candidate in range(low, high + 1):
        prob = _hypergeom_probability(candidate, row1, row2, col1, total)
        if prob <= observed + tolerance:
            p += prob
    return min(1.0, max(0.0, p))


def crude_odds_ratio(a: int, b: int, c: int, d: int):
    """Return the uncorrected cross-product odds ratio."""
    if min(a, b, c, d) < 0:
        raise ValueError('2x2 cell counts must be non-negative')
    numerator = a * d
    denominator = b * c
    if denominator == 0:
        if numerator == 0:
            return None
        return float('inf')
    return numerator / denominator


def log_wald_or_ci95(a: int, b: int, c: int, d: int):
    """Return crude OR and log-Wald 95% CI when all cells are positive.

    The interval is intentionally unavailable for zero-cell tables because this
    helper never applies an unannounced Haldane-Anscombe correction.
    """
    if min(a, b, c, d) <= 0:
        return crude_odds_ratio(a, b, c, d), None, None
    odds_ratio = crude_odds_ratio(a, b, c, d)
    se = math.sqrt(1/a + 1/b + 1/c + 1/d)
    z = 1.959963984540054
    lo = math.exp(math.log(odds_ratio) - z * se)
    hi = math.exp(math.log(odds_ratio) + z * se)
    return odds_ratio, lo, hi


def analyze_2x2(a: int, b: int, c: int, d: int) -> dict:
    """Return a compact manuscript-oriented summary of one 2x2 comparison."""
    odds_ratio, ci_low, ci_high = log_wald_or_ci95(a, b, c, d)
    return {
        'table': {'exposed_yes':a, 'exposed_no':b, 'comparison_yes':c, 'comparison_no':d},
        'odds_ratio_crude': odds_ratio,
        'ci95_log_wald_low': ci_low,
        'ci95_log_wald_high': ci_high,
        'fisher_two_sided_p': fisher_exact_two_sided(a, b, c, d),
    }
