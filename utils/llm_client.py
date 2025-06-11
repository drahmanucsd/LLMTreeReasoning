# utils/llm_client.py

import subprocess
import time
from typing import Optional

from config import LLM_MODEL, MODEL_TEMPERATURE, MAX_TOKENS, MAX_RETRIES, TIMEOUT_SEC
from utils.logging import log_info, log_error


class OllamaClient:
    def __init__(
        self,
        model_name: str = LLM_MODEL,
        temperature: float = MODEL_TEMPERATURE,
        max_tokens: Optional[int] = MAX_TOKENS,
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    def send(self, prompt: str) -> str:
        """Call `ollama eval` under the hood, with retries."""
        cmd = ["ollama", "eval", self.model_name, "--prompt", prompt]
        if self.temperature is not None:
            cmd += ["--temperature", str(self.temperature)]
        if self.max_tokens:
            cmd += ["--max-tokens", str(self.max_tokens)]

        attempt = 0
        while attempt < MAX_RETRIES:
            attempt += 1
            try:
                log_info(f"OllamaClient: running {cmd!r} (attempt {attempt})")
                completed = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=TIMEOUT_SEC
                )
                if completed.returncode == 0:
                    return completed.stdout.strip()
                else:
                    log_error(
                        f"OllamaClient non-zero exit (code={completed.returncode}): "
                        f"{completed.stderr.strip()}"
                    )
            except subprocess.TimeoutExpired:
                log_error(f"OllamaClient timeout after {TIMEOUT_SEC}s (attempt {attempt})")
            time.sleep(1)  # backoff

        raise RuntimeError("OllamaClient: all retries exhausted")
