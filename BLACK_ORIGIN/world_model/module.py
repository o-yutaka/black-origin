from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class WorldModelModule(ModuleBase):
    def __init__(self):
        super().__init__("world_model")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["world_model"] = {"status": "processed", "components": ['economy_model', 'technology_model', 'climate_model', 'population_model']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
