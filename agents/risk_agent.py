"""
MediTriage — Risk Assessment Agent
===================================
Specialized agent that evaluates clinical urgency and assigns ESI levels.
Uses both rule-based checks (for safety) and LLM reasoning (for nuance).
"""

from agents.base_agent import BaseAgent

# ─── Red Flag Keywords (safety-critical, always rule-checked) ────────────────

RED_FLAGS = {
    "cardiac_arrest": ["cardiac arrest", "no pulse", "unresponsive"],
    "respiratory_failure": ["cannot breathe", "respiratory failure", "apnea"],
    "stroke": ["slurred speech", "face drooping", "arm weakness"],
    "severe_bleeding": ["arterial bleeding", "heavy blood loss"],
    "anaphylaxis": ["throat swelling", "anaphylactic shock"],
    "loss_of_consciousness": ["fainted", "unconscious", "unresponsive"],
}

MEDIUM_RISK = [
    "fever", "vomiting", "dehydration", "moderate pain",
    "fracture", "deep laceration", "asthma attack", "allergic reaction",
]


class RiskAgent(BaseAgent):
    """Evaluates patient risk level using rule-based + LLM reasoning."""

    def __init__(self):
        super().__init__(name="RiskAgent")

    def run(self, input_data: dict) -> dict:
        """
        Assess risk level from structured patient data.

        Returns:
            {
                "esi_level": 1-5,
                "risk_level": "Critical" | "Emergent" | "Urgent" | "Less Urgent" | "Low",
                "red_flags": [...],
                "confidence": 0.0-1.0,
                "reasoning": "..."
            }
        """
        symptoms = input_data.get("chief_complaint", "").lower()

        # Phase 1: Rule-based red flag detection (always runs, no LLM)
        red_flags = self._check_red_flags(symptoms)

        # Phase 2: Determine ESI level
        if red_flags:
            esi, risk = self._critical_or_emergent(red_flags)
        else:
            esi, risk = self._assess_urgency(symptoms)

        # Phase 3: Generate reasoning (LLM in production)
        reasoning = self._generate_reasoning(symptoms, esi, red_flags)

        return {
            "esi_level": esi,
            "risk_level": risk,
            "red_flags": red_flags,
            "confidence": 0.85 if red_flags else 0.70,
            "reasoning": reasoning,
        }

    def _check_red_flags(self, text: str) -> list[str]:
        """Rule-based safety check — catches critical patterns."""
        found = []
        for category, keywords in RED_FLAGS.items():
            if any(kw in text for kw in keywords):
                found.append(category)
        return found

    def _critical_or_emergent(self, red_flags: list[str]) -> tuple[int, str]:
        """Map red flags to ESI 1 or 2."""
        critical_flags = {"cardiac_arrest", "respiratory_failure", "loss_of_consciousness"}
        if red_flags & critical_flags if isinstance(red_flags, set) else any(f in critical_flags for f in red_flags):
            return 1, "Critical"
        return 2, "Emergent"

    def _assess_urgency(self, text: str) -> tuple[int, str]:
        """Assess non-critical patients."""
        medium_hits = sum(1 for kw in MEDIUM_RISK if kw in text)
        if medium_hits >= 2:
            return 3, "Urgent"
        elif medium_hits == 1:
            return 4, "Less Urgent"
        return 5, "Low"

    def _generate_reasoning(self, symptoms: str, esi: int, red_flags: list) -> str:
        """Generate human-readable reasoning. Production version uses LLM."""
        if red_flags:
            return f"Red flags detected: {', '.join(red_flags)}. ESI-{esi} assigned for immediate evaluation."
        return f"Based on symptom analysis, ESI-{esi} assigned. No red flags detected."
