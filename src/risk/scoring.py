import numpy as np
from src.utils.math_utils import clamp01

def risk_score(hhi: float, semidev: float, mdd: float, var: float, es: float) -> float:
    """
    Simple fixed scoring (controlled logic): normalize sub-metrics into [0,1] and combine.
    This is intentionally not a “new financial model” — it is a fixed rule-based score for HCI testing.
    """
    hhi_n = clamp01((hhi - 0.2) / (0.6 - 0.2))
    sd_n = clamp01(semidev / 0.03)
    mdd_n = clamp01((-mdd) / 0.30)
    var_n = clamp01((-var) / 0.05) if not np.isnan(var) else 0.0
    es_n = clamp01((-es) / 0.05) if not np.isnan(es) else 0.0
    score = 0.25 * hhi_n + 0.25 * sd_n + 0.25 * mdd_n + 0.15 * var_n + 0.10 * es_n
    return float(clamp01(score))
