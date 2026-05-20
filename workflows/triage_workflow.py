"""
MediTriage — Triage Workflow
============================
Orchestrates the full triage pipeline:
    Patient Input → TriageAgent → RiskAgent → DepartmentRouter → Report

This is the "brain" that coordinates all agents.
"""

from datetime import datetime

from agents.triage_agent import TriageAgent
from agents.risk_agent import RiskAgent
from agents.department_router import DepartmentRouter


class TriageWorkflow:
    """
    Multi-agent workflow for clinical pre-triage.

    Pipeline:
        1. TriageAgent    — parse symptoms, extract structured data
        2. RiskAgent      — assess urgency, assign ESI level
        3. DepartmentRouter — match to medical department
        4. Compile        — assemble final report
    """

    def __init__(self):
        self.triage_agent = TriageAgent()
        self.risk_agent = RiskAgent()
        self.department_router = DepartmentRouter()

    def run(self, symptoms: str, patient_info: dict = None) -> dict:
        """
        Execute the full triage pipeline.

        Args:
            symptoms: Free-text patient symptom description
            patient_info: {"age": "...", "gender": "..."}

        Returns:
            Complete triage report dict
        """
        patient_info = patient_info or {}
        case_id = f"TRI-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Step 1: Extract structured symptoms
        extracted = self.triage_agent.run({
            "symptoms": symptoms,
            "age": patient_info.get("age", "Unknown"),
            "gender": patient_info.get("gender", "Unknown"),
        })

        # Step 2: Assess risk level
        risk_result = self.risk_agent.run(extracted)

        # Step 3: Route to department
        dept_result = self.department_router.run(extracted)

        # Step 4: Compile report
        return {
            "case_id": case_id,
            "timestamp": datetime.now().isoformat(),
            "patient": patient_info,
            "symptoms": {
                "raw": symptoms,
                "extracted": extracted,
            },
            "assessment": {
                "risk_level": risk_result["risk_level"],
                "esi_level": risk_result["esi_level"],
                "red_flags": risk_result["red_flags"],
                "confidence": risk_result["confidence"],
                "reasoning": risk_result["reasoning"],
            },
            "routing": {
                "department": dept_result["department"],
                "alternatives": dept_result["alternatives"],
                "confidence": dept_result["confidence"],
            },
            "differential": ["Requires LLM integration for differential diagnosis"],
        }
