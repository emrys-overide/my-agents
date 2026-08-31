"""
Strategy & Product Consultant Persona (@Consultant)
Implements Deloitte AI Strategy, 2x2 Value-vs-Viability Matrix, TCO/ROI modeling, and PRD generation.
"""

from __future__ import annotations
from typing import Dict, Any, List
from .base_agent import BaseConsultingAgent
from ..models import PRDDocument, BusinessCase, ValueViabilityMatrix, NonFunctionalRequirements
from ..tools import calculate_roi_and_tco


class StrategyConsultantAgent(BaseConsultingAgent):
    def __init__(self):
        super().__init__(
            name="Consultant",
            role_title="Strategy & Product Consultant",
            deloitte_counterpart="AI Strategy & Business Innovation Lead"
        )

    def execute(self, client_brief: str) -> PRDDocument:
        self.log_status("IN_PROGRESS", f"Conducting market discovery and value-spine decomposition for brief: '{client_brief}'")
        
        # Calculate financial ROI and TCO based on Deloitte economic benchmarks
        roi_data = calculate_roi_and_tco(
            annual_task_volume=120_000,
            avg_human_minutes_per_task=15.0,
            human_hourly_rate_usd=45.0,
            avg_tokens_per_task=1800,
            blended_token_cost_per_million=1.50,
            infrastructure_fixed_cost_annual=18000.0,
            development_cost_usd=65000.0
        )
        
        prd = PRDDocument(
            project_name=f"Enterprise Autonomous Solution: {client_brief[:40]}",
            executive_summary=(
                f"Deloitte EVD Phase 1 Discovery: Strategic initiative to implement an autonomous, "
                f"governed AI capability addressing '{client_brief}'. Designed to unlock labor productivity, "
                f"enforce compliance, and deliver rapid time-to-value."
            ),
            business_case=BusinessCase(
                estimated_tco=roi_data["year_1_tco"],
                projected_roi=roi_data["roi_summary"],
                labor_efficiency_gain_pct=roi_data["efficiency_gain_pct"],
                token_cost_per_task=roi_data["token_cost_per_task"]
            ),
            value_viability_matrix=ValueViabilityMatrix(
                value_score=9.2,
                viability_score=8.8,
                classification="Quick Win"
            ),
            functional_requirements=[
                "Deterministic multi-agent task routing with explicit identity logging.",
                "Real-time knowledge ingestion with hybrid dense/sparse vector retrieval.",
                "Automated validation against strict JSON schema contracts before tool dispatch.",
                "Human-in-the-loop escalation pathway for confidence scores below 85%."
            ],
            non_functional_requirements=NonFunctionalRequirements(
                max_p95_latency_ms=1800.0,
                target_accuracy_pct=98.5,
                context_window_limit=8192
            ),
            acceptance_criteria=[
                "All API interactions pass schema validation with zero unhandled exceptions.",
                "Auditor Trustworthy AI score exceeds 90% across all 7 dimensions.",
                "Automated test suite achieves >= 90% statement coverage."
            ],
            regulatory_constraints=[
                "Zero-retention policy for customer PII/PHI under GDPR Article 17 and HIPAA Security Rule.",
                "EU AI Act Conformity Assessment for high-impact decision support.",
                "Immutable episodic event logging for external auditability."
            ]
        )
        
        self.log_status("COMPLETED", f"PRD generated successfully with estimated Year 1 TCO: ${prd.business_case.estimated_tco:,.2f}")
        return prd
