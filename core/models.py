from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class GoalStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    ASSIGNED = "assigned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True)
class Goal:
    goal_id: str
    title: str
    description: str
    success_criteria: List[str] = field(default_factory=list)
    status: GoalStatus = GoalStatus.PENDING
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Task:
    task_id: str
    goal_id: str
    title: str
    description: str
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    progress: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class GoalEvaluation:
    goal_id: str
    score: float
    passed: bool
    summary: str
    details: Dict[str, Any] = field(default_factory=dict)
