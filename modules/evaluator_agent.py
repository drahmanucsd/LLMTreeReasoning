import json
import asyncio

from config import (
    EVAL_PROMPT_PATH,
    LLM_MODEL,
    MODEL_TEMPERATURE,
    MAX_TOKENS,
    TIMEOUT_SEC,
    MAX_RETRIES,
)
from utils.llm_client import OllamaClient
from utils.parser import parse_eval
from schemas.task_models import EvalResult, ExploreResult


class EvaluatorAgent:
    """
    Agent to merge multiple explorer branch outputs into a unified plan.
    """
    def __init__(self):
        # Load prompt template
        with open(EVAL_PROMPT_PATH, 'r') as f:
            self.prompt_template = f.read()

        # Initialize LLM client
        self.client = OllamaClient(
            model_name=LLM_MODEL,
            temperature=MODEL_TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )

    async def run(self, branch_results: list[ExploreResult]) -> EvalResult:
        """
        Run the evaluator-agent on the given list of branch results.

        Steps:
          1. Serialize branch_results to JSON
          2. Fill prompt template with branches_json
          3. Call the LLM (with retries and timeout)
          4. Parse the raw response into EvalResult
          5. Return the EvalResult
        """
        # 1. Serialize branch outputs
        branches_json = json.dumps([br.dict() for br in branch_results], indent=2)

        # 2. Prepare prompt
        prompt = self.prompt_template.replace("{branches_json}", branches_json)

        # 3. Invoke LLM with retries and timeout
        raw_output = await self.client.send(
            prompt_text=prompt,
            timeout=TIMEOUT_SEC,
            retries=MAX_RETRIES,
        )

        # 4. Parse into structured result
        eval_result = parse_eval(raw_output)

        # 5. Return
        return eval_result
