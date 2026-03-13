from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List


def index_knowledge(entities: Iterable[str], relations: Iterable[tuple[str, str, str]]) -> Dict[str, List[str]]:
    index: Dict[str, List[str]] = defaultdict(list)
    relation_list = list(relations)
    for entity in entities:
        for left, relation, right in relation_list:
            if entity in (left, right):
                index[entity].append(f"{left}:{relation}:{right}")
    return dict(index)


def run_knowledge_index(context: Dict[str, object]) -> Dict[str, object]:
    result = dict(context)
    index = index_knowledge(result.get("entities", []), result.get("relations", []))
    result["knowledge_index"] = {"index": index, "indexed_entities": len(index)}
    return result
