from __future__ import annotations

from typing import Dict, List

from BLACK_ORIGIN.memory.memory_index import build_memory_index


def retrieve_memories(query: str, memories: List[Dict[str, object]]) -> List[Dict[str, object]]:
    index = build_memory_index(memories)
    hits = set()
    for token in query.lower().split():
        hits.update(index.get(token, []))
    return [memories[i] for i in sorted(hits)]
