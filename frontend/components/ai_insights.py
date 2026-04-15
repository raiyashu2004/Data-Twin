"""AI Insights component – chat with your personal data twin."""

import requests
import streamlit as st

API_BASE = "http://localhost:8000/api"

_EXAMPLE_QUESTIONS = [
    "Why was my productivity low this week?",
    "How can I improve my sleep quality?",
    "What is the relationship between my screen time and productivity?",
    "How can I reduce my burnout risk?",
    "What habits should I build to improve my study hours?",
]


def render():
    st.title("🤖 AI Insights")
    st.markdown(
        "Ask your **Personal Data Twin** anything about your behaviour and habits. "
        "The AI will analyse your patterns and provide personalised recommendations."
    )

    st.subheader("💬 Ask a question")
    example = st.selectbox("Or pick an example question:", ["(Type your own)"] + _EXAMPLE_QUESTIONS)
    question = st.text_input(
        "Your question:",
        value="" if example == "(Type your own)" else example,
        placeholder="e.g. Why was my productivity low this week?",
    )

    if st.button("🔍 Get Insight", type="primary") and question.strip():
        with st.spinner("Thinking..."):
            try:
                resp = requests.post(
                    f"{API_BASE}/insights/ask",
                    json={"question": question},
                    timeout=30,
                )
                resp.raise_for_status()
                data = resp.json()
                st.markdown("---")
                st.subheader("💡 Insight")
                st.info(data["answer"])
                st.caption(f"Source: {data.get('source', 'ai')}")
            except Exception as e:
                st.error(f"Could not get insight: {e}")
                st.info(
                    "Make sure the FastAPI backend is running: "
                    "`uvicorn backend.main:app --reload`"
                )

    # ── Weekly summary ────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📋 Weekly Behavioural Summary")
    if st.button("📊 Load Summary"):
        try:
            resp = requests.get(f"{API_BASE}/insights/summary", timeout=5)
            resp.raise_for_status()
            summary = resp.json()
            if "message" in summary:
                st.info(summary["message"])
            else:
                st.write(f"**Days tracked:** {summary['total_days']}")
                st.write(
                    f"**Date range:** {summary['date_range']['from']} "
                    f"→ {summary['date_range']['to']}"
                )
                import pandas as pd
                stats_df = pd.DataFrame(summary["statistics"]).T
                st.dataframe(stats_df)
        except Exception as e:
            st.error(f"Could not load summary: {e}")
