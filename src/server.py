"""
FastAPI Server for Deloitte Autonomous AI Consultancy UI.
Serves interactive web frontend and provides REST endpoints for live agent execution,
multi-agent peer-to-peer dialogues, and direct LLM human-agent chat.
"""

from __future__ import annotations
import os
import sys
import requests
from pathlib import Path
from typing import Dict, Any, Optional, List
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
from src.framework.gemini_client import (
    call_gemini_api,
    call_ollama_api,
    call_unified_llm,
    get_gemini_api_key
)

app = FastAPI(
    title="Deloitte Autonomous AI Consultancy API",
    description="Multi-agent EVD orchestration, LLM dialogues, and persona intercom backend.",
    version="2.5.0"
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
        "Keep your response crisp, professional, and actionable."
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


class DialogueRequest(BaseModel):
    agent_a: str  # e.g., "consultant"
    agent_b: str  # e.g., "architect"
    topic: str
    api_key: Optional[str] = None


class ConferenceRequest(BaseModel):
    topic: str
    agents: Optional[List[str]] = None
    api_key: Optional[str] = None


class ROIRequest(BaseModel):
    annual_task_volume: int = 120000
    avg_human_minutes_per_task: float = 15.0
    human_hourly_rate_usd: float = 45.0
    avg_tokens_per_task: int = 1800


class CustomAgentRequest(BaseModel):
    id: str
    name: str
    role: str
    code: str
    color: str = "#3b82f6"
    system_prompt: str


custom_agents_store: Dict[str, Dict[str, Any]] = {}


@app.get("/api/config/status")
@app.get("/api/llm/status")
async def get_config_status():
    has_gemini = bool(get_gemini_api_key())
    
    # Probe local Ollama models
    ollama_models = []
    has_ollama = False
    try:
        res = requests.get("http://localhost:11434/api/tags", timeout=1.5)
        if res.status_code == 200:
            has_ollama = True
            ollama_models = [m.get("name") for m in res.json().get("models", [])]
    except Exception:
        pass

    primary_brain = "gemini-2.5-flash" if has_gemini else ("ollama (qwen2.5-coder)" if has_ollama else "persona_playbook")

    return {
        "gemini_api_configured": has_gemini,
        "ollama_active": has_ollama,
        "ollama_models": ollama_models,
        "primary_brain": primary_brain,
        "active_agents": ["orchestrator", "consultant", "architect", "engineer", "auditor"] + list(custom_agents_store.keys())
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
    """
    Direct 1-on-1 human-to-agent chat powered by LLM (Gemini or Ollama).
    """
    persona_key = req.persona.lower().replace("@", "").strip()
    msg = req.message
    
    if persona_key not in PERSONA_PROMPTS:
        raise HTTPException(status_code=400, detail=f"Unknown persona: {req.persona}")

    system_prompt = PERSONA_PROMPTS[persona_key]
    
    # Call unified multi-LLM engine
    llm_res = call_unified_llm(
        system_prompt=system_prompt,
        user_message=msg,
        gemini_key=req.api_key
    )

    if llm_res.get("reply"):
        return {
            "persona": req.persona,
            "reply": llm_res["reply"],
            "provider": llm_res["provider"],
            "mode": "live_llm"
        }

    # Intelligent Playbook Fallback
    if persona_key == "consultant":
        reply = (
            f"Deloitte AI Strategy analysis for '{msg}': "
            f"Mapped to the Quick Win quadrant (Value: 9.1/10, Viability: 8.7/10). "
            f"Projects ~70% labor efficiency offset with a payback period under 1.5 months."
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
        "provider": "persona_playbook",
        "mode": "playbook_simulated"
    }


@app.post("/api/agent/dialogue")
async def agent_to_agent_dialogue(req: DialogueRequest):
    """
    Agent-to-Agent Peer Discussion (Agent A talks to Agent B using LLMs).
    """
    p_a = req.agent_a.lower().replace("@", "").strip()
    p_b = req.agent_b.lower().replace("@", "").strip()

    if p_a not in PERSONA_PROMPTS or p_b not in PERSONA_PROMPTS:
        raise HTTPException(status_code=400, detail="Invalid agents specified.")

    prompt_a = PERSONA_PROMPTS[p_a]
    prompt_b = PERSONA_PROMPTS[p_b]

    # Turn 1: Agent A speaks to Agent B
    msg_a = f"Consulting with @{p_b.title()} regarding: '{req.topic}'. What is your assessment and how should we align?"
    res_a = call_unified_llm(system_prompt=prompt_a, user_message=msg_a, gemini_key=req.api_key)
    speech_a = res_a.get("reply") or f"@{p_b.title()}, I need your specialist review on '{req.topic}' to ensure adherence to standards."

    # Turn 2: Agent B responds to Agent A
    msg_b = f"@{p_a.title()} asked: '{speech_a}'. Provide your expert response and technical recommendations."
    res_b = call_unified_llm(system_prompt=prompt_b, user_message=msg_b, gemini_key=req.api_key)
    speech_b = res_b.get("reply") or f"@{p_a.title()}, from my domain perspective, '{req.topic}' aligns with our operational parameters and security safeguards."

    return {
        "topic": req.topic,
        "turns": [
            {"speaker": f"@{p_a.title()}", "message": speech_a, "provider": res_a.get("provider", "unified")},
            {"speaker": f"@{p_b.title()}", "message": speech_b, "provider": res_b.get("provider", "unified")}
        ]
    }


@app.post("/api/agent/conference")
async def team_conference(req: ConferenceRequest):
    """
    Multi-Agent Conference: All 5 agents debate and contribute to a topic.
    """
    agents = req.agents or ["orchestrator", "consultant", "architect", "engineer", "auditor"]
    contributions = []

    context_so_far = f"Topic: {req.topic}\n"
    for ag in agents:
        ag_key = ag.lower().replace("@", "").strip()
        if ag_key in PERSONA_PROMPTS:
            sys_p = PERSONA_PROMPTS[ag_key]
            user_m = f"You are attending the Deloitte AI Leadership Conference.\n{context_so_far}\nGive your concise, high-value contribution as @{ag_key.title()}."
            llm_res = call_unified_llm(system_prompt=sys_p, user_message=user_m, gemini_key=req.api_key)
            speech = llm_res.get("reply") or f"As @{ag_key.title()}, I confirm readiness to support '{req.topic}' under our framework."
            contributions.append({
                "agent": f"@{ag_key.title()}",
                "message": speech,
                "provider": llm_res.get("provider", "unified")
            })
            context_so_far += f"\n@{ag_key.title()}: {speech}"

    return {
        "topic": req.topic,
        "conference_contributions": contributions
    }


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
