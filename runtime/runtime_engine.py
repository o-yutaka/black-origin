from __future__ import annotations

from typing import Iterable

from core.models import Goal, GoalEvaluation
from goal_engine.goal_evaluator import GoalEvaluator
from goal_engine.goal_generator import GoalGenerator
from goal_engine.goal_memory import GoalMemory
from goal_engine.goal_scheduler import GoalScheduler
from runtime.agent_messaging import Agent, AgentMessenger
from runtime.event_bus import EventBus
from task_engine.task_executor import TaskExecutor
from task_engine.task_manager import TaskManager
from task_engine.task_memory import TaskMemory
from task_engine.task_planner import TaskPlanner


class RuntimeEngine:
    """Wires goal + task engines with event bus and agent messaging."""

    def __init__(self) -> None:
        self.event_bus = EventBus()
        self.task_memory = TaskMemory()
        self.goal_memory = GoalMemory()

        self.agent_messenger = AgentMessenger(self.event_bus)
        self.task_executor = TaskExecutor(self.event_bus, self.task_memory, self.agent_messenger)
        self.task_manager = TaskManager(TaskPlanner(), self.task_memory, self.task_executor, self.event_bus)

        self.goal_generator = GoalGenerator()
        self.goal_evaluator = GoalEvaluator(self.task_memory)
        self.goal_scheduler = GoalScheduler(self.goal_memory, self.task_manager, self.goal_evaluator)

    def register_agents(self, agents: Iterable[Agent]) -> None:
        for agent in agents:
            self.agent_messenger.register_agent(agent)

    def create_goal(self, title: str, description: str, success_criteria: Iterable[str] | None = None) -> Goal:
        goal = self.goal_generator.create_goal(title, description, success_criteria)
        self.goal_memory.store_goal(goal)
        self.event_bus.publish("goal.created", {"goal_id": goal.goal_id, "title": goal.title})
        return goal

    def run_goal(self, goal_id: str) -> GoalEvaluation:
        self.goal_scheduler.schedule(goal_id)
        evaluation = self.goal_memory.get_evaluation(goal_id)
        self.event_bus.publish("goal.evaluated", {"goal_id": goal_id, "score": evaluation.score, "passed": evaluation.passed})
        return evaluation
