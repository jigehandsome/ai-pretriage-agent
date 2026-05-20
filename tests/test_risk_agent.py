"""
Tests — Risk Agent
==================
Verify risk classification logic produces correct ESI levels.
"""

import pytest
from agents.risk_agent import RiskAgent


@pytest.fixture
def agent():
    return RiskAgent()


def test_critical_cardiac_arrest(agent):
    result = agent.run({"chief_complaint": "patient in cardiac arrest, no pulse"})
    assert result["esi_level"] == 1
    assert result["risk_level"] == "Critical"
    assert len(result["red_flags"]) > 0


def test_emergent_stroke(agent):
    result = agent.run({"chief_complaint": "sudden slurred speech and face drooping"})
    assert result["esi_level"] == 2
    assert result["risk_level"] == "Emergent"


def test_urgent_multiple_symptoms(agent):
    result = agent.run({"chief_complaint": "fever with moderate pain"})
    assert result["esi_level"] == 3
    assert result["risk_level"] == "Urgent"


def test_less_urgent_single_symptom(agent):
    result = agent.run({"chief_complaint": "mild fever"})
    assert result["esi_level"] == 4
    assert result["risk_level"] == "Less Urgent"


def test_low_risk_no_symptoms(agent):
    result = agent.run({"chief_complaint": "routine checkup"})
    assert result["esi_level"] == 5
    assert result["risk_level"] == "Low"


def test_reasoning_included(agent):
    result = agent.run({"chief_complaint": "chest pain"})
    assert len(result["reasoning"]) > 0
