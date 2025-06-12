import json
from config import EXPLORE_PROMPT_PATH
from utils.llm_client import OllamaClient
from utils.parser import parse_explore
from schemas.task_models import ExploreResult
import logging

class ExplorerAgent:
    def __init__(self):
        with open(EXPLORE_PROMPT_PATH, "r") as f:
            self.prompt_template = f.read()
        self.client = OllamaClient()

    async def run(self, subtask: str, parent_context: str="") -> ExploreResult:
        """
        1. Fill the explorer prompt with the subtask.
        2. Call the LLM synchronously.
        3. Parse JSON into ExploreResult.
        """
        # 1. Prepare prompt
        prompt = (
            self.prompt_template
            .replace("{parent_context}", parent_context)
            .replace("{subtask}", subtask)
        )


        # … inside run() …
        logging.debug(f"[{self.__class__.__name__}] using prompt template from {EXPLORE_PROMPT_PATH}")
        logging.debug(f"[{self.__class__.__name__}] filled prompt:\n{prompt}\n--- end prompt ---")
        raw_output = self.client.send(prompt)

        # 2. Invoke LLM (synchronous)
        raw_output = self.client.send(prompt)

        # 3. Parse into ExploreResult
        result = parse_explore(raw_output)

        return result
