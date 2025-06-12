# schemas/task_models.py

from pydantic import BaseModel
from typing import List, Optional

class MetaResult(BaseModel):
    is_multi_step: bool
    subtasks: List[str]

class ExploreResult(BaseModel):
    subtask: str
    steps: List[str]
    dependencies: Optional[List[str]] = None

class EvalResult(BaseModel):
    issues: List[str]
    suggestions: List[str]

class SynthResult(BaseModel):
    merged_plan: List[str]

class FilterResult(BaseModel):
    filtered_prompt: str
