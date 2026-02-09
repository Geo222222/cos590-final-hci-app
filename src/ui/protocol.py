import streamlit as st

from src.ui.figures import render_architecture_figure
from src.eval.timer import render_task_timer_controls


def render_protocol(state: dict):
    st.header("Study Protocol (Built-In)")
    st.write(
        "This page documents the evaluation procedure used to compare interface conditions. "
        "It is included to support reproducibility and traceability in the IEEE paper."
    )

    st.subheader("Experimental Conditions")
    st.markdown(
        "- **EXPLANATION_OFF:** Recommendation-only interface.\n"
        "- **EXPLANATION_ON:** Recommendation + explanation + optional counterfactual.\n"
        "\n"
        "The recommendation logic is fixed across both conditions to isolate the effect of explanation transparency."
    )

    st.subheader("Suggested Tasks")
    st.markdown(
        "Use the following tasks for a small-scale evaluation (3–5 participants):\n"
        "- **T1:** Interpret the risk level and recommendation.\n"
        "- **T2:** Adjust allocation weights to reduce risk score.\n"
        "- **T3:** Report trust and confidence; compare experience between conditions.\n"
    )

    st.subheader("Measures Collected")
    st.markdown(
        "- **Decision:** Accept / Reject / Unsure\n"
        "- **Confidence (1–7)** and **Trust (1–7)**\n"
        "- **Objective time:** Task Timer start/stop logs\n"
        "- **Usability:** SUS score (0–100)\n"
        "- Export: CSV/JSON logs for analysis\n"
    )

    st.divider()

    # Add objective timer controls
    render_task_timer_controls(
        participant_id=state["participant_id"],
        task_id=state["task_id"],
        condition=state["condition"],
    )

    st.divider()

    # Generate the architecture diagram figure
    render_architecture_figure(
        export_dir=state["artifacts_dir"],
        filename_prefix=state["artifacts_prefix"],
    )

    st.divider()
    st.subheader("Paper Tip")
    st.write(
        "Include the exported architecture PNG as **Figure 1** in your IEEE paper, "
        "and include screenshots from the Dashboard and Explainability tabs as additional figures."
    )
