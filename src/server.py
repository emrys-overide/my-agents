"""
FastAPI Server for Deloitte Autonomous AI Consultancy UI.
Serves interactive web frontend and provides REST endpoints for live agent execution.
"""

from __future__ import annotations
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.framework.orchestrator_engine import EVDOrchestrationEngine
from src.framework.personas import (
    StrategyConsultantAgent,
    PrincipalArchitectAgent,
    ImplementationEngineerAgent,
    TrustworthyAuditorAgent,
    OrchestratorAgent
)
from src.framework.tools import calculate_roi_and_tco
from src.framework.gemini_client import call_gemini_api, get_gemini_api_key

app = FastAPI(
    title="Deloitte Autonomous AI Consultancy API",
    description="Multi-agent EVD orchestration and direct persona intercom backend.",
    version="1.0.0"
)

# Engine instance
engine = EVDOrchestrationEngine()
latest_engagement: Optional[Dict[str, Any]] = None

# Personas system prompts
PERSONA_PROMPTS = {
    "consultant": (
        "You are the Deloitte Strategy & Product Consultant (@Consultant). "
        "Apply Deloitte's Enterprise Value Delivery (EVD) and 2x2 Value-vs-Viability framework. "
        "Focus on business viability, ROI, labor efficiency gain, and testable acceptance criteria. "
        "Keep your response structured, professional, and actionable."
    ),
    "architect": (
        "You are the Deloitte Principal Systems Architect (@Architect). "
        "Apply Deloitte's AI Factory as a Service blueprint. "
        "Focus on component topologies, finite state machines, memory layers (working context, episodic, vector RAG), "
        "and strict JSON schema API contracts."
    ),
    "engineer": (
        "You are the Deloitte Lead AI/ML & MLOps Implementation Engineer (@Engineer). "
        "Focus on clean, robust, type-hinted Python code, agent execution loops with exponential backoff retries, "
        "and comprehensive pytest test suites with >90% coverage."
    ),
    "auditor": (
        "You are the Deloitte Trustworthy AI™ & Cyber Risk Auditor (@Auditor). "
        "Maintain zero-trust. Evaluate systems across the 7 Trust Dimensions (Fairness, Reliability, Transparency, "
        "Privacy, Safety, Accountability, Compliance) and OWASP LLM Top 10 defenses."
    ),
    "orchestrator": (
        "You are the Deloitte Managing Director & Engagement Lead (@Orchestrator). "
        "Coordinate the multi-agent engagement lifecycle, align with client North Star goals, manage scope and budget, "
        "and synthesize executive briefings."
    )
}


class EngagementRequest(BaseModel):
    brief: str
    api_key: Optional[str] = None


class ChatRequest(BaseModel):
    persona: str
    message: str
    api_key: Optional[str] = None


class ROIRequest(BaseModel):
    annual_task_volume: int = 120000
    avg_human_minutes_per_task: float = 15.0
    human_hourly_rate_usd: float = 45.0
    avg_tokens_per_task: int = 1800


@app.get("/api/config/status")
async def get_config_status():
    has_key = bool(get_gemini_api_key())
    return {
        "gemini_api_configured": has_key,
        "default_model": "gemini-2.5-flash",
        "active_agents": ["orchestrator", "consultant", "architect", "engineer", "auditor"]
    }


@app.post("/api/engagement/run")
async def run_engagement(req: EngagementRequest):
    global latest_engagement
    try:
        report = engine.run_engagement(client_brief=req.brief)
        latest_engagement = report.model_dump()
        return latest_engagement
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/deliverables/latest")
async def get_latest_deliverables():
    if not latest_engagement:
        return {"status": "NO_ENGAGEMENTS_RUN_YET"}
    return latest_engagement


@app.post("/api/agent/chat")
async def chat_with_agent(req: ChatRequest):
    persona_key = req.persona.lower()
    msg = req.message
    
    if persona_key not in PERSONA_PROMPTS:
        raise HTTPException(status_code=400, detail=f"Unknown persona: {req.persona}")

    system_prompt = PERSONA_PROMPTS[persona_key]
    
    # Try calling live Gemini API if API key exists
    live_reply = call_gemini_api(
        system_prompt=system_prompt,
        user_message=msg,
        model_name="gemini-2.5-flash",
        api_key=req.api_key
    )

    if live_reply and not live_reply.startswith("[API Error"):
        return {
            "persona": req.persona,
            "reply": live_reply,
            "mode": "live_gemini"
        }

    # Fallback to structured playbook response if no API key is provided
    if persona_key == "consultant":
        reply = (
            f"Deloitte AI Strategy evaluation for '{msg}': "
            f"Mapped to the Quick Win quadrant (Value: 9.1/10, Viability: 8.7/10). "
            f"The business case projects a 70% labor efficiency offset with a payback period under 1.5 months."
        )
    elif persona_key == "architect":
        reply = (
            f"AI Factory Architecture for '{msg}': "
            f"Designed a hierarchical 4-component state topology with strict JSON schema tool contracts, "
            f"sliding-window working context (8k tokens), and an episodic vector memory layer."
        )
    elif persona_key == "engineer":
        reply = (
            f"Industrialized Engineering Runtime for '{msg}': "
            f"Implemented resilient execution loop with exponential retry backoff, Pydantic type safety, "
            f"and automated pytest verification harness achieving 94.5% coverage."
        )
    elif persona_key == "auditor":
        reply = (
            f"Trustworthy AI™ Audit for '{msg}': "
            f"Evaluated across all 7 pillars (Overall Score: 94.3%, Status: PASS_EXEMPLARY). "
            f"OWASP LLM01 Prompt Injection and LLM05 Code Injection defenses verified and mitigated."
        )
    else:
        reply = (
            f"Managing Director response regarding '{msg}': "
            f"Aligned initiative with enterprise North Star objectives. Dispatched discovery to @Consultant "
            f"and architecture gating to @Architect."
        )

    return {
        "persona": req.persona,
        "reply": reply,
        "mode": "playbook_simulated"
    }


class CustomAgentRequest(BaseModel):
    id: str
    name: str
    role: str
    code: str
    color: str = "#3b82f6"
    system_prompt: str


custom_agents_store: Dict[str, Dict[str, Any]] = {}


@app.post("/api/agents/custom")
async def create_custom_agent(req: CustomAgentRequest):
    custom_agents_store[req.id] = req.model_dump()
    PERSONA_PROMPTS[req.id] = req.system_prompt
    return {"status": "SUCCESS", "agent": req.model_dump()}


@app.get("/api/agents/custom")
async def list_custom_agents():
    return {"custom_agents": list(custom_agents_store.values())}


@app.post("/api/financial/roi")
async def calculate_roi(req: ROIRequest):
    data = calculate_roi_and_tco(
        annual_task_volume=req.annual_task_volume,
        avg_human_minutes_per_task=req.avg_human_minutes_per_task,
        human_hourly_rate_usd=req.human_hourly_rate_usd,
        avg_tokens_per_task=req.avg_tokens_per_task
    )
    return data


# Serve Frontend
WEB_DIR = PROJECT_ROOT / "web"
if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(str(WEB_DIR / "index.html"))


def start(port: int = 8000, host: str = "0.0.0.0"):
    uvicorn.run("src.server:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    start()
