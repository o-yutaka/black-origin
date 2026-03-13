from __future__ import annotations

import uuid
from typing import Iterable, List

from core.models import Goal


class GoalGenerator:
    def create_goal(self, title: str, description: str, success_criteria: Iterable[str] | None = None) -> Goal:
        criteria: List[str] = list(success_criteria or [])
        return Goal(
            goal_id=f"goal-{uuid.uuid4().hex[:8]}",
            title=title,
            description=description,
            success_criteria=criteria,
        )
