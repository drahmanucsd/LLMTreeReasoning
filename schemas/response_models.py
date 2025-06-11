import re
import json

from .task_models import MetaResult, ExploreResult, EvalResult

# Regex to extract the first JSON object in a response
JSON_OBJ_PATTERN = re.compile(r"\{(?:[^{}]|(?R))*\}", re.DOTALL)


def _extract_json(raw: str) -> str:
    """
    Find and return the first JSON object in the raw LLM response.
    Raises ValueError if none found.
    """
    match = JSON_OBJ_PATTERN.search(raw)
    if not match:
        raise ValueError("No JSON object found in LLM response")
    return match.group(0)


def parse_meta_response(raw: str) -> MetaResult:
    """
    Parse a raw meta-agent response into a MetaResult model.
    """
    json_str = _extract_json(raw)
    data = json.loads(json_str)
    return MetaResult(**data)


def parse_explore_response(raw: str) -> ExploreResult:
    """
    Parse a raw explorer-agent response into an ExploreResult model.
    """
    json_str = _extract_json(raw)
    data = json.loads(json_str)
    return ExploreResult(**data)


def parse_eval_response(raw: str) -> EvalResult:
    """
    Parse a raw evaluator-agent response into an EvalResult model.
    """
    json_str = _extract_json(raw)
    data = json.loads(json_str)
    return EvalResult(**data)
