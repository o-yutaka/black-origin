from __future__ import annotations

from core.models import Goal, GoalEvaluation
from task_engine.task_memory import TaskMemory


class GoalEvaluator:
    def __init__(self, task_memory: TaskMemory) -> None:
        self._task_memory = task_memory

    def evaluate(self, goal: Goal) -> GoalEvaluation:
        completion = self._task_memory.completion_ratio(goal.goal_id)
        passed = completion >= 1.0
        summary = "Goal completed successfully" if passed else "Goal is incomplete"
        details = {
            "completion_ratio": completion,
            "task_snapshot": self._task_memory.task_snapshot(goal.goal_id),
            "criteria": goal.success_criteria,
        }
        return GoalEvaluation(goal_id=goal.goal_id, score=completion, passed=passed, summary=summary, details=details)
