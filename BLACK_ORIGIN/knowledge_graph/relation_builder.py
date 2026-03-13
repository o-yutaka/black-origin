from __future__ import annotations

from itertools import combinations
from typing import Dict, List, Tuple


def build_relations(entities: List[str]) -> List[Tuple[str, str, str]]:
    relations: List[Tuple[str, str, str]] = []
    for left, right in combinations(entities, 2):
        relations.append((left, "co_occurs_with", right))
    return relations


def run_relation_builder(context: Dict[str, object]) -> Dict[str, object]:
    result = dict(context)
    entities = result.get("entities", [])
    if isinstance(entities, dict):
        entities = entities.get("entities", [])
    relations = build_relations(list(entities))
    result["relation_builder"] = {"relations": relations, "count": len(relations)}
    return result
