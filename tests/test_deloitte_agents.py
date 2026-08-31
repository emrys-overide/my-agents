"""
Tests for individual persona execution and tool calling.
"""

import pytest
from src.framework.personas import (
    StrategyConsultantAgent,
    PrincipalArchitectAgent,
    ImplementationEngineerAgent,
    TrustworthyAuditorAgent,
    OrchestratorAgent
)
from src.framework.tools import calculate_roi_and_tco, validate_python_code_syntax_and_safety


def test_financial_roi_tool():
    roi = calculate_roi_and_tco(
        annual_task_volume=10000,
        avg_human_minutes_per_task=20.0,
        human_hourly_rate_usd=50.0,
        avg_tokens_per_task=2000
    )
    assert roi["year_1_tco"] > 0
    assert "ROI" in roi["roi_summary"]
    assert roi["efficiency_gain_pct"] == 70.0


def test_security_ast_tool():
    safe_code = "def add(a, b):\n    return a + b\n"
    is_safe, issues = validate_python_code_syntax_and_safety(safe_code)
    assert is_safe is True
    assert len(issues) == 0

    unsafe_code = "def bad():\n    eval('2+2')\n"
    is_safe, issues = validate_python_code_syntax_and_safety(unsafe_code)
    assert is_safe is False
    assert len(issues) > 0


def test_consultant_agent_execution():
    consultant = StrategyConsultantAgent()
    prd = consultant.execute("Automate IT Helpdesk Tier 1 Tickets")
    assert prd.project_name.startswith("Enterprise Autonomous Solution:")
    assert prd.value_viability_matrix.classification == "Quick Win"
    assert len(prd.functional_requirements) > 0


def test_architect_agent_execution():
    consultant = StrategyConsultantAgent()
    prd = consultant.execute("Automate IT Helpdesk Tier 1 Tickets")
    architect = PrincipalArchitectAgent()
    arch_spec = architect.execute(prd)
    assert arch_spec.topology_type == "Hierarchical"
    assert len(arch_spec.components) == 4
    assert len(arch_spec.state_machine.states) >= 5


def test_engineer_and_auditor_agent_execution():
    consultant = StrategyConsultantAgent()
    prd = consultant.execute("Automate IT Helpdesk Tier 1 Tickets")
    architect = PrincipalArchitectAgent()
    arch_spec = architect.execute(prd)
    engineer = ImplementationEngineerAgent()
    code_deliv = engineer.execute(arch_spec)
    assert code_deliv.build_status == "SUCCESS"
    assert code_deliv.test_coverage_pct >= 90.0

    auditor = TrustworthyAuditorAgent()
    audit_report = auditor.execute(prd, arch_spec, code_deliv)
    assert audit_report.overall_score >= 85.0
    assert audit_report.verdict in ["PASS_EXEMPLARY", "PASS_CONDITIONAL"]
