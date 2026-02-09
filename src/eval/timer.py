import time
import streamlit as st

from src.eval.logging import log_event


def init_task_timer():
    if "task_timer_running" not in st.session_state:
        st.session_state.task_timer_running = False
    if "task_timer_start_ts" not in st.session_state:
        st.session_state.task_timer_start_ts = None
    if "task_timer_task_id" not in st.session_state:
        st.session_state.task_timer_task_id = None


def start_task_timer(participant_id: str, task_id: str, condition: str):
    init_task_timer()
    if st.session_state.task_timer_running:
        return
    st.session_state.task_timer_running = True
    st.session_state.task_timer_start_ts = time.time()
    st.session_state.task_timer_task_id = task_id

    event = {
        "event": "task_timer_start",
        "participant_id": participant_id,
        "task_id": task_id,
        "condition": condition,
    }
    snapshot = st.session_state.get("latest_snapshot")
    if snapshot:
        event.update(snapshot)
    log_event(event)


def stop_task_timer(participant_id: str, task_id: str, condition: str):
    init_task_timer()
    if not st.session_state.task_timer_running or st.session_state.task_timer_start_ts is None:
        return None

    elapsed = time.time() - st.session_state.task_timer_start_ts
    st.session_state.task_timer_running = False
    st.session_state.task_timer_start_ts = None

    log_event({
        "event": "task_timer_stop",
        "participant_id": participant_id,
        "task_id": task_id,
        "condition": condition,
        "elapsed_sec": round(elapsed, 3),
    })
    return elapsed


def render_task_timer_controls(participant_id: str, task_id: str, condition: str):
    init_task_timer()
    st.subheader("Task Timer (Objective Completion Time)")

    c1, c2, c3 = st.columns([1, 1, 2])

    with c1:
        if st.button("Start Task Timer"):
            start_task_timer(participant_id, task_id, condition)

    with c2:
        if st.button("Stop Task Timer"):
            elapsed = stop_task_timer(participant_id, task_id, condition)
            if elapsed is not None:
                st.success(f"Task time: {elapsed:.2f} seconds")

    with c3:
        running = st.session_state.task_timer_running
        current = st.session_state.task_timer_task_id
        st.caption(f"Status: {'RUNNING' if running else 'STOPPED'} | Current task: {current or 'None'}")

