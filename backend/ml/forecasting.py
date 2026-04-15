"""
ML – Time-Series Forecasting
==============================
Forecasts future values (study hours, sleep duration) using linear regression
as a lightweight baseline.  Swap with Prophet or ARIMA for production use.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def forecast(df: pd.DataFrame, column: str, days_ahead: int = 7) -> list[dict]:
    """
    Forecast *column* for the next *days_ahead* days using a simple linear
    trend fitted on the historical data in *df*.

    Returns a list of dicts with ``date`` and ``predicted_value`` keys.
    """
    if df.empty or column not in df.columns:
        return []

    df = df.copy()
    df["entry_date"] = pd.to_datetime(df["entry_date"])
    df = df.sort_values("entry_date").dropna(subset=[column])

    if len(df) < 2:
        return []

    # Encode dates as integer day offsets
    t0 = df["entry_date"].min()
    df["t"] = (df["entry_date"] - t0).dt.days

    X = df[["t"]].values
    y = df[column].values

    model = LinearRegression()
    model.fit(X, y)

    last_t = int(df["t"].max())
    future_dates = [
        t0 + pd.Timedelta(days=last_t + i + 1) for i in range(days_ahead)
    ]
    future_t = np.array([[last_t + i + 1] for i in range(days_ahead)])
    predictions = model.predict(future_t)

    return [
        {"date": d.date().isoformat(), "predicted_value": round(float(v), 3)}
        for d, v in zip(future_dates, predictions)
    ]
