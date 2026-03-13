from __future__ import annotations

from collections import defaultdict, deque
from typing import DefaultDict, Dict, Iterable, List, Set

from core.models import Task, TaskStatus


class TaskGraph:
    def __init__(self) -> None:
        self._tasks: Dict[str, Task] = {}
        self._children: DefaultDict[str, Set[str]] = defaultdict(set)

    def add_task(self, task: Task) -> None:
        self._tasks[task.task_id] = task
        for dependency in task.dependencies:
            self._children[dependency].add(task.task_id)

    def tasks(self) -> Iterable[Task]:
        return self._tasks.values()

    def mark_completed(self, task_id: str) -> None:
        self._tasks[task_id].status = TaskStatus.COMPLETED

    def ready_tasks(self) -> List[Task]:
        ready = []
        for task in self._tasks.values():
            if task.status not in {TaskStatus.PENDING, TaskStatus.READY}:
                continue
            if all(self._tasks[d].status == TaskStatus.COMPLETED for d in task.dependencies):
                task.status = TaskStatus.READY
                ready.append(task)
        return ready

    def topological_sort(self) -> List[str]:
        indegree = {task_id: len(task.dependencies) for task_id, task in self._tasks.items()}
        queue = deque([task_id for task_id, degree in indegree.items() if degree == 0])
        order = []
        while queue:
            current = queue.popleft()
            order.append(current)
            for child in self._children.get(current, set()):
                indegree[child] -= 1
                if indegree[child] == 0:
                    queue.append(child)
        if len(order) != len(self._tasks):
            raise ValueError("Cycle detected in task graph")
        return order
