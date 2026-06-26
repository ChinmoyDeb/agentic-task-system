from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Task:
    """
    Represents a single unit of work in the agentic pipeline.

    Each task is assigned to a specialized agent and tracked by the
    orchestrator as it moves through the pipeline.
    """

    id: int
    agent: str
    description: str
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None