# config.py
import os

# LLM model configuration
LLM_MODEL = "llama3"            # Ollama model to use for all agents
MODEL_TEMPERATURE = 0.7           # Sampling temperature for LLM outputs
MAX_TOKENS = 2048                 # Maximum tokens to generate per request
TIMEOUT_SEC = 30                  # Timeout (in seconds) for LLM calls
MAX_RETRIES = 3                   # Number of retry attempts on failure

# Concurrency settings
MAX_PARALLEL_TASKS = 5            # Maximum number of concurrent explorer agents
MAX_RECURSION_DEPTH = 3

# Prompt file paths
PROJECT_ROOT = os.path.dirname(__file__)
PROMPT_DIR = os.path.join(PROJECT_ROOT, "prompts")
META_PROMPT_PATH   = os.path.join(PROMPT_DIR, "meta_prompt.txt")
EXPLORE_PROMPT_PATH = os.path.join(PROMPT_DIR, "explore_prompt.txt")
FILTER_PROMPT_PATH = os.path.join(PROMPT_DIR, "filter_prompt.txt")
SYNTH_PROMPT_PATH = os.path.join(PROMPT_DIR, "synth_prompt.txt")
EVAL_PROMPT_PATH = os.path.join(PROMPT_DIR, "eval_prompt.txt")


# Logging configuration
LOG_LEVEL = "DEBUG"                # Root log level (DEBUG, INFO, WARNING, ERROR)
LOG_FILE = "logs/orchestrator.log"  # File to write structured logs to
