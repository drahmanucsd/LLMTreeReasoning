# config.py

# LLM model configuration
LLM_MODEL = "llama3"            # Ollama model to use for all agents
MODEL_TEMPERATURE = 0.7           # Sampling temperature for LLM outputs
MAX_TOKENS = 2048                 # Maximum tokens to generate per request
TIMEOUT_SEC = 30                  # Timeout (in seconds) for LLM calls
MAX_RETRIES = 3                   # Number of retry attempts on failure

# Concurrency settings
MAX_PARALLEL_TASKS = 5            # Maximum number of concurrent explorer agents

# Prompt file paths
META_PROMPT_PATH = "prompts/meta_prompt.txt"
EXPLORE_PROMPT_PATH = "prompts/explore_prompt.txt"
EVAL_PROMPT_PATH = "prompts/eval_prompt.txt"

# Logging configuration
LOG_LEVEL = "DEBUG"                # Root log level (DEBUG, INFO, WARNING, ERROR)
LOG_FILE = "logs/orchestrator.log"  # File to write structured logs to
