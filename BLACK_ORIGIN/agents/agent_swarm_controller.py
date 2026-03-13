from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from BLACK_ORIGIN.agents.agent_base import AgentBase
from BLACK_ORIGIN.agents.agent_capabilities import AGENT_CAPABILITIES
from BLACK_ORIGIN.agents.agent_registry import AgentRegistry
from BLACK_ORIGIN.agents.agent_router import AgentRouter
from BLACK_ORIGIN.kernel.communication import EventBus
from BLACK_ORIGIN.kernel.runtime import TaskEngine


@dataclass
class AgentSwarmController:
    event_bus: EventBus
    task_engine: TaskEngine

    def __post_init__(self) -> None:
        self.registry = AgentRegistry()
        for name, capabilities in AGENT_CAPABILITIES.items():
            self.registry.register(AgentBase(name=name, capabilities=capabilities, event_bus=self.event_bus))
        self.router = AgentRouter(registry=self.registry)

    def submit_task(self, task: Dict[str, Any]) -> str:
        task_id = self.task_engine.add_task(name=task.get("type", "generic"), payload=task)
        self.event_bus.publish("swarm.task_submitted", {"task_id": task_id, "task": task}, source="swarm")
        return task_id

    def run_once(self) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for task in self.task_engine.ready_tasks():
            assignments = self.router.route(task.payload)
            for agent_name in assignments:
                agent = self.registry.get(agent_name)
                if not agent:
                    continue
                result = agent.execute(task.payload)
                result["task_id"] = task.task_id
                results.append(result)
            self.task_engine.mark_done(task.task_id)
            self.event_bus.publish("swarm.task_completed", {"task_id": task.task_id}, source="swarm")
        return results
