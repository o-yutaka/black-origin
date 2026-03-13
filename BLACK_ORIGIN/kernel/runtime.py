from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from BLACK_ORIGIN.kernel.communication import EventBus


@dataclass
class Task:
    task_id: str
    name: str
    payload: Dict[str, Any]
    status: str = "pending"
    depends_on: List[str] = field(default_factory=list)


@dataclass
class TaskEngine:
    tasks: Dict[str, Task] = field(default_factory=dict)

    def add_task(self, name: str, payload: Dict[str, Any], depends_on: List[str] | None = None) -> str:
        task_id = f"task-{len(self.tasks) + 1}"
        self.tasks[task_id] = Task(task_id=task_id, name=name, payload=payload, depends_on=depends_on or [])
        return task_id

    def ready_tasks(self) -> List[Task]:
        done = {task_id for task_id, task in self.tasks.items() if task.status == "done"}
        return [
            task
            for task in self.tasks.values()
            if task.status == "pending" and all(dep in done for dep in task.depends_on)
        ]

    def mark_done(self, task_id: str) -> None:
        if task_id in self.tasks:
            self.tasks[task_id].status = "done"


@dataclass
class GoalEngine:
    goals: List[Dict[str, Any]] = field(default_factory=list)

    def add_goal(self, description: str, priority: float = 0.5) -> None:
        self.goals.append({"description": description, "priority": priority})

    def top_goal(self) -> Dict[str, Any]:
        if not self.goals:
            return {"description": "stabilize-intelligence-loop", "priority": 0.1}
        return sorted(self.goals, key=lambda item: item["priority"], reverse=True)[0]


@dataclass
class RuntimeEngine:
    event_bus: EventBus
    task_engine: TaskEngine
    goal_engine: GoalEngine

    def tick(self, context: Dict[str, Any]) -> Dict[str, Any]:
        top_goal = self.goal_engine.top_goal()
        ready = self.task_engine.ready_tasks()
        self.event_bus.publish("runtime.tick", {"goal": top_goal, "ready_tasks": len(ready)}, source="runtime")
        return {
            "goal": top_goal,
            "ready_tasks": [task.task_id for task in ready],
            "task_count": len(self.task_engine.tasks),
        }


def run_runtime(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    event_bus = result.setdefault("event_bus", EventBus())
    task_engine = result.setdefault("task_engine", TaskEngine())
    goal_engine = result.setdefault("goal_engine", GoalEngine())
    runtime = RuntimeEngine(event_bus=event_bus, task_engine=task_engine, goal_engine=goal_engine)
    result["runtime"] = runtime.tick(result)
    return result
