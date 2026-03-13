from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .event_bus import Event, EventBus


@dataclass(slots=True)
class Agent:
    """Subsystem worker that communicates via the event bus."""

    name: str
    bus: EventBus

    def register(self) -> None:
        self.bus.subscribe(f"agent.{self.name}.inbox", self.on_message)

    async def send(self, target: str, message: dict[str, Any]) -> None:
        await self.bus.publish(
            Event(
                topic=f"agent.{target}.inbox",
                payload={"from": self.name, "message": message},
                source=self.name,
            )
        )

    async def on_message(self, event: Event) -> None:
        payload = event.payload
        response = {
            "ack": True,
            "received_from": payload.get("from"),
            "original_message": payload.get("message"),
        }
        await self.bus.publish(
            Event(topic="agent.messages", payload=response, source=self.name)
        )
