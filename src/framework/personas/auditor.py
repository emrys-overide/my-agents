"""
Quality Assurance, Security & Trustworthy AI Auditor Persona (@Auditor)
Implements Deloitte Trustworthy AI™ (7 Pillars), OWASP LLM Top 10 Red-Teaming, and GRC Gating.
"""

from __future__ import annotations
import datetime
from typing import Dict, Any, List
from .base_agent import BaseConsultingAgent
from ..models import (
    PRDDocument,
    ArchitectureSpec,
    CodeDeliverable,
    AuditReport,
    TrustworthyAIPillars,
    OWASPVulnerability
)
from ..tools import evaluate_trustworthy_ai_pillars


class TrustworthyAuditorAgent(BaseConsultingAgent):
    def __init__(self):
        super().__init__(
            name="Auditor",
            role_title="Lead QA, Security & Trustworthy AI Auditor",
            deloitte_counterpart="Trustworthy AI™ & Cyber Risk Lead"
        )

    def execute(
        self,
        prd: PRDDocument,
        arch_spec: ArchitectureSpec,
        code_deliverable: CodeDeliverable
    ) -> AuditReport:
        self.log_status("IN_PROGRESS", f"Auditing deliverable '{code_deliverable.module_name}' against 7 Trustworthy AI pillars.")
        
        eval_result = evaluate_trustworthy_ai_pillars(
            code_deliverable=code_deliverable.model_dump(),
            prd=prd.model_dump(),
            architecture_spec=arch_spec.model_dump()
        )
        
        pillars_data = eval_result["pillars"]
        pillars = TrustworthyAIPillars(
            fair_and_impartial=pillars_data["fair_and_impartial"],
            robust_and_reliable=pillars_data["robust_and_reliable"],
            transparent_and_explainable=pillars_data["transparent_and_explainable"],
            respectful_of_privacy=pillars_data["respectful_of_privacy"],
            safe_and_secure=pillars_data["safe_and_secure"],
            responsible_and_accountable=pillars_data["responsible_and_accountable"],
            grc_and_compliance=pillars_data["grc_and_compliance"]
        )
        
        vulnerabilities = [
            OWASPVulnerability(
                code=v["code"],
                severity=v["severity"],
                description=v["description"],
                status=v["status"]
            )
            for v in eval_result["vulnerabilities"]
        ]
        
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        audit_report = AuditReport(
            audit_id=f"AUDIT_{now_utc.strftime('%Y%m%d_%H%M%S')}",
            overall_score=eval_result["overall_score"],
            verdict=eval_result["verdict"],
            trustworthy_ai_pillars=pillars,
            owasp_llm_vulnerabilities=vulnerabilities,
            remediation_actions=eval_result["remediation_actions"],
            sign_off_timestamp=now_utc.isoformat()
        )
        
        self.log_status(
            "COMPLETED",
            f"Audit finished with score: {audit_report.overall_score}% | Verdict: {audit_report.verdict}"
        )
        return audit_report
