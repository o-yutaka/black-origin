from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple


@dataclass
class GraphStore:
    nodes: Set[str] = field(default_factory=set)
    edges: List[Tuple[str, str, str]] = field(default_factory=list)

    def add_entities(self, entities: List[str]) -> None:
        self.nodes.update(entities)

    def add_relations(self, relations: List[Tuple[str, str, str]]) -> None:
        self.edges.extend(relations)

    def neighbors(self, node: str) -> List[str]:
        return [right for left, _, right in self.edges if left == node] + [left for left, _, right in self.edges if right == node]


def run_graph_store(context: Dict[str, object], store: GraphStore | None = None) -> Dict[str, object]:
    result = dict(context)
    graph_store = store or GraphStore()
    entities = result.get("entities", [])
    relations = result.get("relations", [])
    graph_store.add_entities(list(entities))
    graph_store.add_relations(list(relations))
    result["graph_store"] = {"node_count": len(graph_store.nodes), "edge_count": len(graph_store.edges)}
    return result
