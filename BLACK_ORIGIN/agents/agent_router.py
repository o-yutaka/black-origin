from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from BLACK_ORIGIN.agents.agent_registry import AgentRegistry


@dataclass
class AgentRouter:
    registry: AgentRegistry

    def route(self, task: Dict[str, str]) -> List[str]:
        task_type = task.get("type", "")
        candidates = [agent.name for agent in self.registry.all() if agent.can_handle(task_type)]
        if candidates:
            return candidates
        return ["analysis_agent"] if self.registry.get("analysis_agent") else []
