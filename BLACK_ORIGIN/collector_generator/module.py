from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class CollectorGeneratorModule(ModuleBase):
    def __init__(self):
        super().__init__("collector_generator")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["collector_generator"] = {"status": "processed", "components": ['api_collector_builder', 'crawler_builder', 'stream_connector_builder', 'dataset_parser_builder']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
