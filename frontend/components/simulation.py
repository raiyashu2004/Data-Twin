"""Simulation component – 'what-if' scenario explorer."""

import requests
import streamlit as st

API_BASE = "http://localhost:8000/api"


def render():
    st.title("🔮 What-If Simulation")
    st.markdown(
        "Adjust the sliders below to simulate changes to your daily routine "
        "and see the predicted impact on your **productivity** and **burnout risk**."
    )

    col1, col2 = st.columns(2)
    sleep_delta = col1.slider("Sleep change (hrs)", -4.0, 4.0, 0.0, 0.5)
    screen_delta = col2.slider("Screen time change (hrs)", -6.0, 6.0, 0.0, 0.5)
    study_delta = col1.slider("Study/work change (hrs)", -4.0, 4.0, 0.0, 0.5)
    exercise_delta = col2.slider("Exercise change (min)", -60.0, 120.0, 0.0, 5.0)

    if st.button("▶️ Run Simulation", type="primary"):
        payload = {
            "sleep_hours_delta": sleep_delta,
            "screen_time_delta": screen_delta,
            "study_hours_delta": study_delta,
            "exercise_minutes_delta": exercise_delta,
        }
        try:
            resp = requests.post(f"{API_BASE}/simulation/run", json=payload, timeout=10)
            resp.raise_for_status()
            result = resp.json()

            st.markdown("---")
            col1, col2 = st.columns(2)
            col1.metric(
                "🎯 Predicted Productivity Score",
                f"{result['predicted_productivity_score']:.1f} / 100",
            )
            burnout_pct = result["predicted_burnout_risk"] * 100
            col2.metric(
                "🔥 Predicted Burnout Risk",
                f"{burnout_pct:.1f}%",
                delta=f"{burnout_pct - 40:.1f}% vs baseline",
                delta_color="inverse",
            )

            st.subheader("💡 Recommendations")
            for rec in result["recommendations"]:
                st.success(f"✅ {rec}")
        except Exception as e:
            st.error(f"Simulation failed: {e}")
            st.info(
                "Make sure the FastAPI backend is running: "
                "`uvicorn backend.main:app --reload`"
            )
