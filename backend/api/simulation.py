"""Simulation API route – 'what-if' scenario engine."""

from fastapi import APIRouter, HTTPException

from backend.models.schemas import SimulationRequest, SimulationResult
from backend.services import simulation_service

router = APIRouter()


@router.post("/run", response_model=SimulationResult)
def run_simulation(request: SimulationRequest):
    """Run a what-if simulation and return predicted outcomes."""
    try:
        result = simulation_service.run(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return result
