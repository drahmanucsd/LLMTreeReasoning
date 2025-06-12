# tests/test_explorer_agent.py
import pytest
from modules.explorer_agent import ExplorerAgent
from utils.llm_client import OllamaClient
from schemas.task_models import ExploreResult

@pytest.mark.asyncio
async def test_explorer_agent_parses(monkeypatch):
    raw = '{"subtask": "X", "steps": ["step1", "step2"], "dependencies": ["D1"]}'
    monkeypatch.setattr(OllamaClient, 'send', lambda self, prompt: raw)

    agent = ExplorerAgent()
    result = await agent.run("X", parent_context="")

    assert isinstance(result, ExploreResult)
    assert result.subtask == "X"
    assert result.steps == ["step1", "step2"]
    assert result.dependencies == ["D1"]

@pytest.mark.asyncio
async def test_explorer_agent_no_dependencies(monkeypatch):
    raw = '{"subtask": "Y", "steps": ["only_step"]}'
    monkeypatch.setattr(OllamaClient, 'send', lambda self, prompt: raw)

    agent = ExplorerAgent()
    result = await agent.run("Y", parent_context="")

    assert result.subtask == "Y"
    assert result.steps == ["only_step"]
    assert result.dependencies is None