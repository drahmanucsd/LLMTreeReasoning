# utils/parser.py

import json
from typing import Optional, Any, Dict

from schemas.task_models import MetaResult, ExploreResult, EvalResult


def parse_meta(raw: str) -> MetaResult:
    """
    Parse a raw JSON string from the meta-agent into a MetaResult.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in meta response: {e}")

    # Required boolean
    is_multi = data.get("is_multi_step")
    # Lists default to empty if missing or null
    subtasks = data.get("subtasks") or []

    return MetaResult(
        is_multi_step=is_multi,
        subtasks=subtasks,
    )


def parse_explore(raw: str) -> ExploreResult:
    """
    Parse a raw JSON string from the explorer-agent into an ExploreResult.
    If 'dependencies' is missing, it will be None.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in explore response: {e}")

    subtask = data.get("subtask")
    steps = data.get("steps") or []

    # Only set dependencies if explicitly provided
    dependencies = data.get("dependencies", None)
    if isinstance(dependencies, list) and len(dependencies) == 0:
        # You can choose to treat an empty list as None as well,
        # but tests expect missing → None, present-but-empty → []
        # Here we leave an explicit empty list intact.
        pass

    return ExploreResult(
        subtask=subtask,
        steps=steps,
        dependencies=dependencies,
    )


def parse_eval(raw: str) -> EvalResult:
    """
    Parse a raw JSON string from the evaluator-agent into an EvalResult.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in eval response: {e}")

    issues = data.get("issues") or []
    suggestions = data.get("suggestions") or []


    return EvalResult(
        issues=issues,
        suggestions=suggestions
    )
