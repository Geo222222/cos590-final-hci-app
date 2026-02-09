import streamlit as st
import numpy as np

from src.risk.metrics import normalize_weights

def render_sidebar():
    st.sidebar.header("Study Mode")
    participant_id = st.sidebar.text_input("Participant ID", value="P001")
    task_id = st.sidebar.selectbox("Task", ["T1", "T2", "T3"], index=0)

    condition = st.sidebar.selectbox(
        "Interface Condition",
        ["EXPLANATION_OFF", "EXPLANATION_ON"],
        index=1 if st.session_state.condition == "EXPLANATION_ON" else 0
    )
    st.session_state.condition = condition

    st.sidebar.caption(
        "Use EXPLANATION_OFF vs EXPLANATION_ON to reproduce the controlled comparison. "
        "Recommendation logic remains fixed."
    )

    st.sidebar.header("Portfolio Inputs")
    n_assets = st.sidebar.slider("Number of assets", 1, 8, 5, 1)
    n_periods = st.sidebar.slider("Return periods (hours)", 250, 4000, 750, 50)

    seed = st.sidebar.number_input("Simulation seed", min_value=1, value=7, step=1)
    alpha = st.sidebar.slider("Tail risk alpha (VaR/ES)", 0.01, 0.10, 0.05, 0.01)

    st.sidebar.header("User Controls (Human-in-the-loop)")
    show_counterfactual = st.sidebar.checkbox("Show counterfactual explanation (optional)", value=True)
    loss_aversion_mode = st.sidebar.checkbox("Loss-aversion framing (emphasize downside)", value=True)
    artifacts_dir = st.sidebar.text_input("Artifacts directory", value="artifacts")
    artifacts_prefix = st.sidebar.text_input("Artifacts filename prefix", value="fig_")

    st.sidebar.subheader("Allocation Weights")
    default_w = np.ones(n_assets) / n_assets
    weights = []
    for i in range(n_assets):
        weights.append(st.sidebar.slider(f"Asset {i+1} weight", 0.0, 1.0, float(default_w[i]), 0.01))
    weights = normalize_weights(np.array(weights))

    return {
        "participant_id": participant_id,
        "task_id": task_id,
        "condition": condition,
        "n_assets": n_assets,
        "n_periods": n_periods,
        "seed": int(seed),
        "alpha": float(alpha),
        "show_counterfactual": show_counterfactual,
        "loss_aversion_mode": loss_aversion_mode,
        "weights": weights,
        "artifacts_dir": artifacts_dir,
        "artifacts_prefix": artifacts_prefix,
    }
