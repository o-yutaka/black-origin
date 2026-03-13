from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class OrchestratorModule(ModuleBase):
    def __init__(self):
        super().__init__("orchestrator")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["orchestrator"] = {"status": "processed", "components": ['parallel_executor', 'dependency_resolver', 'agent_coordination']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
