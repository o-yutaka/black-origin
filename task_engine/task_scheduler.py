from __future__ import annotations

from task_engine.task_executor import TaskExecutor
from task_engine.task_graph import TaskGraph


class TaskScheduler:
    def __init__(self, graph: TaskGraph, executor: TaskExecutor) -> None:
        self._graph = graph
        self._executor = executor

    def run_ready(self) -> int:
        ran = 0
        for task in self._graph.ready_tasks():
            self._executor.execute(task.task_id)
            self._graph.mark_completed(task.task_id)
            ran += 1
        return ran

    def run_until_done(self) -> None:
        while self.run_ready() > 0:
            continue
