from __future__ import annotations

from collections import deque
from typing import Any, Deque, Dict, List


class ContextMemory:
    def __init__(self, window: int = 8):
        self.window = window
        self.buffer: Deque[Dict[str, Any]] = deque(maxlen=window)

    def push(self, item: Dict[str, Any]) -> None:
        self.buffer.append(item)

    def snapshot(self) -> List[Dict[str, Any]]:
        return list(self.buffer)


def run_context_memory(context: Dict[str, Any], memory: ContextMemory | None = None) -> Dict[str, Any]:
    result = dict(context)
    context_memory = memory or ContextMemory()
    frame = {"stage": result.get("stage", "unknown"), "signal": result.get("signal", {})}
    context_memory.push(frame)
    result["context_memory"] = {"window": context_memory.window, "active_frames": len(context_memory.snapshot())}
    return result
