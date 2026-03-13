from __future__ import annotations

from core.models import GoalStatus
from goal_engine.goal_evaluator import GoalEvaluator
from goal_engine.goal_memory import GoalMemory
from task_engine.task_manager import TaskManager


class GoalScheduler:
    def __init__(self, goal_memory: GoalMemory, task_manager: TaskManager, evaluator: GoalEvaluator) -> None:
        self._goal_memory = goal_memory
        self._task_manager = task_manager
        self._evaluator = evaluator

    def schedule(self, goal_id: str) -> None:
        goal = self._goal_memory.get_goal(goal_id)
        self._goal_memory.set_status(goal_id, GoalStatus.ACTIVE)
        self._task_manager.execute_goal(goal)
        evaluation = self._evaluator.evaluate(goal)
        self._goal_memory.store_evaluation(evaluation)
        self._goal_memory.set_status(goal_id, GoalStatus.COMPLETED if evaluation.passed else GoalStatus.FAILED)
