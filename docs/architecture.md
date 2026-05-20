# MediTriage — Architecture

## System Overview

```
┌─────────────────────────────────────────────────┐
│                  User Interface                  │
│            (Web / CLI / API Gateway)             │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│              Triage Workflow                     │
│        (LangGraph State Machine)                 │
│                                                  │
│  ┌────────────┐ ┌──────────┐ ┌───────────────┐  │
│  │ TriageAgent│→│RiskAgent │→│Dept Router    │  │
│  └────────────┘ └──────────┘ └───────────────┘  │
└────────────────────┬────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌─────────┐ ┌─────────┐ ┌──────────┐
   │ LLM API │ │ Safety  │ │ Knowledge│
   │(Claude/ │ │Guardrails│ │   Base   │
   │  MiMo)  │ │         │ │          │
   └─────────┘ └─────────┘ └──────────┘
```

## Directory Structure

```
meditriage/
├── agents/              # AI agent implementations
│   ├── base_agent.py    # Abstract base class
│   ├── triage_agent.py  # Main orchestrator
│   ├── risk_agent.py    # Risk classification
│   └── department_router.py  # Specialty matching
├── workflows/           # Agent orchestration
│   └── triage_workflow.py
├── prompts/             # LLM prompt templates
├── models/              # Data schemas (Pydantic)
├── backend/             # API server (FastAPI)
├── tests/               # Pytest test suite
├── docs/                # Documentation
├── config.py            # Settings & env vars
├── main.py              # CLI entry point
└── demo.py              # Standalone demo
```

## Agent Pipeline

1. **TriageAgent** — Parses patient input, extracts structured symptoms
2. **RiskAgent** — Rule-based safety check + LLM risk classification (ESI 1-5)
3. **DepartmentRouter** — Matches symptoms to medical specialties
4. **Report Compiler** — Assembles final JSON assessment

## Safety Architecture

The system uses a **dual-layer safety model**:

- **Layer 1 (Rule-based)**: Keyword matching for red-flag symptoms. Runs before any LLM call. Zero hallucination risk.
- **Layer 2 (LLM reasoning)**: Structured chain-of-thought for nuanced cases. Outputs are validated against Layer 1.
