"""
MediTriage — API Server
=======================
FastAPI server that exposes the triage agent as REST endpoints.
"""

from fastapi import FastAPI
from pydantic import BaseModel

from config import APP_NAME, APP_VERSION
from workflows.triage_workflow import TriageWorkflow

app = FastAPI(title=APP_NAME, version=APP_VERSION)

workflow = TriageWorkflow()


class TriageRequest(BaseModel):
    symptoms: str
    age: str = "Unknown"
    gender: str = "Unknown"


class TriageResponse(BaseModel):
    case_id: str
    risk_level: str
    esi_level: int
    department: str
    differential: list[str]
    reasoning: str


@app.get("/")
def root():
    return {"app": APP_NAME, "version": APP_VERSION, "status": "running"}


@app.post("/triage", response_model=TriageResponse)
def run_triage(req: TriageRequest):
    result = workflow.run(
        symptoms=req.symptoms,
        patient_info={"age": req.age, "gender": req.gender},
    )
    return result
