from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, DefaultDict, Dict, List


@dataclass(slots=True)
class Event:
    topic: str
    payload: Dict[str, Any]


EventHandler = Callable[[Event], None]


class EventBus:
    """Simple in-process pub/sub event bus."""

    def __init__(self) -> None:
        self._handlers: DefaultDict[str, List[EventHandler]] = defaultdict(list)

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        self._handlers[topic].append(handler)

    def publish(self, topic: str, payload: Dict[str, Any]) -> None:
        event = Event(topic=topic, payload=payload)
        for handler in list(self._handlers.get(topic, [])):
            handler(event)
