"""
Pydantic data models enforcing strict schema contracts across agent personas.
Aligned with Deloitte EVD and Trustworthy AI™ methodologies.
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict


class ValueViabilityMatrix(BaseModel):
    value_score: float = Field(..., ge=0.0, le=10.0, description="Business value rating (0-10)")
    viability_score: float = Field(..., ge=0.0, le=10.0, description="Technical/operational viability (0-10)")
    classification: Literal["Quick Win", "Strategic Bet", "Incremental Utility", "Deprioritize"] = Field(
        ..., description="2x2 Prioritization Quadrant"
    )


class BusinessCase(BaseModel):
    estimated_tco: float = Field(..., description="Estimated Total Cost of Ownership ($)")
    projected_roi: str = Field(..., description="Projected ROI summary / multiple (e.g. '3.8x in Year 1')")
    labor_efficiency_gain_pct: float = Field(..., ge=0.0, le=100.0, description="Productivity gain percentage")
    token_cost_per_task: float = Field(..., description="Estimated token cost per task execution ($)")


class NonFunctionalRequirements(BaseModel):
    max_p95_latency_ms: float = Field(..., description="Maximum acceptable p95 latency in milliseconds")
    target_accuracy_pct: float = Field(..., ge=0.0, le=100.0, description="Target task accuracy percentage")
    context_window_limit: int = Field(..., description="Max token budget for context window")


class PRDDocument(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    project_name: str
    executive_summary: str
    business_case: BusinessCase
    value_viability_matrix: ValueViabilityMatrix
    functional_requirements: List[str]
    non_functional_requirements: NonFunctionalRequirements
    acceptance_criteria: List[str]
    regulatory_constraints: List[str]


class ComponentSpec(BaseModel):
    name: str
    role: str
    inputs: List[str]
    outputs: List[str]


class StateTransition(BaseModel):
    from_state: str
    to_state: str
    trigger: str


class StateMachineSpec(BaseModel):
    initial_state: str
    states: List[str]
    transitions: List[StateTransition]


class MemoryLayerSpec(BaseModel):
    working_context: str
    episodic_storage: str
    semantic_vector_store: str


class ToolContract(BaseModel):
    tool_name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


class ComputeLatencyBudget(BaseModel):
    model_tier: str
    estimated_latency_ms: float
    max_tokens_per_call: int


class ArchitectureSpec(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    system_name: str
    topology_type: Literal["Hierarchical", "Sequential", "Choreographed", "Hybrid"]
    components: List[ComponentSpec]
    state_machine: StateMachineSpec
    memory_layer: MemoryLayerSpec
    tool_contracts: List[ToolContract]
    compute_and_latency_budget: ComputeLatencyBudget
    fallback_and_recovery: List[str]


class SourceFile(BaseModel):
    path: str
    description: str
    code: str


class TestFile(BaseModel):
    __test__ = False
    path: str
    test_count: int
    code: str


class CodeDeliverable(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    module_name: str
    source_files: List[SourceFile]
    test_files: List[TestFile]
    dependencies: List[str]
    test_coverage_pct: float = Field(..., ge=0.0, le=100.0)
    build_status: Literal["SUCCESS", "FAILED"]


class TrustworthyAIPillars(BaseModel):
    fair_and_impartial: float = Field(..., ge=0.0, le=100.0)
    robust_and_reliable: float = Field(..., ge=0.0, le=100.0)
    transparent_and_explainable: float = Field(..., ge=0.0, le=100.0)
    respectful_of_privacy: float = Field(..., ge=0.0, le=100.0)
    safe_and_secure: float = Field(..., ge=0.0, le=100.0)
    responsible_and_accountable: float = Field(..., ge=0.0, le=100.0)
    grc_and_compliance: float = Field(..., ge=0.0, le=100.0)


class OWASPVulnerability(BaseModel):
    code: str  # e.g., "LLM01", "LLM02"
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    description: str
    status: Literal["MITIGATED", "OPEN", "ACCEPTED"]


class AuditReport(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    audit_id: str
    overall_score: float = Field(..., ge=0.0, le=100.0)
    verdict: Literal["PASS_EXEMPLARY", "PASS_CONDITIONAL", "REJECTED_REMEDIATION_REQUIRED"]
    trustworthy_ai_pillars: TrustworthyAIPillars
    owasp_llm_vulnerabilities: List[OWASPVulnerability]
    remediation_actions: List[str]
    sign_off_timestamp: str


class ExecutiveEngagementReport(BaseModel):
    engagement_title: str
    client_brief: str
    managing_director_summary: str
    prd: PRDDocument
    architecture_spec: ArchitectureSpec
    code_deliverable: CodeDeliverable
    audit_report: AuditReport
    final_readiness_status: Literal["PRODUCTION_READY", "PILOT_READY", "BLOCKED"]
