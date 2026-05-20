#!/usr/bin/env python3
"""
MediTriage — Main Entry Point
==============================
CLI interface for the clinical pre-triage agent.
Usage: python main.py
"""

import json
import sys

from workflows.triage_workflow import TriageWorkflow


def main():
    print("=" * 50)
    print("  MediTriage — AI Clinical Pre-Triage Agent")
    print("=" * 50)

    workflow = TriageWorkflow()

    # Collect patient info
    print("\n[Patient Information]")
    age = input("  Age: ").strip() or "Unknown"
    gender = input("  Gender (M/F/Other): ").strip() or "Unknown"

    # Collect symptoms
    print("\n[Symptom Description]")
    symptoms = input("  Describe symptoms: ").strip()

    if not symptoms:
        print("Error: No symptoms provided.")
        sys.exit(1)

    # Run triage pipeline
    print("\n[Processing...]")
    result = workflow.run(
        symptoms=symptoms,
        patient_info={"age": age, "gender": gender},
    )

    # Display results
    print("\n" + "=" * 50)
    print("  TRIAGE RESULT")
    print("=" * 50)
    print(f"  Case ID:     {result['case_id']}")
    print(f"  Risk Level:  {result['assessment']['risk_level']}")
    print(f"  ESI Level:   {result['assessment']['esi_level']}")
    print(f"  Department:  {result['routing']['department']}")
    print(f"  Confidence:  {result['assessment']['confidence']}")
    print(f"  Reasoning:   {result['assessment']['reasoning']}")

    if result["assessment"]["red_flags"]:
        print(f"\n  ⚠ Red Flags: {', '.join(result['assessment']['red_flags'])}")

    # JSON output
    print("\n" + "-" * 50)
    print("  JSON Output:")
    print("-" * 50)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print()


if __name__ == "__main__":
    main()
