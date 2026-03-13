from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class DistributedNetworkModule(ModuleBase):
    def __init__(self):
        super().__init__("distributed_network")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["distributed_network"] = {"status": "processed", "components": ['node_manager', 'knowledge_sync', 'agent_distribution', 'global_memory']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
