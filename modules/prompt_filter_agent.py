# modules/prompt_filter_agent.py
from config import FILTER_PROMPT_PATH
from utils.llm_client import OllamaClient
import logging

class PromptFilterAgent:
    """
    Takes the raw user_goal and returns a cleaned, de-duplicated version.
    """
    def __init__(self):
        with open(FILTER_PROMPT_PATH, "r") as f:
            self.prompt_template = f.read()
        self.client = OllamaClient()

    async def run(self, raw_prompt: str) -> str:
        """
        Returns the cleaned prompt as a plain string.
        """
        prompt = self.prompt_template.replace("{raw_prompt}", raw_prompt)
        logging.debug(f"[{self.__class__.__name__}] using prompt template from {FILTER_PROMPT_PATH}")
        logging.debug(f"[{self.__class__.__name__}] filled prompt:\n{prompt}\n--- end prompt ---")
        raw_output = self.client.send(prompt)

        # single-positional call
        cleaned = self.client.send(prompt)
        return cleaned.strip()
