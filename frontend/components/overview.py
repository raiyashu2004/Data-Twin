"""Overview component – upload data and view summary metrics."""

import io
import datetime

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
    st.title("📊 Overview Dashboard")
    st.markdown("Upload your daily behavioural data or enter it manually below.")

    # ── Manual entry form ────────────────────────────────────────────────────
    with st.expander("➕ Add a daily entry manually"):
        with st.form("manual_entry"):
            entry_date = st.date_input("Date", value=datetime.date.today())
            col1, col2, col3 = st.columns(3)
            screen = col1.number_input("Screen Time (hrs)", 0.0, 24.0, 6.0, step=0.5)
            study = col2.number_input("Study / Work (hrs)", 0.0, 24.0, 4.0, step=0.5)
            sleep = col3.number_input("Sleep (hrs)", 0.0, 24.0, 7.0, step=0.5)
            col4, col5 = st.columns(2)
            exercise = col4.number_input("Exercise (min)", 0.0, 300.0, 30.0, step=5.0)
            expenses = col5.number_input("Expenses (optional)", 0.0, step=10.0)
            notes = st.text_area("Notes (optional)")
            submitted = st.form_submit_button("Save entry")

        if submitted:
            payload = {
                "entry_date": entry_date.isoformat(),
                "screen_time_hours": screen,
                "study_hours": study,
                "sleep_hours": sleep,
                "exercise_minutes": exercise,
                "expenses": expenses if expenses else None,
                "notes": notes if notes else None,
            }
            try:
                r = requests.post(f"{API_BASE}/data/entry", json=payload, timeout=5)
                r.raise_for_status()
                st.success("Entry saved ✅")
            except Exception as e:
                st.error(f"Could not save entry: {e}")

    # ── CSV upload ───────────────────────────────────────────────────────────
    with st.expander("📂 Upload CSV"):
        csv_file = st.file_uploader("Upload a CSV with your daily data", type=["csv"])
        if csv_file:
            try:
                r = requests.post(
                    f"{API_BASE}/data/upload-csv",
                    files={"file": (csv_file.name, csv_file.getvalue(), "text/csv")},
                    timeout=10,
                )
                r.raise_for_status()
                st.success(f"Imported {r.json()['imported']} rows ✅")
            except Exception as e:
                st.error(f"Upload failed: {e}")

    # ── Summary metrics ──────────────────────────────────────────────────────
    st.markdown("---")
    df = _get_entries()
    if df.empty:
        st.info("No data yet. Add entries above or upload a CSV to get started.")
        return

    df["entry_date"] = pd.to_datetime(df["entry_date"])
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📅 Days tracked", len(df))
    col2.metric("📚 Avg study (hrs)", f"{df['study_hours'].mean():.1f}")
    col3.metric("😴 Avg sleep (hrs)", f"{df['sleep_hours'].mean():.1f}")
    col4.metric("📱 Avg screen (hrs)", f"{df['screen_time_hours'].mean():.1f}")

    st.subheader("Daily activity over time")
    fig = px.line(
        df.sort_values("entry_date"),
        x="entry_date",
        y=["study_hours", "sleep_hours", "screen_time_hours"],
        labels={"value": "Hours", "variable": "Metric"},
        template="plotly_dark",
    )
    st.plotly_chart(fig, use_container_width=True)
