import json
from config import EVAL_PROMPT_PATH
from utils.llm_client import OllamaClient
from utils.parser import parse_eval
from schemas.task_models import EvalResult, ExploreResult
import logging

class EvaluatorAgent:
    def __init__(self):
        with open(EVAL_PROMPT_PATH, "r") as f:
            self.prompt_template = f.read()
        self.client = OllamaClient()

    async def run(self, branch_results: list[ExploreResult]) -> EvalResult:
        """
        1. Serialize branch_results to JSON.
        2. Fill the evaluator prompt.
        3. Call the LLM synchronously.
        4. Parse JSON into EvalResult.
        """
        # 1. Serialize branch outputs
        branches_json = json.dumps([br.dict() for br in branch_results], indent=2)

        # 2. Prepare prompt
        prompt = self.prompt_template.replace("{branches_json}", branches_json)

        # … inside run() …
        logging.debug(f"[{self.__class__.__name__}] using prompt template from {EVAL_PROMPT_PATH}")
        logging.debug(f"[{self.__class__.__name__}] filled prompt:\n{prompt}\n--- end prompt ---")
        raw_output = self.client.send(prompt)

        # 3. Invoke LLM (synchronous)
        raw_output = self.client.send(prompt)

        # 4. Parse into EvalResult
        result = parse_eval(raw_output)

        return result
