"""
ML – Productivity & Burnout Prediction
=======================================
Trains a Random Forest model on historical data to predict:
  - Productivity score (0-100)
  - Burnout risk (0-1 probability)

Falls back to a rule-based heuristic when training data is insufficient.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler

FEATURE_COLS = ["screen_time_hours", "study_hours", "sleep_hours", "exercise_minutes"]

# Heuristic weights for rule-based fallback
_PROD_WEIGHTS = {
    "study_hours": 15.0,
    "sleep_hours": 10.0,
    "exercise_minutes": 0.1,
    "screen_time_hours": -5.0,
}
_BASE_PRODUCTIVITY = 40.0
_DEFAULT_AVERAGES = {
    "screen_time_hours": 6.0,
    "study_hours": 4.0,
    "sleep_hours": 7.0,
    "exercise_minutes": 30.0,
}


def _heuristic_productivity(deltas: dict[str, float]) -> float:
    score = _BASE_PRODUCTIVITY
    for col, weight in _PROD_WEIGHTS.items():
        score += weight * deltas.get(col, 0)
    return float(np.clip(score, 0, 100))


def _heuristic_burnout(deltas: dict[str, float]) -> float:
    risk = 0.4
    risk -= 0.05 * deltas.get("sleep_hours", 0)
    risk += 0.03 * deltas.get("screen_time_hours", 0)
    risk -= 0.02 * deltas.get("study_hours", 0)
    risk -= 0.001 * deltas.get("exercise_minutes", 0)
    return float(np.clip(risk, 0, 1))


def predict_from_deltas(
    sleep_delta: float = 0.0,
    screen_delta: float = 0.0,
    study_delta: float = 0.0,
    exercise_delta: float = 0.0,
) -> tuple[float, float]:
    """
    Predict productivity score and burnout risk given behavioural deltas.

    Attempts to use a trained model if historical data exists; otherwise
    applies the rule-based heuristic.
    """
    from backend.services import data_service

    df = data_service.get_dataframe()
    deltas = {
        "screen_time_hours": screen_delta,
        "study_hours": study_delta,
        "sleep_hours": sleep_delta,
        "exercise_minutes": exercise_delta,
    }

    if df.empty or len(df) < 10:
        return _heuristic_productivity(deltas), _heuristic_burnout(deltas)

    # --- build synthetic target variables from existing data ---
    features = df[FEATURE_COLS].fillna(0)
    scaler = MinMaxScaler()
    norm = pd.DataFrame(scaler.fit_transform(features), columns=FEATURE_COLS)

    productivity_target = (
        norm["study_hours"] * 40
        + norm["sleep_hours"] * 30
        + norm["exercise_minutes"] * 15
        - norm["screen_time_hours"] * 20
        + 20
    ).clip(0, 100)

    burnout_target = (
        norm["screen_time_hours"] * 0.4
        - norm["sleep_hours"] * 0.3
        - norm["exercise_minutes"] * 0.2
        + 0.3
    ).clip(0, 1)

    reg = RandomForestRegressor(n_estimators=50, random_state=42)
    reg.fit(features, productivity_target)

    reg_burnout = RandomForestRegressor(n_estimators=50, random_state=42)
    reg_burnout.fit(features, burnout_target)

    # Build a simulated "next day" input
    mean_vals = features.mean()
    sim_input = np.array([[
        mean_vals["screen_time_hours"] + screen_delta,
        mean_vals["study_hours"] + study_delta,
        mean_vals["sleep_hours"] + sleep_delta,
        mean_vals["exercise_minutes"] + exercise_delta,
    ]])
    sim_input = np.clip(sim_input, 0, None)

    prod = float(reg.predict(sim_input)[0])
    burn = float(reg_burnout.predict(sim_input)[0])
    return np.clip(prod, 0, 100), np.clip(burn, 0, 1)
