import asyncio

from config import (
    META_PROMPT_PATH,
    LLM_MODEL,
    MODEL_TEMPERATURE,
    MAX_TOKENS,
    TIMEOUT_SEC,
    MAX_RETRIES,
)
from utils.llm_client import OllamaClient
from utils.parser import parse_meta
from schemas.task_models import MetaResult


class MetaAgent:
    """
    Agent to decompose a user goal into subtasks and propose approaches.
    """
    def __init__(self):
        # Load prompt template
        with open(META_PROMPT_PATH, 'r') as f:
            self.prompt_template = f.read()

        # Initialize LLM client
        self.client = OllamaClient(
            model_name=LLM_MODEL,
            temperature=MODEL_TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )

    async def run(self, user_goal: str) -> MetaResult:
        """
        Run the meta-agent on the given user goal.

        Steps:
          1. Fill prompt template with user_goal
          2. Call the LLM (with retries and timeout)
          3. Parse the raw response into MetaResult
          4. Return the MetaResult
        """
        # 1. Prepare prompt
        prompt = self.prompt_template.replace("{user_goal}", user_goal)

        # 2. Invoke LLM with retries and timeout
        raw_output = await self.client.send(
            prompt_text=prompt,
            timeout=TIMEOUT_SEC,
            retries=MAX_RETRIES,
        )

        # 3. Parse into structured result
        meta_result = parse_meta(raw_output)

        # 4. Return
        return meta_result
