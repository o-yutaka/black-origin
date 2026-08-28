from __future__ import annotations

from typing import Any, Iterable, List

from BLACK_ORIGIN.common import ModuleBase, Signal
from BLACK_ORIGIN.knowledge_graph.entity_extractor import extract_entities
from BLACK_ORIGIN.knowledge_graph.relation_builder import build_relations
from BLACK_ORIGIN.knowledge_graph.knowledge_index import index_knowledge
from BLACK_ORIGIN.knowledge_graph.causal_graph import build_causal_graph
from BLACK_ORIGIN.knowledge_graph.graph_store import KnowledgeGraphStore


def _flatten_text(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from _flatten_text(item)
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            yield from _flatten_text(item)
    elif value is not None:
        yield str(value)


class KnowledgeGraphModule(ModuleBase):
    def __init__(self):
        super().__init__("knowledge_graph")
        self.store = KnowledgeGraphStore()

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            text = " ".join(_flatten_text(payload.get("text", payload.get("state", payload))))
            entities = extract_entities(text)[:32]
            relations = build_relations(entities)
            global_stats = self.store.update(entities, relations)
            global_snapshot = self.store.snapshot(limit=24)

            payload["knowledge_graph"] = {
                "entities": entities,
                "relations": relations,
                "causal_graph": build_causal_graph(relations),
                "index": index_knowledge(entities, relations),
                "global": global_snapshot,
            }

            event_bus = payload.get("event_bus")
            if event_bus is not None and hasattr(event_bus, "publish"):
                event_bus.publish(
                    "knowledge_graph.updated",
                    {
                        "signal_entities": len(entities),
                        "signal_relations": len(relations),
                        **global_stats,
                    },
                    source=self.name,
                )

            enriched.append(
                Signal(
                    source=self.name,
                    stage=signal.stage,
                    payload=payload,
                    score=signal.score + 0.03,
                )
            )
        return enriched
