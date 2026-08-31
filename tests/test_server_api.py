"""
Tests for FastAPI server endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from src.server import app

client = TestClient(app)


def test_index_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "Deloitte AI Team" in response.text


def test_chat_with_agent_route():
    for persona in ["consultant", "architect", "engineer", "auditor", "orchestrator"]:
        res = client.post("/api/agent/chat", json={"persona": persona, "message": "Test inquiry"})
        assert res.status_code == 200
        data = res.json()
        assert data["persona"] == persona
        assert "reply" in data


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
