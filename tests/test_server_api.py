"""
Fast, robust unit tests for FastAPI server endpoints.
"""

from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from src.server import app

client = TestClient(app)


def test_index_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "Deloitte AI Team" in response.text


def test_llm_status_route():
    res = client.get("/api/llm/status")
    assert res.status_code == 200
    data = res.json()
    assert "primary_brain" in data
    assert "active_agents" in data


def test_chat_with_agent_route():
    with patch("src.server.call_unified_llm") as mock_llm:
        mock_llm.return_value = {
            "reply": "Live LLM response from Specialist.",
            "provider": "gemini-2.5-flash",
            "is_live_llm": True
        }
        res = client.post("/api/agent/chat", json={"persona": "architect", "message": "What is our architecture?"})
        assert res.status_code == 200
        data = res.json()
        assert data["persona"] == "architect"
        assert "reply" in data


def test_agent_to_agent_dialogue_route():
    with patch("src.server.call_unified_llm") as mock_llm:
        mock_llm.side_effect = [
            {"reply": "@Architect, what vector index do you recommend?", "provider": "gemini-2.5-flash"},
            {"reply": "@Consultant, I recommend HNSW with cosine similarity.", "provider": "gemini-2.5-flash"}
        ]
        res = client.post(
            "/api/agent/dialogue",
            json={
                "agent_a": "consultant",
                "agent_b": "architect",
                "topic": "Determine vector index storage architecture"
            }
        )
        assert res.status_code == 200
        data = res.json()
        assert "turns" in data
        assert len(data["turns"]) == 2
        assert data["turns"][0]["speaker"] == "@Consultant"
        assert data["turns"][1]["speaker"] == "@Architect"


def test_team_conference_route():
    with patch("src.server.call_unified_llm") as mock_llm:
        mock_llm.return_value = {"reply": "Specialist assessment complete.", "provider": "gemini-2.5-flash"}
        res = client.post(
            "/api/agent/conference",
            json={
                "topic": "Enterprise migration to multi-agent architecture"
            }
        )
        assert res.status_code == 200
        data = res.json()
        assert "conference_contributions" in data
        assert len(data["conference_contributions"]) == 5


def test_calculate_roi_route():
    res = client.post(
        "/api/financial/roi",
        json={
            "annual_task_volume": 50000,
            "avg_human_minutes_per_task": 10.0,
            "human_hourly_rate_usd": 40.0,
            "avg_tokens_per_task": 1500
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert "year_1_tco" in data
    assert "roi_summary" in data


def test_engagement_run_route():
    res = client.post(
        "/api/engagement/run",
        json={"brief": "Test Autonomous Security Agent"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "engagement_title" in data
    assert "prd" in data
    assert "architecture_spec" in data
    assert "audit_report" in data


def test_custom_agent_routes():
    res = client.post(
        "/api/agents/custom",
        json={
            "id": "devops",
            "name": "DevOps Engineer",
            "role": "Cloud Automation",
            "code": "@DevOps",
            "color": "#f97316",
            "system_prompt": "You are the DevOps Engineer."
        }
    )
    assert res.status_code == 200
    assert res.json()["status"] == "SUCCESS"

    list_res = client.get("/api/agents/custom")
    assert list_res.status_code == 200
    agents = list_res.json()["custom_agents"]
    assert any(a["id"] == "devops" for a in agents)


def test_chat_without_live_model_returns_unavailable():
    with patch("src.server.call_unified_llm", return_value={"reply": None, "provider": "none"}):
        res = client.post("/api/agent/chat", json={"persona": "auditor", "message": "Assess controls"})
    assert res.status_code == 503
    assert "No live language model" in res.json()["detail"]


def test_dialogue_without_live_model_returns_unavailable():
    with patch("src.server.call_unified_llm", return_value={"reply": None, "provider": "none"}):
        res = client.post("/api/agent/dialogue", json={
            "agent_a": "consultant", "agent_b": "architect", "topic": "Review controls"
        })
    assert res.status_code == 503


def test_conference_without_live_model_returns_unavailable():
    with patch("src.server.call_unified_llm", return_value={"reply": None, "provider": "none"}):
        res = client.post("/api/agent/conference", json={"topic": "Review controls"})
    assert res.status_code == 503
