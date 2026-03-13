from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class MemoryModule(ModuleBase):
    def __init__(self):
        super().__init__("memory")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["memory"] = {"status": "processed", "components": ['vector_memory', 'long_term_memory', 'context_memory']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
