import numpy as np

def normalize_weights(w: np.ndarray) -> np.ndarray:
    w = np.array(w, dtype=float)
    w[w < 0] = 0.0
    s = w.sum()
    if s <= 0:
        return np.zeros_like(w)
    return w / s

def herfindahl_hirschman_index(w: np.ndarray) -> float:
    # HHI = sum(w_i^2). Higher -> more concentrated
    w = normalize_weights(w)
    return float(np.sum(w ** 2))

def portfolio_returns(asset_returns: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Calculates the time series of portfolio returns.

    Args:
        asset_returns: A (T x N) array of T periodic returns for N assets.
        w: An (N,) array of portfolio weights.

    Returns:
        A (T,) array of periodic portfolio returns.
    """
    w = normalize_weights(w)
    return asset_returns @ w


def max_drawdown(returns: np.ndarray) -> float:
    """Calculates the largest peak-to-trough drop in portfolio equity.

    Args:
        returns: An array of periodic portfolio returns.

    Returns:
        The maximum drawdown as a negative float.
    """
    # returns: periodic returns
    equity = np.cumprod(1 + returns)
    peak = np.maximum.accumulate(equity)
    dd = (equity - peak) / peak
    return float(dd.min())  # negative number


def downside_semidev(returns: np.ndarray, mar: float = 0.0) -> float:
    # Semideviation below MAR (minimum acceptable return)
    downside = np.minimum(0.0, returns - mar)
    return float(np.sqrt(np.mean(downside ** 2)))


def historical_var_es(returns: np.ndarray, alpha: float = 0.05):
    """Calculates historical Value-at-Risk (VaR) and Expected Shortfall (ES).

    Args:
        returns: An array of periodic portfolio returns.
        alpha: The significance level for VaR/ES (e.g., 0.05 for 95% confidence).

    Returns:
        A tuple containing the VaR and ES as floats.
    """
    # Historical simulation VaR/ES: returns are periodic.
    r = np.sort(returns)
    idx = max(0, int(np.floor(alpha * len(r))) - 1)
    var = float(r[idx]) if len(r) else np.nan
    tail = r[: idx + 1] if len(r) else np.array([])
    es = float(np.mean(tail)) if len(tail) else np.nan
    return var, es
