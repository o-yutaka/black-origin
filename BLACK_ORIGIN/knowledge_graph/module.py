from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class KnowledgeGraphModule(ModuleBase):
    def __init__(self):
        super().__init__("knowledge_graph")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["knowledge_graph"] = {"status": "processed", "components": ['entity_extractor', 'relationship_discovery', 'causal_reasoning']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
