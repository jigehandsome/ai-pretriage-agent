"""
MediTriage — Configuration
==========================
All settings in one place. Reads from environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()


# ─── LLM Settings ────────────────────────────────────────────────────────────

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")  # "anthropic" or "mock"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")


# ─── App Settings ─────────────────────────────────────────────────────────────

APP_NAME = "MediTriage"
APP_VERSION = "0.1.0"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"


# ─── Triage Settings ─────────────────────────────────────────────────────────

MAX_CONVERSATION_TURNS = 10
CONFIDENCE_THRESHOLD = 0.7
ENABLE_SAFETY_GUARDRAILS = True
