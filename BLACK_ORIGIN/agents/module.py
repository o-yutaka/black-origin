from __future__ import annotations

from typing import List

from BLACK_ORIGIN.common import ModuleBase, Signal
from BLACK_ORIGIN.agents.agent_swarm_controller import AgentSwarmController
from BLACK_ORIGIN.kernel.communication import EventBus
from BLACK_ORIGIN.kernel.runtime import GoalEngine, TaskEngine


class AgentsModule(ModuleBase):
    def __init__(self):
        super().__init__("agents")
        self.event_bus = EventBus()
        self.task_engine = TaskEngine()
        self.goal_engine = GoalEngine()
        self.swarm = AgentSwarmController(event_bus=self.event_bus, task_engine=self.task_engine)

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            goal = payload.get("goal", "autonomous-reasoning")
            self.goal_engine.add_goal(goal, priority=0.8)
            task_type = "plan" if signal.stage in {"reason", "decide"} else "analyze"
            self.swarm.submit_task({"type": task_type, "goal": goal, "stage": signal.stage})
            results = self.swarm.run_once()
            payload["agents"] = {
                "status": "processed",
                "executions": results,
                "goals": len(self.goal_engine.goals),
            }
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.03))
        return enriched
