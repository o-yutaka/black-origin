from __future__ import annotations

import asyncio
from typing import Any

from .agent import Agent
from .event_bus import Event, EventBus
from .signals import SignalSystem


class RuntimeEngine:
    """Continuous event-driven intelligence loop for BLACK ORIGIN."""

    def __init__(self, tick_interval: float = 1.0) -> None:
        self.bus = EventBus()
        self.tick_interval = tick_interval
        self._running = False
        self._tasks: list[asyncio.Task[Any]] = []
        self._signal_system = SignalSystem(self.stop)

        self._agents = {
            "orchestrator": Agent("orchestrator", self.bus),
            "observer": Agent("observer", self.bus),
        }

        self.bus.subscribe("runtime.tick", self._orchestrate)
        self.bus.subscribe("agent.messages", self._collect_agent_updates)

    def setup(self) -> None:
        for agent in self._agents.values():
            agent.register()

    async def _orchestrate(self, event: Event) -> None:
        await self._agents["orchestrator"].send(
            "observer",
            {
                "type": "heartbeat",
                "sequence": event.payload["sequence"],
                "status": "runtime-active",
            },
        )

    async def _collect_agent_updates(self, event: Event) -> None:
        print(f"[agent-update] {event.source}: {event.payload}")

    async def _tick_loop(self) -> None:
        sequence = 0
        while self._running:
            await self.bus.publish(
                Event(topic="runtime.tick", payload={"sequence": sequence}, source="runtime")
            )
            sequence += 1
            await asyncio.sleep(self.tick_interval)

    async def run(self) -> None:
        self.setup()
        self._signal_system.install()
        self._running = True
        self._tasks = [
            asyncio.create_task(self.bus.run(), name="event-bus"),
            asyncio.create_task(self._tick_loop(), name="runtime-loop"),
        ]

        try:
            await asyncio.gather(*self._tasks)
        except asyncio.CancelledError:
            pass

    def stop(self) -> None:
        if not self._running:
            return
        self._running = False
        self.bus.stop()
        for task in self._tasks:
            task.cancel()
