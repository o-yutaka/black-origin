from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from threading import RLock
from typing import Any, Callable, DefaultDict, Dict, List


EventHandler = Callable[[Dict[str, Any]], None]


@dataclass
class Event:
    topic: str
    payload: Dict[str, Any]
    source: str = "unknown"


@dataclass
class EventBus:
    """In-memory pub/sub bus used by core engines and agent swarm."""

    _subscribers: DefaultDict[str, List[EventHandler]] = field(default_factory=lambda: defaultdict(list))
    _history: List[Event] = field(default_factory=list)
    _lock: RLock = field(default_factory=RLock)

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        with self._lock:
            self._subscribers[topic].append(handler)

    def publish(self, topic: str, payload: Dict[str, Any], source: str = "unknown") -> None:
        event = Event(topic=topic, payload=payload, source=source)
        with self._lock:
            self._history.append(event)
            handlers = list(self._subscribers.get(topic, [])) + list(self._subscribers.get("*", []))

        for handler in handlers:
            handler({"topic": topic, "payload": payload, "source": source})

    def history(self, topic: str | None = None) -> List[Dict[str, Any]]:
        with self._lock:
            events = [event for event in self._history if topic is None or event.topic == topic]
        return [{"topic": e.topic, "payload": e.payload, "source": e.source} for e in events]


def run_communication(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    bus = result.setdefault("event_bus", EventBus())
    bus.publish("communication.ready", {"status": "ok"}, source="communication")
    result["communication"] = "ok"
    return result
