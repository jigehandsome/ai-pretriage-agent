"""
MediTriage — Patient Model
===========================
Data schema for patient information.
"""

from pydantic import BaseModel


class Patient(BaseModel):
    """Patient demographics and basic info."""

    age: str = "Unknown"
    gender: str = "Unknown"
    chief_complaint: str = ""
    duration: str = "Unknown"
    medical_history: list[str] = []
    medications: list[str] = []
    allergies: list[str] = []
