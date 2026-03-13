from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class LongTermMemoryStore:
    entries: List[Dict[str, Any]] = field(default_factory=list)

    def remember(self, item: Dict[str, Any]) -> None:
        self.entries.append(item)

    def recent(self, limit: int = 5) -> List[Dict[str, Any]]:
        return self.entries[-limit:]


def run_long_term_memory(context: Dict[str, Any], store: LongTermMemoryStore | None = None) -> Dict[str, Any]:
    result = dict(context)
    memory_store = store or LongTermMemoryStore()
    item = {"fact": result.get("fact", ""), "importance": float(result.get("importance", 0.5))}
    memory_store.remember(item)
    result["long_term_memory"] = {"stored": item, "total_entries": len(memory_store.entries)}
    return result
