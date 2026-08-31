"""
Integration test for full end-to-end EVD orchestration lifecycle.
"""

import pytest
from src.framework.orchestrator_engine import EVDOrchestrationEngine


def test_full_evd_engagement_lifecycle():
    engine = EVDOrchestrationEngine()
    report = engine.run_engagement("Autonomous Regulatory Compliance Assistant for FinTech")
    
    assert report.engagement_title.startswith("Enterprise Autonomous Solution:")
    assert report.final_readiness_status in ["PRODUCTION_READY", "PILOT_READY"]
    assert report.prd.business_case.estimated_tco > 0
    assert report.audit_report.overall_score >= 90.0
    assert "Deloitte Autonomous Consultancy Executive Summary" in report.managing_director_summary
