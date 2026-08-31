"""
Principal Systems Architect Persona (@Architect)
Implements Deloitte AI Factory Architecture, topology mapping, state machines, and schema contracts.
"""

from __future__ import annotations
from typing import Dict, Any, List
from .base_agent import BaseConsultingAgent
from ..models import (
    PRDDocument,
    ArchitectureSpec,
    ComponentSpec,
    StateMachineSpec,
    StateTransition,
    MemoryLayerSpec,
    ToolContract,
    ComputeLatencyBudget
)


class PrincipalArchitectAgent(BaseConsultingAgent):
    def __init__(self):
        super().__init__(
            name="Architect",
            role_title="Principal Systems Architect",
            deloitte_counterpart="Enterprise & GenAI Systems Architect"
        )

    def execute(self, prd: PRDDocument) -> ArchitectureSpec:
        self.log_status("IN_PROGRESS", f"Designing AI Factory system architecture for: '{prd.project_name}'")
        
        components = [
            ComponentSpec(
                name="OrchestratorControlPlane",
                role="EVD Phase Governor & Context Coordinator",
                inputs=["UserRequest", "SpecialistOutputs"],
                outputs=["PhaseGateDecisions", "ExecutiveReport"]
            ),
            ComponentSpec(
                name="ConsultingEngine",
                role="Strategy & Financial Optimization Engine",
                inputs=["ClientBrief", "MarketData"],
                outputs=["PRDDocument", "ValueSpine"]
            ),
            ComponentSpec(
                name="EngineeringRuntime",
                role="Industrialized Agent Runtime & Tool Pipeline",
                inputs=["ArchitectureSpec"],
                outputs=["CodeDeliverable", "ExecutionLogs"]
            ),
            ComponentSpec(
                name="TrustworthyAuditor",
                role="7-Pillar Trustworthy AI & Red-Teaming Validator",
                inputs=["CodeDeliverable", "ArchitectureSpec", "PRDDocument"],
                outputs=["AuditReport", "RemediationPlan"]
            )
        ]
        
        state_machine = StateMachineSpec(
            initial_state="INIT",
            states=["INIT", "DISCOVERY", "ARCHITECTURE", "IMPLEMENTATION", "AUDIT", "DELIVERY", "REMEDIATION"],
            transitions=[
                StateTransition(from_state="INIT", to_state="DISCOVERY", trigger="brief_submitted"),
                StateTransition(from_state="DISCOVERY", to_state="ARCHITECTURE", trigger="prd_approved"),
                StateTransition(from_state="ARCHITECTURE", to_state="IMPLEMENTATION", trigger="architecture_approved"),
                StateTransition(from_state="IMPLEMENTATION", to_state="AUDIT", trigger="code_generated"),
                StateTransition(from_state="AUDIT", to_state="DELIVERY", trigger="audit_passed"),
                StateTransition(from_state="AUDIT", to_state="REMEDIATION", trigger="audit_failed"),
                StateTransition(from_state="REMEDIATION", to_state="IMPLEMENTATION", trigger="remediation_applied")
            ]
        )
        
        memory_layer = MemoryLayerSpec(
            working_context="Sliding Token Window (max 8192 tokens) with prompt caching",
            episodic_storage="Structured JSONL session event store with immutable audit trail",
            semantic_vector_store="HNSW cosine similarity index with 768-dim text embeddings"
        )
        
        tool_contracts = [
            ToolContract(
                tool_name="financial_roi_calculator",
                description="Calculates TCO, labor cost offset, and payback metrics",
                input_schema={
                    "type": "object",
                    "properties": {
                        "annual_task_volume": {"type": "integer"},
                        "human_hourly_rate_usd": {"type": "number"}
                    },
                    "required": ["annual_task_volume", "human_hourly_rate_usd"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "year_1_tco": {"type": "number"},
                        "roi_summary": {"type": "string"}
                    }
                }
            ),
            ToolContract(
                tool_name="security_ast_validator",
                description="Performs static AST safety and vulnerability scanning on generated code",
                input_schema={
                    "type": "object",
                    "properties": {"code_str": {"type": "string"}},
                    "required": ["code_str"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "is_safe": {"type": "boolean"},
                        "issues": {"type": "array", "items": {"type": "string"}}
                    }
                }
            )
        ]
        
        compute_budget = ComputeLatencyBudget(
            model_tier="Frontier Reasoning (Gemini 3.7 Flash Pro)",
            estimated_latency_ms=1250.0,
            max_tokens_per_call=4096
        )
        
        spec = ArchitectureSpec(
            system_name=f"ArchSpec_{prd.project_name.replace(' ', '_')[:30]}",
            topology_type="Hierarchical",
            components=components,
            state_machine=state_machine,
            memory_layer=memory_layer,
            tool_contracts=tool_contracts,
            compute_and_latency_budget=compute_budget,
            fallback_and_recovery=[
                "Exponential backoff with jitter on API rate limit encounters (HTTP 429)",
                "Fallback to secondary compact model if primary inference times out > 5000ms",
                "Automatic rollback to last known valid state on unhandled tool failure"
            ]
        )
        
        self.log_status("COMPLETED", f"Architecture blueprint created with {len(components)} components and {len(state_machine.transitions)} state transitions.")
        return spec
