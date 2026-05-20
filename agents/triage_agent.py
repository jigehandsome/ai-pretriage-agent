"""
MediTriage — Triage Agent
=========================
The main orchestrator agent. Takes patient input, coordinates
symptom extraction, risk assessment, and department routing.
"""

from agents.base_agent import BaseAgent


class TriageAgent(BaseAgent):
    """
    Main triage agent that orchestrates the full assessment pipeline.

    Flow:
        1. Parse patient symptoms
        2. Extract structured clinical data
        3. Delegate to RiskAgent for urgency scoring
        4. Delegate to DepartmentRouter for specialist matching
        5. Compile final triage report
    """

    def __init__(self):
        super().__init__(name="TriageAgent")

    def run(self, input_data: dict) -> dict:
        """
        Run full triage assessment.

        Args:
            input_data: {
                "symptoms": "patient description...",
                "age": "45",
                "gender": "M"
            }

        Returns:
            Complete triage assessment dict
        """
        symptoms = input_data.get("symptoms", "")

        # Step 1: Extract structured symptoms (placeholder)
        structured = self._extract_symptoms(symptoms)

        # Step 2: Build clinical context
        context = {
            **structured,
            "age": input_data.get("age", "Unknown"),
            "gender": input_data.get("gender", "Unknown"),
        }

        return context

    def _extract_symptoms(self, raw_text: str) -> dict:
        """
        Parse free-text symptoms into structured data.
        In production, this uses the LLM with a structured prompt.
        """
        # Placeholder — production version calls LLM with prompts/symptom_extraction.txt
        return {
            "chief_complaint": raw_text,
            "symptom_keywords": raw_text.lower().split(),
            "duration": "unknown",
            "severity": "unknown",
        }
