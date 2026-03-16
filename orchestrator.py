"""Simple asynchronous API orchestrator.

This module defines Task and Workflow classes that can be used to build a directed
acyclic graph (DAG) of asynchronous tasks.  Each task can depend on the results of
other tasks.  The example at the bottom of this file illustrates fetching data from
mock APIs, enriching it, and posting the result to another service.
"""

from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable, Dict, List, Optional


class Task:
    """Represents a unit of work in the orchestrator."""

    def __init__(
        self,
        name: str,
        coro: Callable[..., Awaitable[Any]],
        dependencies: Optional[List["Task"]] = None,
    ) -> None:
        self.name = name
        self.coro = coro
        self.dependencies = dependencies or []
        self.result: Any = None

    async def run(self) -> Any:
        """Run the task after ensuring dependencies have completed."""
        # Wait on dependencies
        for dep in self.dependencies:
            await dep.run()
        if self.result is not None:
            return self.result
        self.result = await self.coro(*(dep.result for dep in self.dependencies))
        return self.result


class Workflow:
    """Execute a collection of tasks according to their dependencies."""

    def __init__(self, tasks: List[Task]) -> None:
        self.tasks = tasks

    async def execute(self) -> Dict[str, Any]:
        """Execute all tasks and return a mapping of task names to results."""
        results: Dict[str, Any] = {}
        for task in self.tasks:
            results[task.name] = await task.run()
        return results


# Mock API functions for the example

async def fetch_user() -> Dict[str, Any]:
    await asyncio.sleep(0.1)
    return {"id": 1, "name": "Jane Doe", "email": "jane@example.com"}


async def enrich_user(user: Dict[str, Any]) -> Dict[str, Any]:
    await asyncio.sleep(0.1)
    # Add a fake enrichment field
    user["loyalty_score"] = 0.9
    return user


async def post_billing(user: Dict[str, Any]) -> str:
    await asyncio.sleep(0.1)
    # Simulate posting to a billing system and returning an acknowledgement
    return f"Billing record created for {user['name']}"


async def main() -> None:
    """Run the example workflow."""
    # Define tasks and their dependencies
    t_fetch = Task(name="fetch_user", coro=lambda: fetch_user())
    t_enrich = Task(name="enrich_user", coro=enrich_user, dependencies=[t_fetch])
    t_billing = Task(name="post_billing", coro=post_billing, dependencies=[t_enrich])
    wf = Workflow([t_fetch, t_enrich, t_billing])
    results = await wf.execute()
    for name, result in results.items():
        print(f"{name}: {result}")


if __name__ == "__main__":
    asyncio.run(main())