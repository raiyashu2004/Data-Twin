"""Pydantic schemas for the Personal Data Twin."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class DailyEntry(BaseModel):
    """A single day's behavioural data record."""

    entry_date: date = Field(..., description="Date of the entry (YYYY-MM-DD)")
    screen_time_hours: float = Field(..., ge=0, le=24, description="Total screen time in hours")
    study_hours: float = Field(..., ge=0, le=24, description="Hours spent studying/working")
    sleep_hours: float = Field(..., ge=0, le=24, description="Hours of sleep")
    exercise_minutes: float = Field(0.0, ge=0, description="Minutes of physical exercise")
    expenses: Optional[float] = Field(None, ge=0, description="Daily expenses in local currency")
    notes: Optional[str] = Field(None, description="Free-text notes for the day")


class DailyEntryResponse(DailyEntry):
    """DailyEntry with a server-assigned id."""

    id: int


class SimulationRequest(BaseModel):
    """Parameters for a 'what-if' simulation scenario."""

    sleep_hours_delta: float = Field(0.0, description="Change in sleep hours (+/-)")
    screen_time_delta: float = Field(0.0, description="Change in screen time (+/-)")
    study_hours_delta: float = Field(0.0, description="Change in study hours (+/-)")
    exercise_minutes_delta: float = Field(0.0, description="Change in exercise minutes (+/-)")


class SimulationResult(BaseModel):
    """Predicted outcomes after applying a simulation scenario."""

    predicted_productivity_score: float = Field(..., ge=0, le=100)
    predicted_burnout_risk: float = Field(..., ge=0, le=1)
    recommendations: list[str]


class InsightRequest(BaseModel):
    """Free-text question for the AI insight engine."""

    question: str = Field(..., min_length=3, description="Natural-language question about your data")


class InsightResponse(BaseModel):
    """AI-generated insight."""

    answer: str
    source: str = "llm"
