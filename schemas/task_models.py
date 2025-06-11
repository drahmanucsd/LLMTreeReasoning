from pydantic import BaseModel
from typing import List, Optional


class MetaResult(BaseModel):
    """
    Result of meta-agent decomposition.
    """
    is_multi_step: bool              # True if the task breaks into subtasks
    subtasks: List[str]              # Immediate one-layer-deep subtasks
    approaches: List[str]            # Alternative high-level strategies


class ExploreResult(BaseModel):
    """
    Result of explorer-agent for a single subtask.
    """
    subtask: str                     # Echoed input subtask
    steps: List[str]                 # Ordered implementation steps
    dependencies: List[str] = []     # Other subtasks this depends on


class EvalResult(BaseModel):
    """
    Result of evaluator-agent merging multiple branches.
    """
    merged_plan: List[str]           # Unified ordered list of all steps
    issues: List[str] = []           # Conflicts or missing pieces identified
