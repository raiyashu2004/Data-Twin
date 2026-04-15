"""AI Insights API route."""

from fastapi import APIRouter, HTTPException

from backend.models.schemas import InsightRequest, InsightResponse
from backend.ai import insight_engine

router = APIRouter()


@router.post("/ask", response_model=InsightResponse)
def ask_insight(request: InsightRequest):
    """Send a natural-language question and receive an AI-generated answer."""
    try:
        answer = insight_engine.generate_insight(request.question)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return InsightResponse(answer=answer)


@router.get("/summary")
def get_summary():
    """Return a structured weekly behavioural summary."""
    from backend.services import analytics_service
    return analytics_service.weekly_summary()
