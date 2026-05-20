"""
MediTriage — Triage Result Model
=================================
Data schema for the final triage assessment output.
"""

from pydantic import BaseModel
from datetime import datetime


class TriageResult(BaseModel):
    """Complete triage assessment result."""

    case_id: str
    timestamp: str = datetime.now().isoformat()

    # Risk assessment
    risk_level: str  # Critical, Emergent, Urgent, Less Urgent, Low
    esi_level: int   # 1-5
    confidence: float = 0.0

    # Routing
    department: str = "General Medicine"
    alternative_departments: list[str] = []

    # Clinical reasoning
    red_flags: list[str] = []
    differential_diagnosis: list[str] = []
    reasoning_chain: str = ""

    # Metadata
    model_used: str = ""
    processing_time_ms: int = 0
