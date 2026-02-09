import json
import time
import streamlit as st

from src.eval.sus import SUS_ITEMS, compute_sus_score
from src.eval.logging import log_event, logs_to_df, export_logs

def render_evaluation(state: dict):
    st.subheader("SUS (System Usability Scale) + Export")
    st.caption("Capture SUS items and export logs as CSV/JSON for your Results section.")

    sus_responses = []
    st.write("Rate each statement (1 = strongly disagree, 5 = strongly agree):")
    for i, q in enumerate(SUS_ITEMS, start=1):
        sus_responses.append(st.slider(f"SUS {i}: {q}", 1, 5, 3))

    sus_score = compute_sus_score(sus_responses)
    st.metric("SUS Score (0–100)", f"{sus_score:.1f}")

    if st.button("Submit SUS Log"):
        log_event({
            "event": "sus_submit",
            "participant_id": state["participant_id"],
            "task_id": state["task_id"],
            "condition": state["condition"],
            "sus_score": sus_score,
            "sus_items": sus_responses,
            "elapsed_sec": round(time.time() - st.session_state.start_ts, 3),
        })
        st.success("Logged SUS.")

    st.divider()
    st.subheader("Export Logs")

    df_logs = logs_to_df()
    if df_logs.empty:
        st.info("No logs yet. Submit a decision and/or SUS to create entries.")
        return

    st.dataframe(df_logs, use_container_width=True)

    if st.button("Export logs to artifacts folder"):
        csv_path, json_path = export_logs(state["artifacts_dir"])
        st.success(f"Exported: {csv_path.as_posix()} and {json_path.as_posix()}")

    csv_bytes = df_logs.to_csv(index=False).encode("utf-8")
    st.download_button("Download logs.csv", data=csv_bytes, file_name="logs.csv", mime="text/csv")

    json_bytes = json.dumps(st.session_state.logs, indent=2).encode("utf-8")
    st.download_button("Download logs.json", data=json_bytes, file_name="logs.json", mime="application/json")




