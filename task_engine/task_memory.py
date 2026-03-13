from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Iterable, List, Optional

from core.models import Task, TaskStatus


class TaskMemory:
    def __init__(self) -> None:
        self._tasks: Dict[str, Task] = {}
        self._events: List[dict] = []

    def store_task(self, task: Task) -> None:
        self._tasks[task.task_id] = task

    def get_task(self, task_id: str) -> Task:
        return self._tasks[task_id]

    def maybe_task(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def all_tasks(self, goal_id: Optional[str] = None) -> Iterable[Task]:
        tasks = self._tasks.values()
        if goal_id is None:
            return list(tasks)
        return [task for task in tasks if task.goal_id == goal_id]

    def update_status(self, task_id: str, status: TaskStatus, progress: Optional[float] = None) -> None:
        task = self._tasks[task_id]
        task.status = status
        if progress is not None:
            task.progress = progress

    def append_event(self, event: dict) -> None:
        self._events.append(event)

    def task_snapshot(self, goal_id: str) -> List[dict]:
        return [asdict(task) for task in self.all_tasks(goal_id)]

    def completion_ratio(self, goal_id: str) -> float:
        tasks = list(self.all_tasks(goal_id))
        if not tasks:
            return 0.0
        completed = sum(1 for task in tasks if task.status == TaskStatus.COMPLETED)
        return completed / len(tasks)
