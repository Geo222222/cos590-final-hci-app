import time
import uuid
import pandas as pd
import streamlit as st

from src.utils.time_utils import now_iso

def init_session():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "start_ts" not in st.session_state:
        st.session_state.start_ts = time.time()
    if "logs" not in st.session_state:
        st.session_state.logs = []
    if "condition" not in st.session_state:
        st.session_state.condition = "EXPLANATION_ON"

def log_event(event: dict):
    e = dict(event)
    e["timestamp_utc"] = now_iso()
    e["session_id"] = st.session_state.session_id
    st.session_state.logs.append(e)

def logs_to_df():
    return pd.DataFrame(st.session_state.logs) if st.session_state.logs else pd.DataFrame()

def export_logs(artifacts_dir: str):
    from pathlib import Path
    import json

    export_dir = Path(artifacts_dir)
    export_dir.mkdir(parents=True, exist_ok=True)

    df_logs = logs_to_df()
    csv_path = export_dir / "logs.csv"
    json_path = export_dir / "logs.json"

    df_logs.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(st.session_state.logs, indent=2), encoding="utf-8")

    return csv_path, json_path
