import streamlit as st
from src.eval.logging import init_session
from src.ui.sidebar import render_sidebar
from src.ui.dashboard import render_dashboard
from src.ui.explainability import render_explainability
from src.ui.evaluation import render_evaluation
from src.ui.protocol import render_protocol

st.set_page_config(page_title="AI-Assisted Investment Risk Decision Support", layout="wide")
st.title("AI-Assisted Investment Decision Support System (HCI Prototype)")
st.caption(
    "Portfolio-level risk decision support with controlled recommendation logic and an evaluation mode "
    "supporting two interface conditions: recommendation-only vs recommendation+explanation."
)

init_session()

state = render_sidebar()

tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Explainability", "Evaluation & Export", "Protocol & Figures"])
with tab1:
    render_dashboard(state)
with tab2:
    render_explainability(state)
with tab3:
    render_evaluation(state)
with tab4:
    render_protocol(state)
