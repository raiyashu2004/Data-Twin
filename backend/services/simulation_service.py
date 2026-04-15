"""Simulation service – applies deltas and predicts outcomes."""

from backend.models.schemas import SimulationRequest, SimulationResult
from backend.ml import prediction


def run(request: SimulationRequest) -> SimulationResult:
    """
    Compute predicted productivity and burnout risk given behavioural deltas.

    Uses the ML prediction module under the hood.  When no historical data is
    present the module falls back to a simple rule-based heuristic.
    """
    predicted_productivity, predicted_burnout = prediction.predict_from_deltas(
        sleep_delta=request.sleep_hours_delta,
        screen_delta=request.screen_time_delta,
        study_delta=request.study_hours_delta,
        exercise_delta=request.exercise_minutes_delta,
    )

    recommendations = _build_recommendations(request)

    return SimulationResult(
        predicted_productivity_score=round(predicted_productivity, 2),
        predicted_burnout_risk=round(predicted_burnout, 4),
        recommendations=recommendations,
    )


def _build_recommendations(request: SimulationRequest) -> list[str]:
    recs = []
    if request.sleep_hours_delta > 0:
        recs.append("Increasing sleep should improve cognitive performance and mood.")
    elif request.sleep_hours_delta < 0:
        recs.append("Reducing sleep may negatively impact focus and productivity.")
    if request.screen_time_delta < 0:
        recs.append("Less screen time typically correlates with lower stress levels.")
    if request.study_hours_delta > 0:
        recs.append("More structured study time can boost skill acquisition.")
    if request.exercise_minutes_delta > 0:
        recs.append("Regular exercise is one of the strongest predictors of wellbeing.")
    if not recs:
        recs.append("No significant changes detected – keep your current routine!")
    return recs
