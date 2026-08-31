"""
Base Consulting Agent class enforcing identity declarations, logging,
and deterministic schema compliance across all Deloitte agent personas.
"""

from __future__ import annotations
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("DeloitteAI")


class BaseConsultingAgent(ABC):
    def __init__(self, name: str, role_title: str, deloitte_counterpart: str):
        self.name = name
        self.role_title = role_title
        self.deloitte_counterpart = deloitte_counterpart

    def log_status(self, status: str, detail: str = ""):
        prefix = f"[{self.name.upper()} | {status.upper()}]"
        msg = f"{prefix} {detail}" if detail else prefix
        logger.info(msg)
        return msg

    @abstractmethod
    def execute(self, input_data: Any) -> BaseModel:
        """Executes the agent's phase deliverable according to its playbook."""
        pass
