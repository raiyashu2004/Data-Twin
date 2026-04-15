"""
Personal Data Twin – Streamlit Dashboard
==========================================
Main entry point.  Run with:
    streamlit run frontend/app.py
"""

import streamlit as st

from frontend.components import overview, trends, simulation, ai_insights

st.set_page_config(
    page_title="Personal Data Twin",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar navigation ────────────────────────────────────────────────────────
st.sidebar.title("🧠 Personal Data Twin")
st.sidebar.markdown("_Your AI-powered behavioural analytics companion_")

page = st.sidebar.radio(
    "Navigate",
    ["📊 Overview", "📈 Trends", "🔮 Simulation", "🤖 AI Insights"],
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Upload your behavioural data (CSV) or enter daily entries manually "
    "to unlock all features."
)

# ── Page routing ──────────────────────────────────────────────────────────────
if page == "📊 Overview":
    overview.render()
elif page == "📈 Trends":
    trends.render()
elif page == "🔮 Simulation":
    simulation.render()
elif page == "🤖 AI Insights":
    ai_insights.render()
