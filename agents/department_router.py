"""
MediTriage — Department Router
===============================
Routes patients to the appropriate medical department based on
symptom analysis and clinical specialty matching.
"""

from agents.base_agent import BaseAgent

# ─── Department Matching Rules ────────────────────────────────────────────────

DEPARTMENT_MAP = [
    {
        "name": "Cardiology",
        "keywords": ["chest pain", "heart", "palpitation", "cardiac", "arrhythmia"],
    },
    {
        "name": "Pulmonology",
        "keywords": ["breathing", "cough", "lung", "asthma", "pneumonia", "wheeze"],
    },
    {
        "name": "Neurology",
        "keywords": ["head", "stroke", "seizure", "dizziness", "numbness", "vision"],
    },
    {
        "name": "Orthopedics",
        "keywords": ["bone", "fracture", "sprain", "back pain", "joint", "spine"],
    },
    {
        "name": "Gastroenterology",
        "keywords": ["stomach", "abdominal", "vomit", "diarrhea", "nausea", "liver"],
    },
    {
        "name": "Emergency Surgery",
        "keywords": ["wound", "laceration", "trauma", "burn", "accident"],
    },
    {
        "name": "Pediatrics",
        "keywords": ["child", "baby", "infant", "pediatric", "newborn"],
    },
    {
        "name": "OB/GYN",
        "keywords": ["pregnant", "pregnancy", "labor", "obstetric", "vaginal"],
    },
    {
        "name": "ENT (Otolaryngology)",
        "keywords": ["ear", "hearing", "throat", "nose", "sinus"],
    },
    {
        "name": "Ophthalmology",
        "keywords": ["eye", "vision", "blind", "glaucoma"],
    },
]


class DepartmentRouter(BaseAgent):
    """Matches patients to the most appropriate medical department."""

    def __init__(self):
        super().__init__(name="DepartmentRouter")

    def run(self, input_data: dict) -> dict:
        """
        Route patient to department based on symptoms.

        Args:
            input_data: Must contain "chief_complaint" or "symptom_keywords"

        Returns:
            {
                "department": "Cardiology",
                "alternatives": ["Pulmonology"],
                "confidence": 0.9,
                "reasoning": "Chest pain symptoms match cardiology protocol"
            }
        """
        text = input_data.get("chief_complaint", "").lower()
        keywords = input_data.get("symptom_keywords", [])

        search_text = text + " " + " ".join(keywords)

        matches = []
        for dept in DEPARTMENT_MAP:
            score = sum(1 for kw in dept["keywords"] if kw in search_text)
            if score > 0:
                matches.append((dept["name"], score))

        # Sort by match score, highest first
        matches.sort(key=lambda x: x[1], reverse=True)

        if not matches:
            return {
                "department": "General Medicine",
                "alternatives": [],
                "confidence": 0.5,
                "reasoning": "No specific department match found. Routing to General Medicine.",
            }

        primary = matches[0][0]
        alternatives = [m[0] for m in matches[1:3]]
        confidence = min(0.95, 0.6 + matches[0][1] * 0.1)

        return {
            "department": primary,
            "alternatives": alternatives,
            "confidence": round(confidence, 2),
            "reasoning": f"Symptoms match {primary} specialty with {matches[0][1]} keyword hits.",
        }
