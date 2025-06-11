# tests/test_evaluator_agent.py
import pytest
from modules.evaluator_agent import EvaluatorAgent
from utils.llm_client import OllamaClient
from schemas.task_models import EvalResult

@pytest.mark.asyncio
async def test_evaluator_agent_parses(monkeypatch):
    raw = '{"merged_plan": ["m1", "m2"], "issues": ["i1"]}'
    monkeypatch.setattr(OllamaClient, 'send', lambda self, prompt: raw)

    agent = EvaluatorAgent()
    result = await agent.run([
        # pass dummy branch results; actual parsing happens on raw
    ])

    assert isinstance(result, EvalResult)
    assert result.merged_plan == ["m1", "m2"]
    assert result.issues == ["i1"]

@pytest.mark.asyncio
async def test_evaluator_agent_empty(monkeypatch):
    raw = '{"merged_plan": [], "issues": []}'
    monkeypatch.setattr(OllamaClient, 'send', lambda self, prompt: raw)

    agent = EvaluatorAgent()
    result = await agent.run([])

    assert result.merged_plan == []
    assert result.issues == []
