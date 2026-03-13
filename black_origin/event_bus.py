from __future__ import annotations

import asyncio
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable

EventHandler = Callable[["Event"], Awaitable[None] | None]


@dataclass(slots=True)
class Event:
    """Single message flowing through the runtime."""

    topic: str
    payload: dict[str, Any] = field(default_factory=dict)
    source: str = "system"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class EventBus:
    """Async event bus for topic-based publish/subscribe communication."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)
        self._queue: asyncio.Queue[Event] = asyncio.Queue()
        self._running = False

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        self._handlers[topic].append(handler)

    async def publish(self, event: Event) -> None:
        await self._queue.put(event)

    async def dispatch_once(self) -> None:
        event = await self._queue.get()
        handlers = [*self._handlers.get(event.topic, []), *self._handlers.get("*", [])]
        for handler in handlers:
            result = handler(event)
            if asyncio.iscoroutine(result):
                await result
        self._queue.task_done()

    async def run(self) -> None:
        self._running = True
        while self._running:
            await self.dispatch_once()

    def stop(self) -> None:
        self._running = False
