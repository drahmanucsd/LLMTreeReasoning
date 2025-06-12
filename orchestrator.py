import sys
import asyncio
import json

from config import MAX_PARALLEL_TASKS, MAX_RECURSION_DEPTH
from modules.meta_agent import MetaAgent
from modules.explorer_agent import ExplorerAgent
from modules.evaluator_agent import EvaluatorAgent
from modules.design_agent import DesignAgent
from modules.synthesizer_agent import SynthesizerAgent
from modules.prompt_filter_agent import PromptFilterAgent

from utils.concurrency import run_parallel
from utils.logging import log_info, log_error


# def orchestrate(user_goal: str):
def orchestrate(user_goal: str, parent_context: str = "", depth: int=0):
    """
    Core orchestration flow:
      1. Decompose goal into subtasks via MetaAgent
      2. Execute ExplorerAgent on each subtask in parallel
      3. Merge branch outputs via EvaluatorAgent
      4. Plan file structure via DesignAgent
    Returns a dict with all intermediate and final results.
    """
    if depth == 0:
        filter_agent = PromptFilterAgent()
        filtered_goal = asyncio.run(filter_agent.run(user_goal))
        return orchestrate(filtered_goal, "", 1)
    # async def _run():
    async def _run(goal, context, lvl):
        log_info(f"Orchestration started for goal: {goal} (depth={lvl})")

        try:
            # 1. Meta decomposition
            meta_agent = MetaAgent()
            meta_res = await meta_agent.run(goal, context)
            combined_context = (context + "\n" + f"User goal at depth {lvl}: {goal}").strip()


            # Determine subtasks (fallback to entire goal if not multi-step)
            subtasks = meta_res.subtasks if meta_res.is_multi_step and meta_res.subtasks else [user_goal]
            log_info(f"Identified subtasks: {subtasks}")

            if lvl < MAX_RECURSION_DEPTH and meta_res.is_multi_step and meta_res.subtasks:
                # recurse one layer deeper in parallel
                tasks = [
                    asyncio.create_task(_run(sub, combined_context, lvl+1))
                    for sub in meta_res.subtasks
                ]
                # each result is the full dict from a deeper orchestrate
                explore_results = await asyncio.gather(*tasks)
            else:
                # leaf: just run ExplorerAgent, feeding context
                explorers = [
                    ExplorerAgent().run(task, combined_context)
                    for task in (meta_res.subtasks or [goal])
                ]
                explore_results = await run_parallel(explorers, limit=MAX_PARALLEL_TASKS)

            # 3. Critique each branch (feedback + suggestions)
            eval_res = await EvaluatorAgent().run(explore_results)
            log_info("Evaluator produced feedback and suggestions.")

            # 4. Synthesize final plan from parent goal + branches + feedback
            synth_in = {
                "user_goal": user_goal,
                "branches": [br.dict() for br in explore_results],
                # "feedback":    eval_res.feedback,
                "suggestions": eval_res.suggestions,
            }
            synth_res = await SynthesizerAgent().run(synth_in)
            log_info("Synthesizer combined everything into a final plan.")

            # 5. Design file/folder tree
            file_tree = DesignAgent().plan(synth_res.merged_plan)
            log_info("Design tree generated.")

            return {
                "meta": meta_res,
                "explore": explore_results,
                "eval": eval_res,
                "synth":   synth_res,
                "design": file_tree,
            }

        except Exception as e:
            log_error(f"Orchestration error: {e}")
            raise

    # return asyncio.run(_run())
    return asyncio.run(_run(user_goal, parent_context, depth))


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
