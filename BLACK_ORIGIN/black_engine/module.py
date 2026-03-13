from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class BlackEngineModule(ModuleBase):
    def __init__(self):
        super().__init__("black_engine")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["black_engine"] = {"status": "processed", "components": ['model_generator', 'agent_generator', 'strategy_generator', 'architecture_generator', 'research_generator', 'civilization_generator']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
