"""
Tests — Triage Agent
====================
Basic tests to verify the triage agent produces expected outputs.
"""

import pytest
from agents.triage_agent import TriageAgent


@pytest.fixture
def agent():
    return TriageAgent()


def test_extract_symptoms(agent):
    result = agent.run({"symptoms": "chest pain for 2 hours", "age": "55", "gender": "M"})
    assert "chief_complaint" in result
    assert "chest pain" in result["chief_complaint"]


def test_default_values(agent):
    result = agent.run({"symptoms": "headache"})
    assert result["age"] == "Unknown"
    assert result["gender"] == "Unknown"


def test_empty_symptoms(agent):
    result = agent.run({})
    assert result["chief_complaint"] == ""
