<div align="center">

# MediTriage

**AI-Powered Clinical Pre-Triage Agent**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Made with Claude](https://img.shields.io/badge/Built%20with-Claude%20Code-d4a574.svg)](https://claude.ai/code)
[![Powered by Xiaomi MiMo](https://img.shields.io/badge/Powered%20by-Xiaomi%20MiMo-orange.svg)](https://mi.com)
[![Cursor IDE](https://img.shields.io/badge/IDE-Cursor-ff6b6b.svg)](https://cursor.sh)

An intelligent clinical pre-triage agent that leverages structured medical reasoning and large language models to perform patient symptom assessment, urgency classification, and clinical decision support.

[Features](#-features) · [Architecture](#-architecture) · [Quick Start](#-quick-start) · [Agent Workflow](#-agent-workflow) · [Roadmap](#-roadmap) · [Contributing](#-contributing)

</div>

---

## Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Agent Workflow](#-agent-workflow)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Demo](#-demo)
- [Roadmap](#-roadmap)
- [Tech Stack](#-tech-stack)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## Features

- **Structured Medical Reasoning** — Applies chain-of-thought clinical logic to analyze symptoms, not just pattern match
- **Intelligent Symptom Extraction** — Parses natural language patient descriptions into structured clinical data
- **Triage Urgency Classification** — Assigns ESI (Emergency Severity Index) levels with confidence scoring
- **Differential Diagnosis Suggestions** — Generates ranked differential diagnoses with supporting evidence
- **Clinical Safety Guardrails** — Rule-based safety layer to prevent hallucination-driven misclassification
- **Conversation Memory** — Maintains multi-turn patient context for progressive assessment
- **Explainable Decisions** — Every triage decision includes a transparent reasoning chain

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                           │
│                   (Web / CLI / API Gateway)                     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Triage Orchestrator                         │
│              (LangGraph State Machine / Agent Core)             │
│                                                                 │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌─────────────┐  │
│  │ Symptom   │→ │ Clinical  │→ │ Diagnosis │→ │  Triage     │  │
│  │ Extractor │  │ Reasoner  │  │ Generator │  │  Classifier │  │
│  └───────────┘  └───────────┘  └───────────┘  └─────────────┘  │
│       │              │              │               │           │
│       ▼              ▼              ▼               ▼           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              LLM Backend (Claude / MiMo)                │    │
│  └─────────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
               ┌───────────┼───────────┐
               ▼           ▼           ▼
         ┌──────────┐ ┌─────────┐ ┌──────────┐
         │ Medical  │ │ Safety  │ │ Patient  │
         │ Knowledge│ │ Guard-  │ │ History  │
         │ Base     │ │ rails   │ │ Store    │
         └──────────┘ └─────────┘ └──────────┘
```

| Component | Responsibility |
|---|---|
| **Triage Orchestrator** | Coordinates the multi-step agent workflow, manages state transitions |
| **Symptom Extractor** | Parses free-text into structured clinical observations (SNOMED/ICD mapped) |
| **Clinical Reasoner** | Applies structured medical reasoning chains to evaluate symptom patterns |
| **Diagnosis Generator** | Produces ranked differential diagnoses with evidence linkage |
| **Triage Classifier** | Maps clinical assessment to ESI level (1-5) with confidence metrics |
| **Safety Guardrails** | Rule-based override layer — catches critical patterns before LLM output |
| **Medical Knowledge Base** | Clinical guidelines, drug interactions, red-flag symptom databases |

---

## Agent Workflow

Meditriage follows a **multi-step agent pipeline** with structured clinical reasoning:

```
Patient Input
     │
     ▼
┌─────────────┐     Extract symptoms, duration,
│  1. Intake   │──── severity, demographics
└──────┬──────┘
       │
       ▼
┌─────────────┐     Validate completeness,
│  2. Verify  │──── ask follow-up questions
└──────┬──────┘
       │
       ▼
┌─────────────┐     Apply clinical reasoning
│  3. Reason  │──── chains (chain-of-thought
└──────┬──────┘     medical logic)
       │
       ▼
┌─────────────┐     Rule-based safety check
│  4. Guard   │──── red-flag symptom detection
└──────┬──────┘
       │
       ▼
┌─────────────┐     ESI 1-5 classification
│  5. Classify│──── with confidence score
└──────┬──────┘
       │
       ▼
┌─────────────┐     Human-readable report
│  6. Report  │──── with reasoning chain
└─────────────┘
```

Each step is **independently auditable** and produces structured intermediate outputs, making the system transparent and debuggable.

---

## Quick Start

### Prerequisites

- Python 3.10+
- An LLM API key (Claude API / Xiaomi MiMo API)

### Installation

```bash
git clone https://github.com/your-username/meditriage.git
cd meditriage
pip install -e .
```

### Configuration

```bash
cp .env.example .env
# Edit .env with your API keys
```

### Run

```bash
meditriage --mode interactive
```

---

## Usage

### Interactive Mode

```bash
meditriage chat
```

### API Mode

```python
from meditriage import TriageAgent

agent = TriageAgent()
result = agent.assess(
    symptoms="Sharp chest pain radiating to left arm, started 30 minutes ago. "
             "Shortness of breath. Patient is 58M with history of hypertension."
)

print(result.esi_level)       # 2 (Emergent)
print(result.differential)    # ["Acute MI", "Unstable Angina", "Aortic Dissection"]
print(result.reasoning_chain) # Full clinical reasoning trace
```

### Batch Mode

```bash
meditriage batch --input patients.csv --output results.json
```

---

## Demo

> **Coming Soon** — Interactive web demo and video walkthrough.
>
> - Live demo link: `[TBD]`
> - Video walkthrough: `[TBD]`

---

## Tech Stack

| Layer | Technology |
|---|---|
| **AI Engine** | Claude API, Xiaomi MiMo |
| **Agent Framework** | LangGraph, structured output parsing |
| **Medical Standards** | SNOMED CT, ICD-11, ESI Protocol |
| **Backend** | Python, FastAPI |
| **Development** | Claude Code, Cursor IDE |
| **Knowledge Base** | Clinical guidelines DB, drug interaction APIs |

---

## Roadmap

### Phase 1 — Core Agent (Current)

- [x] Structured clinical reasoning pipeline
- [x] Symptom extraction from natural language
- [x] ESI triage classification
- [x] Safety guardrails layer
- [x] Explainable reasoning chains

### Phase 2 — Enhanced Intelligence

- [ ] Multi-turn patient conversation support
- [ ] Integration with FHIR/HL7 medical data standards
- [ ] Image-based symptom input (wound/rash assessment)
- [ ] Confidence calibration and uncertainty quantification
- [ ] Automated clinical guideline compliance checking

### Phase 3 — Multi-Agent System

- [ ] Specialized sub-agents (cardiology, neurology, pediatrics)
- [ ] Multi-agent consensus for complex cases
- [ ] Agent-to-agent consultation workflow
- [ ] Real-time escalation to human clinicians
- [ ] EHR system integration plugins

### Phase 4 — Production & Scale

- [ ] HIPAA-compliant deployment architecture
- [ ] Multi-language support
- [ ] Hospital dashboard and analytics
- [ ] Clinical validation study framework
- [ ] Regulatory compliance documentation

---

## Contributing

Contributions are welcome! Whether it's bug reports, feature proposals, or code contributions.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and submission guidelines.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- **Claude Code** — Primary development assistant for code generation and architecture design
- **Cursor IDE** — AI-powered development environment
- **Xiaomi MiMo** — LLM integration and model support
- Inspired by clinical triage protocols (ESI, Manchester Triage System)

---

<div align="center">

**If this project helps you, please give it a Star**

</div>
