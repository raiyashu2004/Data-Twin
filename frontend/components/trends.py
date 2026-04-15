"""Trends component – visualise patterns and ML clustering."""

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_BASE = "http://localhost:8000/api"


def _get_entries() -> pd.DataFrame:
    try:
        resp = requests.get(f"{API_BASE}/data/entries", timeout=5)
        resp.raise_for_status()
        return pd.DataFrame(resp.json())
    except Exception:
        return pd.DataFrame()


def render():
    st.title("📈 Trends & Patterns")

    df = _get_entries()
    if df.empty:
        st.info("No data available. Please add entries on the Overview page first.")
        return

    df["entry_date"] = pd.to_datetime(df["entry_date"])
    df = df.sort_values("entry_date")

    # ── Weekly aggregation ────────────────────────────────────────────────────
    st.subheader("Weekly averages")
    weekly = (
        df.set_index("entry_date")
        .resample("W")[["study_hours", "sleep_hours", "screen_time_hours", "exercise_minutes"]]
        .mean()
        .reset_index()
    )
    fig = px.bar(
        weekly,
        x="entry_date",
        y=["study_hours", "sleep_hours", "screen_time_hours"],
        barmode="group",
        labels={"value": "Hours", "variable": "Metric"},
        template="plotly_dark",
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Correlation heatmap ───────────────────────────────────────────────────
    st.subheader("Correlation matrix")
    numeric_cols = ["study_hours", "sleep_hours", "screen_time_hours", "exercise_minutes"]
    corr = df[numeric_cols].corr().round(2)
    fig2 = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        template="plotly_dark",
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ── Behaviour clustering (local, no API call needed) ─────────────────────
    st.subheader("Behaviour clustering")
    if len(df) >= 3:
        try:
            import sys
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
            from backend.ml.clustering import cluster

            clustered = cluster(df)
            fig3 = px.scatter(
                clustered,
                x="study_hours",
                y="sleep_hours",
                color="cluster_label",
                size="exercise_minutes",
                hover_data=["entry_date", "screen_time_hours"],
                template="plotly_dark",
                title="Behavioural clusters",
            )
            st.plotly_chart(fig3, use_container_width=True)
        except Exception as e:
            st.warning(f"Clustering unavailable: {e}")
    else:
        st.info("At least 3 entries are required for clustering.")
