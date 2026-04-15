"""Data service – in-memory store (replace with DB in production)."""

from datetime import date
from typing import Optional
import pandas as pd

from backend.models.schemas import DailyEntry, DailyEntryResponse

_store: list[dict] = []
_next_id: int = 1


def save_entry(entry: DailyEntry) -> DailyEntryResponse:
    global _next_id
    record = entry.model_dump()
    record["id"] = _next_id
    _store.append(record)
    _next_id += 1
    return DailyEntryResponse(**record)


def get_all_entries() -> list[DailyEntryResponse]:
    return [DailyEntryResponse(**r) for r in _store]


def save_from_dataframe(df: pd.DataFrame) -> list[DailyEntryResponse]:
    """Bulk-import rows from a DataFrame; unknown columns are ignored."""
    required = {"entry_date", "screen_time_hours", "study_hours", "sleep_hours"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")
    results = []
    for _, row in df.iterrows():
        entry = DailyEntry(
            entry_date=row["entry_date"],
            screen_time_hours=float(row["screen_time_hours"]),
            study_hours=float(row["study_hours"]),
            sleep_hours=float(row["sleep_hours"]),
            exercise_minutes=float(row.get("exercise_minutes", 0)),
            expenses=float(row["expenses"]) if "expenses" in row and pd.notna(row["expenses"]) else None,
            notes=str(row["notes"]) if "notes" in row and pd.notna(row["notes"]) else None,
        )
        results.append(save_entry(entry))
    return results


def get_dataframe() -> pd.DataFrame:
    """Return the current in-memory store as a DataFrame."""
    if not _store:
        return pd.DataFrame()
    return pd.DataFrame(_store)
