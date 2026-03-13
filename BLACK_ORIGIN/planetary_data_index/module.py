from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class PlanetaryDataIndexModule(ModuleBase):
    def __init__(self):
        super().__init__("planetary_data_index")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["planetary_data_index"] = {"status": "processed", "components": ['dataset_registry', 'api_discovery', 'dataset_crawler', 'stream_registry', 'data_source_ranker']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
