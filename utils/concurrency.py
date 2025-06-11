import asyncio
from typing import List, Any, Coroutine

from utils.logging import log_error

async def run_parallel(coros: List[Coroutine], limit: int) -> List[Any]:
    """
    Run a list of coroutines with a concurrency limit.

    Args:
        coros: List of coroutine objects to execute.
        limit: Maximum number of coroutines to run concurrently.

    Returns:
        List of results corresponding to each coroutine, in the same order.

    Raises:
        Exception: Propagates the first exception encountered.
    """
    semaphore = asyncio.Semaphore(limit)

    async def sem_task(coro):
        async with semaphore:
            try:
                return await coro
            except Exception as e:
                # Log and re-raise to let gather handle it
                log_error(f"Subtask error: {e}")
                raise

    # Gather will cancel all on first exception by default
    return await asyncio.gather(*(sem_task(c) for c in coros))
