# modules/synthesizer_agent.py

import json
from typing import Any, Dict

from config import SYNTH_PROMPT_PATH
from utils.llm_client import OllamaClient
from schemas.task_models import SynthResult  # you’ll need to add this model in task_models.py
import logging

class SynthesizerAgent:
    """
    Combines the parent goal, raw branch outputs, evaluator feedback
    and suggestions into one final, unified plan.
    """
    def __init__(self):
        # Load the synthesizer prompt template
        with open(SYNTH_PROMPT_PATH, "r") as f:
            self.prompt_template = f.read()
        self.client = OllamaClient()

    async def run(self, synth_input: Dict[str, Any]) -> SynthResult:
        """
        synth_input dict must contain:
          - "user_goal": str
          - "branches": List[dict]        # each branch_result.dict()
          - "suggestions": List[str]
        
        Returns a SynthResult (with at least .merged_plan: List[str])
        """
        # 1. Fill the template
        prompt = (
            self.prompt_template
            .replace("{user_goal}", synth_input["user_goal"])
            .replace("{branches_json}", json.dumps(synth_input["branches"], indent=2))
            .replace("{suggestions_json}", json.dumps(synth_input["suggestions"], indent=2))
        )
        logging.debug(f"[{self.__class__.__name__}] using prompt template from {SYNTH_PROMPT_PATH}")
        logging.debug(f"[{self.__class__.__name__}] filled prompt:\n{prompt}\n--- end prompt ---")
        raw_output = self.client.send(prompt)

        # 2. Invoke the LLM (synchronous call)
        raw_output = self.client.send(prompt)

        # 3. Parse the JSON response into your SynthResult schema
        data = json.loads(raw_output)
        return SynthResult(**data)
