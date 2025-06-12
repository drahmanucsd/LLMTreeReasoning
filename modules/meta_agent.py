import json
from config import META_PROMPT_PATH
from utils.llm_client import OllamaClient
from utils.parser import parse_meta
from schemas.task_models import MetaResult
import logging

class MetaAgent:
    def __init__(self):
        # Load the prompt template once at initialization
        with open(META_PROMPT_PATH, "r") as f:
            self.prompt_template = f.read()
        # OllamaClient.send(prompt: str) -> str
        self.client = OllamaClient()

    async def run(self, user_goal: str, parent_context: str="") -> MetaResult:
        """
        1. Fill the meta prompt with the user goal.
        2. Call the LLM synchronously via client.send(prompt).
        3. Parse JSON into MetaResult.
        """
        # 1. Prepare prompt
        prompt = (self.prompt_template
                .replace("{parent_context}", parent_context)
                .replace("{user_goal}", user_goal)
        )


        logging.debug(f"[{self.__class__.__name__}] using prompt template from {META_PROMPT_PATH}")
        logging.debug(f"[{self.__class__.__name__}] filled prompt:\n{prompt}\n--- end prompt ---")
        raw_output = self.client.send(prompt)

        # 2. Invoke LLM (synchronous)
        raw_output = self.client.send(prompt)

        # 3. Parse into MetaResult
        result = parse_meta(raw_output)

        return result
