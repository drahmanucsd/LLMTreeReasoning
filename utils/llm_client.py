# utils/llm_client.py

import subprocess
import time
from typing import Optional

from config import LLM_MODEL, MAX_RETRIES, TIMEOUT_SEC
from utils.logging import log_info, log_error


class OllamaClient:
    def __init__(
        self,
        model_name: str = LLM_MODEL,
    ):
        self.model_name = model_name

    def send(self, prompt: str) -> str:
        """
        Call `ollama run <model> <prompt>` under the hood, with retries.
        """
        # Pass the prompt as a positional argument, no --prompt flag
        cmd = ["ollama", "run", self.model_name, prompt]

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
            time.sleep(1)

        raise RuntimeError("OllamaClient: all retries exhausted")
