from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class StrategyModule(ModuleBase):
    def __init__(self):
        super().__init__("strategy")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["strategy"] = {"status": "processed", "components": ['risk_analysis', 'scenario_planning', 'strategic_planning']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
