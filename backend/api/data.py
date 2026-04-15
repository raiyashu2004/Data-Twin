"""Data collection API route."""

from fastapi import APIRouter, HTTPException, UploadFile, File
import pandas as pd
import io

from backend.models.schemas import DailyEntry, DailyEntryResponse
from backend.services import data_service

router = APIRouter()


@router.post("/entry", response_model=DailyEntryResponse, status_code=201)
def create_entry(entry: DailyEntry):
    """Manually submit a single day's behavioural data."""
    return data_service.save_entry(entry)


@router.get("/entries", response_model=list[DailyEntryResponse])
def list_entries():
    """Return all stored entries."""
    return data_service.get_all_entries()


@router.post("/upload-csv")
def upload_csv(file: UploadFile = File(...)):
    """Upload a CSV file containing multiple daily entries."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")
    content = file.file.read()
    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Could not parse CSV: {exc}") from exc
    records = data_service.save_from_dataframe(df)
    return {"imported": len(records), "message": "Data imported successfully."}
