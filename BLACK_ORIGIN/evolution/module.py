from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class EvolutionModule(ModuleBase):
    def __init__(self):
        super().__init__("evolution")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["evolution"] = {"status": "processed", "components": ['architecture_optimizer', 'agent_optimizer', 'knowledge_optimizer']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
