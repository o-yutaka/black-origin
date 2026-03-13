from __future__ import annotations

from core.models import Goal
from runtime.event_bus import EventBus
from task_engine.task_executor import TaskExecutor
from task_engine.task_graph import TaskGraph
from task_engine.task_memory import TaskMemory
from task_engine.task_planner import TaskPlanner
from task_engine.task_scheduler import TaskScheduler


class TaskManager:
    def __init__(self, planner: TaskPlanner, memory: TaskMemory, executor: TaskExecutor, event_bus: EventBus) -> None:
        self._planner = planner
        self._memory = memory
        self._executor = executor
        self._event_bus = event_bus

    def build_graph(self, goal: Goal) -> TaskGraph:
        tasks = self._planner.decompose(goal)
        graph = TaskGraph()
        for task in tasks:
            self._memory.store_task(task)
            graph.add_task(task)
            self._event_bus.publish("task.created", {"task_id": task.task_id, "goal_id": goal.goal_id})
        return graph

    def execute_goal(self, goal: Goal) -> TaskGraph:
        graph = self.build_graph(goal)
        scheduler = TaskScheduler(graph, self._executor)
        scheduler.run_until_done()
        return graph
