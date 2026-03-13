from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class AgentsModule(ModuleBase):
    def __init__(self):
        super().__init__("agents")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["agents"] = {"status": "processed", "components": ['crawler_agent', 'analysis_agent', 'simulation_agent', 'research_agent', 'strategy_agent']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
