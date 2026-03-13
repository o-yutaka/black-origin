from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List


def build_memory_index(memories: Iterable[Dict[str, object]]) -> Dict[str, List[int]]:
    index: Dict[str, List[int]] = defaultdict(list)
    for i, memory in enumerate(memories):
        for token in str(memory.get("fact", "")).lower().split():
            index[token].append(i)
    return dict(index)
