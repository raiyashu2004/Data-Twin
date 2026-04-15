"""Analytics service – computes summaries and trends."""

import pandas as pd

from backend.services import data_service


def weekly_summary() -> dict:
    """Return basic weekly statistics from stored data."""
    df = data_service.get_dataframe()
    if df.empty:
        return {"message": "No data available yet. Please upload or enter some data first."}

    df["entry_date"] = pd.to_datetime(df["entry_date"])
    df = df.sort_values("entry_date")

    numeric_cols = ["screen_time_hours", "study_hours", "sleep_hours", "exercise_minutes"]
    stats = df[numeric_cols].describe().round(2).to_dict()

    return {
        "total_days": len(df),
        "date_range": {
            "from": df["entry_date"].min().date().isoformat(),
            "to": df["entry_date"].max().date().isoformat(),
        },
        "statistics": stats,
    }
