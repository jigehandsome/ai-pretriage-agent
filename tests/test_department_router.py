"""
Tests — Department Router
=========================
Verify department routing logic.
"""

import pytest
from agents.department_router import DepartmentRouter


@pytest.fixture
def router():
    return DepartmentRouter()


def test_cardiology_match(router):
    result = router.run({"chief_complaint": "chest pain and palpitation"})
    assert result["department"] == "Cardiology"


def test_pulmonology_match(router):
    result = router.run({"chief_complaint": "severe cough and difficulty breathing"})
    assert result["department"] == "Pulmonology"


def test_neurology_match(router):
    result = router.run({"chief_complaint": "sudden dizziness and numbness"})
    assert result["department"] == "Neurology"


def test_no_match_returns_general(router):
    result = router.run({"chief_complaint": "feeling tired lately"})
    assert result["department"] == "General Medicine"


def test_alternatives_populated(router):
    result = router.run({"chief_complaint": "chest pain with breathing difficulty"})
    assert result["department"] == "Cardiology"
    assert "Pulmonology" in result["alternatives"]
