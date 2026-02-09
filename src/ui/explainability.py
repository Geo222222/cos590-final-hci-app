import streamlit as st
import pandas as pd

from src.risk.simulation import get_market_data
from src.risk.metrics import (
    portfolio_returns,
    herfindahl_hirschman_index,
    max_drawdown,
    downside_semidev,
    historical_var_es,
)
from src.risk.scoring import risk_score

def render_explainability(state: dict):
    n_assets = state["n_assets"]
    n_periods = state["n_periods"]
    seed = state["seed"]
    alpha = state["alpha"]
    weights = state["weights"]

    asset_rets, _ = get_market_data(n_assets=n_assets, n_periods=n_periods, seed=seed)
    port_rets = portfolio_returns(asset_rets, weights)

    hhi = herfindahl_hirschman_index(weights)
    mdd = max_drawdown(port_rets)
    sd = downside_semidev(port_rets, mar=0.0)
    var, es = historical_var_es(port_rets, alpha=alpha)
    score = risk_score(hhi, sd, mdd, var, es)

    st.subheader("Equations (for IEEE paper support)")
    st.latex(r"HHI = \sum_{i=1}^{N} w_i^2")
    st.latex(r"r_p(t) = \sum_{i=1}^{N} w_i \, r_i(t)")
    st.latex(r"VaR_\alpha = Q_\alpha(r_p)")
    st.latex(r"ES_\alpha = \mathbb{E}[r_p \mid r_p \le VaR_\alpha]")

    st.caption(
        "These are standard, interpretable risk constructs used for portfolio-level assessment. "
        "The recommendation logic is intentionally fixed to isolate interface effects."
    )

    st.subheader("Feature/Metric Traceability Table")
    trace = pd.DataFrame([
        {"Metric": "HHI", "Purpose": "Concentration/diversification", "Interpretation": "Higher = more concentrated"},
        {"Metric": "Semideviation", "Purpose": "Downside volatility", "Interpretation": "Higher = worse downside variability"},
        {"Metric": "Max Drawdown", "Purpose": "Peak-to-trough loss", "Interpretation": "More negative = deeper drawdown"},
        {"Metric": "VaR", "Purpose": "Tail loss threshold", "Interpretation": "More negative = worse tail threshold"},
        {"Metric": "ES", "Purpose": "Average loss in worst tail", "Interpretation": "More negative = worse tail severity"},
        {"Metric": "Risk Score", "Purpose": "Controlled combined score", "Interpretation": f"Current score = {score:.2f}"},
    ])
    st.table(trace)

    st.subheader("Controlled Recommendation Logic (Fixed)")
    st.code(
        "if score < 0.33: LOW -> Maintain\n"
        "elif score < 0.66: MEDIUM -> Rebalance\n"
        "else: HIGH -> Reduce exposure",
        language="text",
    )
