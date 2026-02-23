import numpy as np
from src.utils.math_utils import clamp01

def risk_score(hhi: float, semidev: float, mdd: float, var: float, es: float) -> float:
    """Computes a normalized risk score from several underlying risk metrics.

    The function normalizes each metric to a [0, 1] scale, where 1 is higher risk,
    and combines them using a weighted average. This is a fixed rule-based score
    designed for controlled HCI experiments.

    Args:
        hhi: Herfindahl-Hirschman Index (concentration).
        semidev: Downside semideviation.
        mdd: Maximum drawdown.
        var: Value-at-Risk.
        es: Expected Shortfall.

    Returns:
        A final, clamped risk score between 0.0 and 1.0.
    """
    hhi_n = clamp01((hhi - 0.2) / (0.6 - 0.2))
    sd_n = clamp01(semidev / 0.03)
    mdd_n = clamp01((-mdd) / 0.30)
    var_n = clamp01((-var) / 0.05) if not np.isnan(var) else 0.0
    es_n = clamp01((-es) / 0.05) if not np.isnan(es) else 0.0
    score = 0.25 * hhi_n + 0.25 * sd_n + 0.25 * mdd_n + 0.15 * var_n + 0.10 * es_n
    return float(clamp01(score))
