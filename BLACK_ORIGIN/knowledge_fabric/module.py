from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class KnowledgeFabricModule(ModuleBase):
    def __init__(self):
        super().__init__("knowledge_fabric")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["knowledge_fabric"] = {"status": "processed", "components": ['entity_graph', 'causal_graph', 'temporal_graph', 'semantic_index']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
