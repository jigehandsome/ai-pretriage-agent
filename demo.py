#!/usr/bin/env python3
"""
MediTriage — AI Clinical Pre-Triage Demo
=========================================
A rule-based interactive demo that simulates AI-powered clinical triage.
No API key needed. Run it and follow the prompts.
"""

import json
import sys
import time
from datetime import datetime


# ─── Symptom Keywords & Rules ────────────────────────────────────────────────

RED_FLAG_KEYWORDS = {
    "chest pain": ["crushing chest pain", "pressure in chest"],
    "breathing": ["cannot breathe", "severe shortness of breath"],
    "stroke": ["slurred speech", "face drooping", "one side numb"],
    "unconscious": ["fainted", "unresponsive", "loss of consciousness"],
    "severe bleeding": ["heavy bleeding", "blood loss", "arterial bleeding"],
}

MEDIUM_RISK_KEYWORDS = [
    "fever", "high temperature", "vomiting", "dehydration",
    "moderate pain", "broken bone", "fracture", "deep cut",
    "allergic reaction", "asthma", "dizziness", "confusion",
]

DEPARTMENT_RULES = [
    (["chest pain", "heart", "palpitation", "cardiac"], "Cardiology"),
    (["breathing", "cough", "lung", "asthma", "pneumonia"], "Pulmonology"),
    (["head", "stroke", "seizure", "dizziness", "numb"], "Neurology"),
    (["bone", "fracture", "sprain", "back pain", "joint"], "Orthopedics"),
    (["skin", "rash", "burn", "wound", "cut"], "Dermatology / Emergency Surgery"),
    (["child", "baby", "infant", "pediatric"], "Pediatrics"),
    (["pregnant", "pregnancy", "labor", "obstetric"], "OB/GYN"),
    (["stomach", "abdominal", "vomit", "diarrhea", "nausea"], "Gastroenterology"),
    (["eye", "vision", "blind"], "Ophthalmology"),
    (["ear", "hearing", "throat", "nose"], "ENT (Otolaryngology)"),
]


# ─── Core Triage Logic ───────────────────────────────────────────────────────

def analyze_symptoms(text: str) -> dict:
    """Analyze patient symptoms and return a triage result."""
    text_lower = text.lower()

    # 1. Check red flags → ESI 1-2 (Critical / Emergent)
    risk_level = "Low"
    esi = 5
    red_flags_found = []

    for category, phrases in RED_FLAG_KEYWORDS.items():
        for phrase in phrases + [category]:
            if phrase in text_lower:
                red_flags_found.append(category)
                break

    if red_flags_found:
        risk_level = "Critical" if len(red_flags_found) >= 2 or "unconscious" in red_flags_found else "Emergent"
        esi = 1 if risk_level == "Critical" else 2
    else:
        # 2. Check medium risk → ESI 3-4
        medium_hits = [kw for kw in MEDIUM_RISK_KEYWORDS if kw in text_lower]
        if len(medium_hits) >= 2:
            risk_level = "Urgent"
            esi = 3
        elif medium_hits:
            risk_level = "Less Urgent"
            esi = 4

    # 3. Determine department
    department = "General Medicine"
    for keywords, dept in DEPARTMENT_RULES:
        if any(kw in text_lower for kw in keywords):
            department = dept
            break

    # 4. Generate differential suggestions
    differential = suggest_differentials(text_lower)

    return {
        "risk_level": risk_level,
        "esi_level": esi,
        "department": department,
        "red_flags": red_flags_found,
        "differential": differential,
    }


def suggest_differentials(text: str) -> list[str]:
    """Return a list of possible diagnoses based on symptom patterns."""
    differentials = []

    patterns = {
        "chest pain + radiation": (["chest pain", "arm"], ["Acute Coronary Syndrome", "Myocardial Infarction"]),
        "chest pain + breathing": (["chest pain", "breath"], ["Pulmonary Embolism", "Pneumothorax"]),
        "headache + sudden": (["sudden", "headache"], ["Subarachnoid Hemorrhage", "Migraine"]),
        "fever + cough": (["fever", "cough"], ["Pneumonia", "Bronchitis", "COVID-19"]),
        "abdominal + pain": (["stomach", "pain"], ["Appendicitis", "Gastritis", "Pancreatitis"]),
        "dizziness + nausea": (["dizzy", "nausea"], ["Vertigo", "Hypotension", "Dehydration"]),
    }

    for _name, (triggers, diagnoses) in patterns.items():
        if all(t in text for t in triggers):
            differentials.extend(diagnoses)

    if not differentials:
        differentials = ["Requires further clinical evaluation"]

    return differentials


# ─── Display Helpers ──────────────────────────────────────────────────────────

ESI_COLORS = {
    1: "\033[91m",  # red
    2: "\033[93m",  # yellow
    3: "\033[33m",  # orange-ish
    4: "\033[96m",  # cyan
    5: "\033[92m",  # green
}
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"


def typewriter(text: str, delay: float = 0.02):
    """Print text character by character for demo effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def print_banner():
    print(f"""
{BOLD}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    \033[96m  __  __         _ _ ____  _              _                \033[0m{BOLD}║
║    \033[96m |  \\/  | ___ __| (_)  _ \\(_)_ __ ___  __| |               \033[0m{BOLD}║
║    \033[96m | |\\/| |/ _ \\ _| | | |_) | | '__/ _ \\/ _` |               \033[0m{BOLD}║
║    \033[96m | |  | |  __/ |_| | |  __/| | | |  __/ (_| |               \033[0m{BOLD}║
║    \033[96m |_|  |_|\\___|\\__|_|_|_|   |_|_|  \\___|\\__,_|               \033[0m{BOLD}║
║                                                              ║
║           AI Clinical Pre-Triage Agent — Demo                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{RESET}
""")


def print_separator():
    print(f"{DIM}{'─' * 60}{RESET}")


def print_result(result: dict, patient_info: dict):
    """Pretty-print the triage result."""
    esi = result["esi_level"]
    color = ESI_COLORS.get(esi, RESET)

    print()
    print_separator()
    print(f"\n{BOLD}  TRIAGE RESULT{RESET}")
    print_separator()

    # Patient info
    print(f"\n  {DIM}Patient:{RESET}    {patient_info.get('age', '?')} / {patient_info.get('gender', '?')}")
    print(f"  {DIM}Time:{RESET}      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  {DIM}Case ID:{RESET}   TRI-{datetime.now().strftime('%Y%m%d%H%M%S')}")

    print_separator()

    # Risk level
    print(f"\n  {BOLD}Risk Level:{RESET}    {color}{BOLD}{result['risk_level']}{RESET}")
    print(f"  {BOLD}ESI Level:{RESET}     {color}{BOLD}ESI-{esi}{RESET}  {DIM}({5 - esi + 1}/5 urgency){RESET}")
    print(f"  {BOLD}Department:{RESET}    {result['department']}")

    # Red flags
    if result["red_flags"]:
        print(f"\n  \033[91m⚠ Red Flags Detected:{RESET}")
        for flag in result["red_flags"]:
            print(f"    \033[91m• {flag}{RESET}")

    # Differential diagnosis
    print(f"\n  {BOLD}Differential Diagnosis:{RESET}")
    for i, dx in enumerate(result["differential"], 1):
        print(f"    {i}. {dx}")

    # JSON summary
    summary = {
        "case_id": f"TRI-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "patient": patient_info,
        "assessment": {
            "risk_level": result["risk_level"],
            "esi_level": result["esi_level"],
            "department": result["department"],
            "red_flags": result["red_flags"],
            "differential_diagnosis": result["differential"],
        },
    }

    print_separator()
    print(f"\n  {BOLD}Structured Summary (JSON):{RESET}")
    print(f"\n{DIM}{json.dumps(summary, indent=4, ensure_ascii=False)}{RESET}")
    print_separator()

    # Disclaimer
    print(f"\n  {DIM}* This is a demonstration tool. Not for real clinical use.{RESET}")
    print(f"  {DIM}* Always consult a licensed medical professional.{RESET}\n")


# ─── Main Loop ────────────────────────────────────────────────────────────────

def get_patient_info() -> dict:
    """Collect basic patient demographics."""
    print(f"\n{BOLD}  Step 1 — Patient Information{RESET}\n")

    age = input(f"  {DIM}Age:{RESET} ").strip() or "Unknown"
    gender = input(f"  {DIM}Gender (M/F/Other):{RESET} ").strip() or "Unknown"

    return {"age": age, "gender": gender}


def get_symptoms() -> str:
    """Collect symptom description from user."""
    print(f"\n{BOLD}  Step 2 — Describe Symptoms{RESET}")
    print(f"  {DIM}(Describe what the patient is experiencing in plain language){RESET}\n")

    symptoms = input(f"  Symptoms: ").strip()

    if not symptoms:
        print(f"  \033[93mNo symptoms entered. Using default placeholder.{RESET}")
        symptoms = "general malaise"

    return symptoms


def run_demo():
    """Main demo loop."""
    print_banner()

    typewriter(f"  {BOLD}Welcome to MediTriage Demo{RESET}")
    typewriter(f"  {DIM}AI-powered clinical pre-triage simulation{RESET}\n")
    time.sleep(0.5)

    while True:
        # Collect info
        patient_info = get_patient_info()
        symptoms = get_symptoms()

        # Simulate thinking
        print(f"\n  {DIM}Analyzing symptoms...", end="", flush=True)
        for _ in range(3):
            time.sleep(0.4)
            sys.stdout.write(".")
            sys.stdout.flush()
        print(f" Done.{RESET}\n")
        time.sleep(0.3)

        # Analyze
        result = analyze_symptoms(symptoms)

        # Display
        print_result(result, patient_info)

        # Continue?
        print_separator()
        again = input(f"\n  {BOLD}Triage another patient? (y/n):{RESET} ").strip().lower()
        if again not in ("y", "yes"):
            print(f"\n  {BOLD}Thank you for using MediTriage.{RESET}")
            print(f"  {DIM}github.com/jigehandsome/ai-pretriage-agent{RESET}\n")
            break


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print(f"\n\n  {DIM}Session ended.{RESET}\n")
