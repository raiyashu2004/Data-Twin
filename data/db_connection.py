"""
Database connection scaffolding (PostgreSQL / Supabase)
========================================================
This module provides a SQLAlchemy engine and session factory.
Configure the DATABASE_URL environment variable to point at your
PostgreSQL / Supabase instance, e.g.:

    DATABASE_URL=postgresql://user:password@host:5432/datatwin

When DATABASE_URL is not set the application falls back to the
in-memory store in backend/services/data_service.py.
"""

import os
from sqlalchemy import create_engine, Column, Integer, Float, String, Date
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "")


class Base(DeclarativeBase):
    pass


class DailyEntryORM(Base):
    """SQLAlchemy ORM model for daily behavioural entries."""

    __tablename__ = "daily_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    entry_date = Column(Date, nullable=False)
    screen_time_hours = Column(Float, nullable=False)
    study_hours = Column(Float, nullable=False)
    sleep_hours = Column(Float, nullable=False)
    exercise_minutes = Column(Float, default=0.0)
    expenses = Column(Float, nullable=True)
    notes = Column(String, nullable=True)


def get_engine():
    """Return a SQLAlchemy engine.  Raises if DATABASE_URL is not configured."""
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set. "
            "Set it to a valid PostgreSQL connection string to use the database."
        )
    return create_engine(DATABASE_URL, pool_pre_ping=True)


def get_session_factory():
    """Return a configured session factory bound to the database engine."""
    engine = get_engine()
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)
