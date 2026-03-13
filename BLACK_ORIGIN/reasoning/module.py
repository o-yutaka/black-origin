from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class ReasoningModule(ModuleBase):
    def __init__(self):
        super().__init__("reasoning")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["reasoning"] = {"status": "processed", "components": ['multistep_reasoning', 'causal_inference', 'decision_synthesis']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
