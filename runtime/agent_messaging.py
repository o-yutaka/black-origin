from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional

from runtime.event_bus import EventBus


@dataclass(slots=True)
class Agent:
    agent_id: str
    capability: str
    handler: Optional[Callable[[dict], None]] = None


class AgentMessenger:
    """Routes task assignments to agents and emits messaging events."""

    def __init__(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self._agents: Dict[str, Agent] = {}

    def register_agent(self, agent: Agent) -> None:
        self._agents[agent.agent_id] = agent
        self._event_bus.publish("agent.registered", {"agent_id": agent.agent_id, "capability": agent.capability})

    def find_agent(self, capability: str) -> Optional[str]:
        for agent in self._agents.values():
            if agent.capability == capability:
                return agent.agent_id
        return None

    def send_task(self, agent_id: str, message: dict) -> None:
        agent = self._agents[agent_id]
        self._event_bus.publish("agent.message.sent", {"agent_id": agent_id, "message": message})
        if agent.handler:
            agent.handler(message)
