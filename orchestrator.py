import sys
import asyncio
import json

from config import MAX_PARALLEL_TASKS
from modules.meta_agent import MetaAgent
from modules.explorer_agent import ExplorerAgent
from modules.evaluator_agent import EvaluatorAgent
from modules.design_agent import DesignAgent
from utils.concurrency import run_parallel
from utils.logging import log_info, log_error


def orchestrate(user_goal: str):
    """
    Core orchestration flow:
      1. Decompose goal into subtasks via MetaAgent
      2. Execute ExplorerAgent on each subtask in parallel
      3. Merge branch outputs via EvaluatorAgent
      4. Plan file structure via DesignAgent
    Returns a dict with all intermediate and final results.
    """
    async def _run():
        log_info(f"Orchestration started for goal: {user_goal}")
        try:
            # 1. Meta decomposition
            meta_agent = MetaAgent()
            meta_res = await meta_agent.run(user_goal)

            # Determine subtasks (fallback to entire goal if not multi-step)
            subtasks = meta_res.subtasks if meta_res.is_multi_step and meta_res.subtasks else [user_goal]
            log_info(f"Identified subtasks: {subtasks}")

            # 2. Parallel exploration
            explorers = [ExplorerAgent().run(task) for task in subtasks]
            explore_results = await run_parallel(explorers, limit=MAX_PARALLEL_TASKS)
            log_info(f"Explorer results collected ({len(explore_results)} branches)")

            # 3. Evaluation and merging
            evaluator = EvaluatorAgent()
            eval_res = await evaluator.run(explore_results)
            log_info("Branches merged into unified plan.")

            # 4. Design file/folder tree
            design_agent = DesignAgent()
            file_tree = design_agent.plan(eval_res.merged_plan)
            log_info("Design tree generated.")

            return {
                "meta": meta_res,
                "explore": explore_results,
                "eval": eval_res,
                "design": file_tree,
            }

        except Exception as e:
            log_error(f"Orchestration error: {e}")
            raise

    return asyncio.run(_run())


def main():
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py <user_goal>")
        sys.exit(1)

    user_goal = " ".join(sys.argv[1:])
    result = orchestrate(user_goal)

    # Display merged plan
    print("\n=== Unified Plan ===")
    for idx, step in enumerate(result["eval"].merged_plan, start=1):
        print(f"{idx}. {step}")

    # Display file structure
    print("\n=== File Structure ===")
    print(json.dumps(result["design"], indent=2))


if __name__ == "__main__":
    main()
