# LLMTreeReasoning

A modular, recursive multi-agent LLM orchestration framework built on Ollama’s `llama3` model.
It decomposes complex user goals into subtasks, explores each in parallel, critically evaluates branch outputs, synthesizes a final plan, and scaffolds a codebase—all driven by purpose-specific LLM “agents.”

---

## 🚀 Features

* **Prompt Filtering**: Cleans, deduplicates, and reformats the raw user prompt for clarity.
* **Meta Decomposition**: Decides if the task is multi-step and enumerates immediate subtasks & alternative approaches.
* **Recursive Orchestration**: Automatically recurses up to 3 levels—subtasks of subtasks—before falling back to the explorer.
* **Parallel Exploration**: Spawns multiple `ExplorerAgent` instances to outline implementation steps for each subtask concurrently.
* **Critical Evaluation**: `EvaluatorAgent` generates structured feedback and suggestions for each branch.
* **Synthesis**: `SynthesizerAgent` merges branches + feedback into a cohesive, final action plan.
* **Design Scaffolding**: `DesignAgent` converts the final plan into a JSON file/folder tree for code generation.
* **Configurable**: All core limits, model settings, and prompt paths are centralized in `config.py`.
* **Test Suite**: Unit tests validate each agent’s parsing logic and end-to-end flow.

---

## 📦 Prerequisites

* **macOS / Linux**
* **Python 3.10+**
* **Ollama CLI** (with `llama3` model downloaded)

  ```bash
  # macOS (Homebrew)
  brew install ollama
  ollama pull llama3
  ```

---

## 🛠️ Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/your-org/LLMTreeReasoning.git
   cd LLMTreeReasoning
   ```

2. **Create & activate a virtualenv**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   export PYTHONPATH="$(pwd)"
   ```

4. *(Optional)* Install in editable mode for easy imports:

   ```bash
   pip install -e .
   ```

---

## ⚙️ Configuration

All tunable parameters and prompt file paths live in `config.py`:

| Key                   | Description                                    | Default                        |
| --------------------- | ---------------------------------------------- | ------------------------------ |
| `LLM_MODEL`           | Ollama model name                              | `"llama3"`                     |
| `MAX_PARALLEL_TASKS`  | Explorer parallelism limit                     | `5`                            |
| `MAX_RECURSION_DEPTH` | Recursive decomposition depth                  | `3`                            |
| `TIMEOUT_SEC`         | Ollama CLI timeout per call (seconds)          | `30`                           |
| `MAX_RETRIES`         | Retries for Ollama CLI failures                | `3`                            |
| `META_PROMPT_PATH`    | File path to meta-agent prompt template        | `"prompts/meta_prompt.txt"`    |
| `EXPLORE_PROMPT_PATH` | File path to explorer-agent prompt template    | `"prompts/explore_prompt.txt"` |
| `EVAL_PROMPT_PATH`    | File path to evaluator-agent prompt template   | `"prompts/eval_prompt.txt"`    |
| `SYNTH_PROMPT_PATH`   | File path to synthesizer-agent prompt template | `"prompts/synth_prompt.txt"`   |
| `FILTER_PROMPT_PATH`  | File path to prompt-filter prompt template     | `"prompts/filter_prompt.txt"`  |

Adjust these before running to point to your custom templates or change timeouts.

---

## 🏗️ Project Layout

```
LLMTreeReasoning/
├── orchestrator.py            # Entry point & high-level orchestration
├── config.py                  # Central settings & paths
├── requirements.txt           # Python deps
│
├── prompts/                   # LLM prompt templates
│   ├── filter_prompt.txt
│   ├── meta_prompt.txt
│   ├── explore_prompt.txt
│   ├── eval_prompt.txt
│   ├── synth_prompt.txt
│
├── modules/                   # Agent implementations
│   ├── prompt_filter_agent.py
│   ├── meta_agent.py
│   ├── explorer_agent.py
│   ├── evaluator_agent.py
│   ├── synthesizer_agent.py
│   └── design_agent.py
│
├── schemas/                   # Pydantic models for structured responses
│   ├── task_models.py
│   └── response_models.py
│
├── utils/                     # Helpers & wrappers
│   ├── llm_client.py          # Ollama CLI wrapper with retries
│   ├── parser.py              # JSON/bullet-list parsing into models
│   ├── logging.py             # Structured logging setup
│   └── concurrency.py         # Semaphore-based parallel runner
│
└── tests/                     # pytest suite for each agent
    ├── test_prompt_filter_agent.py
    ├── test_meta_agent.py
    ├── test_explorer_agent.py
    └── test_evaluator_agent.py
```

---

## ▶️ Usage

Run the orchestrator with your desired user goal:

```bash
python orchestrator.py "build a to-do list app"
```

* **Step 0**: `PromptFilterAgent` cleans your raw text.
* **Step 1**: `MetaAgent` decides single vs. multi-step and lists subtasks.
* **Step 2**: Recurses (up to depth 3) or directly spins up `ExplorerAgent` instances.
* **Step 3**: `EvaluatorAgent` generates critical feedback & suggestions.
* **Step 4**: `SynthesizerAgent` merges everything into a final plan.
* **Step 5**: `DesignAgent` outputs a JSON tree of files/folders for implementation.


---

## 🔧 Extending & Customizing

1. **Add a new agent**

   * Create `modules/your_agent.py` with a `.run(...)` method.
   * Add a prompt template in `prompts/`.
   * Wire into `orchestrator.py` where appropriate.

2. **Adjust recursion or parallelism**

   * Tweak `MAX_RECURSION_DEPTH` and `MAX_PARALLEL_TASKS` in `config.py`.

3. **Swap LLM backend**

   * Implement a new client in `utils/llm_client.py` (e.g., HTTP API).
   * Point your agents at that client instead of `OllamaClient`.

---

## ✅ Testing

Ensure your virtualenv is active and run:

```bash
pytest -q
```

All tests validate:

* Proper parsing of LLM JSON into Pydantic models.
* Correct handling of optional fields (`dependencies`, `feedback`).
* Stubbed LLM responses via monkeypatching `OllamaClient.send`.

---

## 🚧 Troubleshooting

* **`unknown flag --prompt`**: Ensure `llm_client.py` invokes `ollama run <model> <prompt>` positionally.
* **Module import errors**: Run tests from the repo root and/or install in editable mode (`pip install -e .`).
* **Timeouts / non-zero exit codes**: Adjust `TIMEOUT_SEC` and `MAX_RETRIES` in `config.py`.

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/XYZ`)
3. Commit your changes (`git commit -am "Add XYZ"`)
4. Push to your fork (`git push origin feature/XYZ`)
5. Open a Pull Request

Please include tests for any new agents or parsing logic.

---

## 📄 License

This project is released under the **MIT License**. See `LICENSE` for details.
