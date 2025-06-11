import re
import json
from typing import Dict

from schemas.task_models import MetaResult, ExploreResult, EvalResult


def _extract_json(raw: str) -> Dict:
    """
    Scan raw text for the first JSON object and parse it.
    Raises ValueError if none found or parsing fails.
    """
    # Attempt to find a JSON block in the response
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM response")
    try:
        return json.loads(match.group())
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}")


def parse_meta(raw: str) -> MetaResult:
    """
    Parse raw LLM output into a MetaResult.
    Expects JSON with keys: is_multi_step (bool), subtasks (list[str]), approaches (list[str]).
    """
    data = _extract_json(raw)
    # Validate required fields
    if 'is_multi_step' not in data or 'subtasks' not in data or 'approaches' not in data:
        raise ValueError(f"Missing keys in MetaResult JSON: {data.keys()}")
    return MetaResult(**data)


def parse_explore(raw: str) -> ExploreResult:
    """
    Parse raw LLM output into an ExploreResult.
    Expects JSON with keys: subtask (str), steps (list[str]), optional dependencies (list[str]).
    """
    data = _extract_json(raw)
    if 'subtask' not in data or 'steps' not in data:
        raise ValueError(f"Missing keys in ExploreResult JSON: {data.keys()}")
    return ExploreResult(**data)


def parse_eval(raw: str) -> EvalResult:
    """
    Parse raw LLM output into an EvalResult.
    Expects JSON with keys: merged_plan (list[str]), issues (list[str]).
    """
    data = _extract_json(raw)
    if 'merged_plan' not in data or 'issues' not in data:
        raise ValueError(f"Missing keys in EvalResult JSON: {data.keys()}")
    return EvalResult(**data)
