from __future__ import annotations

from typing import Dict, Optional

from core.models import Goal, GoalEvaluation, GoalStatus


class GoalMemory:
    def __init__(self) -> None:
        self._goals: Dict[str, Goal] = {}
        self._evaluations: Dict[str, GoalEvaluation] = {}

    def store_goal(self, goal: Goal) -> None:
        self._goals[goal.goal_id] = goal

    def get_goal(self, goal_id: str) -> Goal:
        return self._goals[goal_id]

    def maybe_goal(self, goal_id: str) -> Optional[Goal]:
        return self._goals.get(goal_id)

    def set_status(self, goal_id: str, status: GoalStatus) -> None:
        self._goals[goal_id].status = status

    def store_evaluation(self, evaluation: GoalEvaluation) -> None:
        self._evaluations[evaluation.goal_id] = evaluation

    def get_evaluation(self, goal_id: str) -> GoalEvaluation:
        return self._evaluations[goal_id]
