"""
Deloitte EVD Multi-Agent Orchestration Engine.
Coordinates the state machine lifecycle across:
Discovery (@Consultant) -> Architecture (@Architect) -> Implementation (@Engineer) -> Trust Audit (@Auditor) -> Delivery (@Orchestrator).
"""

from __future__ import annotations
import logging
from typing import Dict, Any, Optional
from .models import (
    PRDDocument,
    ArchitectureSpec,
    CodeDeliverable,
    AuditReport,
    ExecutiveEngagementReport
)
from .personas import (
    OrchestratorAgent,
    StrategyConsultantAgent,
    PrincipalArchitectAgent,
    ImplementationEngineerAgent,
    TrustworthyAuditorAgent
)

logger = logging.getLogger("DeloitteAI")


class EVDOrchestrationEngine:
    def __init__(self, max_remediation_cycles: int = 2):
        self.max_remediation_cycles = max_remediation_cycles
        self.orchestrator = OrchestratorAgent()
        self.consultant = StrategyConsultantAgent()
        self.architect = PrincipalArchitectAgent()
        self.engineer = ImplementationEngineerAgent()
        self.auditor = TrustworthyAuditorAgent()

    def run_engagement(self, client_brief: str) -> ExecutiveEngagementReport:
        logger.info("\n" + "="*80)
        logger.info("  STARTING DELOITTE AUTONOMOUS AI CONSULTANCY ENGAGEMENT")
        logger.info("="*80 + "\n")
        
        self.orchestrator.execute(client_brief)
        
        # Phase 1: Discovery & Scoping (@Consultant)
        logger.info("\n>>> [PHASE 1: STRATEGY & VALUE SPINE DISCOVERY]")
        prd: PRDDocument = self.consultant.execute(client_brief)
        
        # Phase 2: Architecture & System Blueprint (@Architect)
        logger.info("\n>>> [PHASE 2: AI FACTORY TECHNICAL ARCHITECTURE]")
        arch_spec: ArchitectureSpec = self.architect.execute(prd)
        
        # Phase 3 & 4: Implementation & Trustworthy AI Audit Loop
        remediation_count = 0
        code_deliverable: Optional[CodeDeliverable] = None
        audit_report: Optional[AuditReport] = None
        
        while remediation_count <= self.max_remediation_cycles:
            logger.info(f"\n>>> [PHASE 3: INDUSTRIALIZED IMPLEMENTATION (Cycle {remediation_count + 1})]")
            code_deliverable = self.engineer.execute(arch_spec)
            
            logger.info("\n>>> [PHASE 4: TRUSTWORTHY AI™ & ZERO-TRUST AUDIT]")
            audit_report = self.auditor.execute(prd, arch_spec, code_deliverable)
            
            if audit_report.verdict in ["PASS_EXEMPLARY", "PASS_CONDITIONAL"]:
                logger.info(f"\n✓ Trustworthy AI Gate PASSED with score: {audit_report.overall_score}% ({audit_report.verdict})")
                break
            else:
                remediation_count += 1
                logger.warning(
                    f"\n⚠ Trustworthy AI Gate FAILED (Score: {audit_report.overall_score}%). "
                    f"Initiating remediation cycle {remediation_count}/{self.max_remediation_cycles}."
                )
                if remediation_count > self.max_remediation_cycles:
                    logger.error("❌ Max remediation cycles exceeded. Escalating to Managing Director.")
                    break
                    
        # Phase 5: Executive Delivery (@Orchestrator)
        logger.info("\n>>> [PHASE 5: EXECUTIVE DELIVERY & VALUE REALIZATION]")
        executive_report = self.orchestrator.synthesize_executive_report(
            client_brief=client_brief,
            prd=prd,
            arch_spec=arch_spec,
            code_deliverable=code_deliverable,
            audit_report=audit_report
        )
        
        logger.info("\n" + "="*80)
        logger.info(f"  ENGAGEMENT COMPLETE: {executive_report.final_readiness_status}")
        logger.info("="*80 + "\n")
        return executive_report
