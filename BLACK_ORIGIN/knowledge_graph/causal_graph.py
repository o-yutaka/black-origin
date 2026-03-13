from __future__ import annotations

from typing import Dict, List, Tuple


def build_causal_graph(relations: List[Tuple[str, str, str]]) -> Dict[str, List[str]]:
    graph: Dict[str, List[str]] = {}
    for source, relation, target in relations:
        if relation in {"causes", "influences", "co_occurs_with"}:
            graph.setdefault(source, []).append(target)
    return graph


def run_causal_graph(context: Dict[str, object]) -> Dict[str, object]:
    result = dict(context)
    relations = list(result.get("relations", []))
    graph = build_causal_graph(relations)
    result["causal_graph"] = {"graph": graph, "driver_count": len(graph)}
    return result
