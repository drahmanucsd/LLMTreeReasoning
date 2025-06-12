# tests/test_meta_agent.py
import pytest
from modules.meta_agent import MetaAgent
from utils.llm_client import OllamaClient
from schemas.task_models import MetaResult

@pytest.mark.asyncio
async def test_meta_agent_parses(monkeypatch):
    raw = '{"is_multi_step": true, "subtasks": ["A","B"], "approaches": ["X","Y"]}'
    # Stub out the LLM response
    monkeypatch.setattr(OllamaClient, 'send', lambda self, prompt: raw)

    agent = MetaAgent()
    result = await agent.run("dummy goal", parent_context="")

    assert isinstance(result, MetaResult)
    assert result.is_multi_step is True
    assert result.subtasks == ["A", "B"]

@pytest.mark.asyncio
async def test_meta_agent_single_step(monkeypatch):
    raw = '{"is_multi_step": false, "subtasks": [], "approaches": []}'
    monkeypatch.setattr(OllamaClient, 'send', lambda self, prompt: raw)

    agent = MetaAgent()
    result = await agent.run("another goal", parent_context="")

    assert result.is_multi_step is False
    assert result.subtasks == []