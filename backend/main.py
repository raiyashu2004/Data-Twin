"""Personal Data Twin – FastAPI entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import data, insights, simulation

app = FastAPI(
    title="Personal Data Twin API",
    description="AI-powered personal behaviour analytics and simulation engine.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router, prefix="/api/data", tags=["Data"])
app.include_router(insights.router, prefix="/api/insights", tags=["Insights"])
app.include_router(simulation.router, prefix="/api/simulation", tags=["Simulation"])


@app.get("/", tags=["Health"])
def health_check():
    """Simple liveness probe."""
    return {"status": "ok", "message": "Personal Data Twin API is running."}
