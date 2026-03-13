from __future__ import annotations

import uuid
from typing import List

from core.models import Goal, Task


class TaskPlanner:
    """Heuristic planner that decomposes a goal into a small dependency chain."""

    def decompose(self, goal: Goal) -> List[Task]:
        chunks = [item.strip(" -") for item in goal.description.split(".") if item.strip()]
        if not chunks:
            chunks = [goal.title]

        tasks: List[Task] = []
        previous_task_id: str | None = None
        for index, chunk in enumerate(chunks, start=1):
            task_id = f"task-{uuid.uuid4().hex[:8]}"
            dependencies = [previous_task_id] if previous_task_id else []
            task = Task(
                task_id=task_id,
                goal_id=goal.goal_id,
                title=f"{goal.title} - Step {index}",
                description=chunk,
                dependencies=dependencies,
                metadata={"capability": "general"},
            )
            tasks.append(task)
            previous_task_id = task_id
        return tasks
