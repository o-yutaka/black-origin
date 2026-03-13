from __future__ import annotations

from typing import List

from BLACK_ORIGIN.common import ModuleBase, Signal
from BLACK_ORIGIN.knowledge_graph.entity_extractor import extract_entities
from BLACK_ORIGIN.knowledge_graph.relation_builder import build_relations
from BLACK_ORIGIN.knowledge_graph.knowledge_index import index_knowledge
from BLACK_ORIGIN.knowledge_graph.causal_graph import build_causal_graph


class KnowledgeGraphModule(ModuleBase):
    def __init__(self):
        super().__init__("knowledge_graph")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            text = str(payload.get("text", payload.get("state", "")))
            entities = extract_entities(text)
            relations = build_relations(entities)
            payload["knowledge_graph"] = {
                "entities": entities,
                "relations": relations,
                "causal_graph": build_causal_graph(relations),
                "index": index_knowledge(entities, relations),
            }
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.03))
        return enriched
