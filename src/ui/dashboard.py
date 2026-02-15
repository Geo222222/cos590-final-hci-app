import time
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from src.risk.simulation import get_market_data
from src.risk.metrics import (
    portfolio_returns,
    herfindahl_hirschman_index,
    max_drawdown,
    downside_semidev,
    historical_var_es,
)
from src.risk.scoring import risk_score
from src.risk.recommendations import (
    recommendation_from_score,
    explanation_text,
    counterfactual_suggestion,
)
from src.eval.logging import log_event
from src.ui.market import render_market_data_chart

def render_dashboard(state: dict):
    render_market_data_chart()
    st.divider()
    n_assets = state["n_assets"]
    n_periods = state["n_periods"]
    seed = state["seed"]
    alpha = state["alpha"]
    weights = state["weights"]

    asset_rets, dates = get_market_data(n_assets=n_assets, n_periods=n_periods, seed=seed)
    port_rets = portfolio_returns(asset_rets, weights)

    hhi = herfindahl_hirschman_index(weights)
    mdd = max_drawdown(port_rets)
    sd = downside_semidev(port_rets, mar=0.0)
    var, es = historical_var_es(port_rets, alpha=alpha)

    score = risk_score(hhi, sd, mdd, var, es)
    risk_level, rec, rationale = recommendation_from_score(score)
    explanation_shown = state["condition"] == "EXPLANATION_ON"
    counterfactual_shown = explanation_shown and state["show_counterfactual"]

    st.session_state.latest_snapshot = {
        "n_assets": n_assets,
        "n_periods": n_periods,
        "seed": seed,
        "alpha": alpha,
        "weights": weights.tolist(),
        "risk_level": risk_level,
        "risk_score": float(score),
        "hhi": float(hhi),
        "semidev": float(sd),
        "mdd": float(mdd),
        "var": float(var),
        "es": float(es),
        "machine_action": rec,
        "machine_recommendation_text": rationale,
        "explanation_shown": explanation_shown,
        "counterfactual_shown": counterfactual_shown,
        "loss_aversion_mode": state["loss_aversion_mode"],
    }

    colA, colB, colC, colD = st.columns(4)
    colA.metric("Risk Level", risk_level)
    colB.metric("Risk Score (0–1)", f"{score:.2f}")
    colC.metric("Diversification (HHI)", f"{hhi:.3f}")
    colD.metric("Max Drawdown", f"{mdd:.2%}")

    st.divider()

    left, right = st.columns([1.2, 1])

    with left:
        st.subheader("Portfolio Performance (Historical)")
        fig = plt.figure()
        equity = np.cumprod(1 + port_rets)
        plt.plot(dates, equity)
        plt.title("Equity Curve (Historical)")
        plt.xlabel("Date")
        plt.ylabel("Growth of $1")
        fig.autofmt_xdate()
        st.pyplot(fig)

        st.subheader("Return Distribution")
        fig2 = plt.figure()
        plt.hist(port_rets, bins=40)
        plt.title("Portfolio Returns Histogram")
        plt.xlabel("Return")
        plt.ylabel("Count")
        st.pyplot(fig2)

    with right:
        st.subheader("System Recommendation")

        if state["loss_aversion_mode"]:
            st.warning(f"Recommendation: **{rec}**")
            st.write("This view emphasizes downside risk to support loss-aware decisions.")
        else:
            st.success(f"Recommendation: **{rec}**")

        st.write(rationale)

        metrics_table = pd.DataFrame([{
            "Semideviation (Downside)": sd,
            f"VaR (alpha={alpha:.2f})": var,
            f"ES (alpha={alpha:.2f})": es,
            "HHI (Concentration)": hhi,
            "Max Drawdown": mdd,
        }])
        st.table(metrics_table.style.format(precision=4))

        if explanation_shown:
            st.subheader("Explanation (Why this recommendation?)")
            st.text(explanation_text(hhi, sd, mdd, var, es, score))

            if counterfactual_shown:
                st.subheader("Counterfactual (What would change it?)")
                st.info(counterfactual_suggestion(hhi, sd, mdd, var, es, score))
        else:
            st.caption("Explanation is hidden in this condition (Recommendation-Only).")

    st.divider()

    st.subheader("User Decision (for study logging)")
    decision = st.radio("Do you accept the recommendation?", ["ACCEPT", "REJECT", "UNSURE"], horizontal=True)
    confidence = st.slider("Decision confidence (1–7)", 1, 7, 4)
    trust = st.slider("Trust in system (1–7)", 1, 7, 4)

    if st.button("Submit Decision Log"):
        elapsed = None
        if st.session_state.get("task_timer_start_ts"):
            elapsed = round(time.time() - st.session_state.task_timer_start_ts, 3)
        else:
            elapsed = round(time.time() - st.session_state.start_ts, 3)

        log_event({
            "event": "decision_submit",
            "participant_id": state["participant_id"],
            "task_id": state["task_id"],
            "condition": state["condition"],
            "decision": decision,
            "confidence_1_7": int(confidence),
            "trust_1_7": int(trust),
            "n_assets": n_assets,
            "n_periods": n_periods,
            "seed": seed,
            "alpha": alpha,
            "risk_level": risk_level,
            "risk_score": score,
            "hhi": hhi,
            "semidev": sd,
            "mdd": mdd,
            "var": var,
            "es": es,
            "machine_action": rec,
            "machine_recommendation_text": rationale,
            "explanation_shown": explanation_shown,
            "counterfactual_shown": counterfactual_shown,
            "loss_aversion_mode": state["loss_aversion_mode"],
            "weights": weights.tolist(),
            "elapsed_sec": elapsed,
        })
        st.success("Logged.")
