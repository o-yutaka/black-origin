from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class MetaIntelligenceModule(ModuleBase):
    def __init__(self):
        super().__init__("meta_intelligence")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["meta_intelligence"] = {"status": "processed", "components": ['reason_monitor', 'decision_auditor', 'learning_optimizer']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
