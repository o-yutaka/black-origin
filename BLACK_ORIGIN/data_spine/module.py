from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class DataSpineModule(ModuleBase):
    def __init__(self):
        super().__init__("data_spine")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["data_spine"] = {"status": "processed", "components": ['ingestion_engine', 'normalization_engine', 'stream_processor', 'storage_router']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
