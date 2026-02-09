import numpy as np

def clamp01(x: float) -> float:
    return float(max(0.0, min(1.0, x)))

def safe_float(x, default=np.nan):
    try:
        return float(x)
    except Exception:
        return default
    
