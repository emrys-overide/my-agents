"""
Tests for Pydantic models & JSON schema conformance.
"""

import json
from pathlib import Path
import pytest
from src.framework.models import (
    PRDDocument,
    BusinessCase,
    ValueViabilityMatrix,
    NonFunctionalRequirements,
    ArchitectureSpec,
    ComponentSpec,
    StateMachineSpec,
    StateTransition,
    MemoryLayerSpec,
    ToolContract,
    ComputeLatencyBudget,
    CodeDeliverable,
    SourceFile,
    TestFile,
    AuditReport,
    TrustworthyAIPillars,
    OWASPVulnerability
)


def test_prd_model_validation():
    prd = PRDDocument(
        project_name="Test AI Underwriting",
        executive_summary="Testing automated underwriting platform.",
        business_case=BusinessCase(
            estimated_tco=50000.0,
            projected_roi="3.2x in Year 1",
            labor_efficiency_gain_pct=65.0,
            token_cost_per_task=0.015
        ),
        value_viability_matrix=ValueViabilityMatrix(
            value_score=9.0,
            viability_score=8.5,
            classification="Quick Win"
        ),
        functional_requirements=["Parse documents", "Verify identity"],
        non_functional_requirements=NonFunctionalRequirements(
            max_p95_latency_ms=1500.0,
            target_accuracy_pct=99.0,
            context_window_limit=8192
        ),
        acceptance_criteria=["Zero schema validation errors"],
        regulatory_constraints=["SOC2 compliance"]
    )
    assert prd.value_viability_matrix.classification == "Quick Win"
    assert prd.business_case.estimated_tco == 50000.0
    json_data = prd.model_dump()
    assert "functional_requirements" in json_data


def test_audit_report_model_validation():
    report = AuditReport(
        audit_id="AUDIT_TEST_001",
        overall_score=94.5,
        verdict="PASS_EXEMPLARY",
        trustworthy_ai_pillars=TrustworthyAIPillars(
            fair_and_impartial=92.0,
            robust_and_reliable=95.0,
            transparent_and_explainable=94.0,
            respectful_of_privacy=96.0,
            safe_and_secure=95.0,
            responsible_and_accountable=93.0,
            grc_and_compliance=95.0
        ),
        owasp_llm_vulnerabilities=[
            OWASPVulnerability(
                code="LLM01",
                severity="LOW",
                description="Prompt injection mitigated.",
                status="MITIGATED"
            )
        ],
        remediation_actions=["Maintain audit trail"],
        sign_off_timestamp="2026-08-31T07:00:00Z"
    )
    assert report.overall_score == 94.5
    assert report.verdict == "PASS_EXEMPLARY"
