from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class PlanetaryDigitalTwinModule(ModuleBase):
    def __init__(self):
        super().__init__("planetary_digital_twin")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["planetary_digital_twin"] = {"status": "processed", "components": ['earth_model', 'economic_model', 'technology_model', 'climate_model', 'population_model']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
