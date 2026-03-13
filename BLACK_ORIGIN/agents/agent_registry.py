from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable

from BLACK_ORIGIN.agents.agent_base import AgentBase


@dataclass
class AgentRegistry:
    _agents: Dict[str, AgentBase] = field(default_factory=dict)

    def register(self, agent: AgentBase) -> None:
        self._agents[agent.name] = agent

    def get(self, name: str) -> AgentBase | None:
        return self._agents.get(name)

    def all(self) -> Iterable[AgentBase]:
        return self._agents.values()
