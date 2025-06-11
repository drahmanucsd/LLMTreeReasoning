import asyncio

from config import (
    EXPLORE_PROMPT_PATH,
    LLM_MODEL,
    MODEL_TEMPERATURE,
    MAX_TOKENS,
    TIMEOUT_SEC,
    MAX_RETRIES,
)
from utils.llm_client import OllamaClient
from utils.parser import parse_explore
from schemas.task_models import ExploreResult


class ExplorerAgent:
    """
    Agent to outline implementation steps for a given subtask.
    """
    def __init__(self):
        # Load prompt template
        with open(EXPLORE_PROMPT_PATH, 'r') as f:
            self.prompt_template = f.read()

        # Initialize LLM client
        self.client = OllamaClient(
            model_name=LLM_MODEL,
            temperature=MODEL_TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )

    async def run(self, subtask: str) -> ExploreResult:
        """
        Run the explorer-agent on the given subtask.

        Steps:
          1. Fill prompt template with subtask
          2. Call the LLM (with retries and timeout)
          3. Parse the raw response into ExploreResult
          4. Return the ExploreResult
        """
        # 1. Prepare prompt
        prompt = self.prompt_template.replace("{subtask}", subtask)

        # 2. Invoke LLM with retries and timeout
        raw_output = await self.client.send(
            prompt_text=prompt,
            timeout=TIMEOUT_SEC,
            retries=MAX_RETRIES,
        )

        # 3. Parse into structured result
        explore_result = parse_explore(raw_output)

        # 4. Return
        return explore_result
