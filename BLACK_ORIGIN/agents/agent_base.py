from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from BLACK_ORIGIN.kernel.communication import EventBus


@dataclass
class AgentBase:
    name: str
    capabilities: List[str]
    event_bus: EventBus
    memory: List[Dict[str, Any]] = field(default_factory=list)

    def can_handle(self, task_type: str) -> bool:
        return task_type in self.capabilities

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        result = {
            "agent": self.name,
            "task_type": task.get("type", "unknown"),
            "summary": f"{self.name} processed task",
            "confidence": 0.55,
        }
        self.memory.append(result)
        self.event_bus.publish("agent.executed", result, source=self.name)
        return result
