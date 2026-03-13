from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class SimulationModule(ModuleBase):
    def __init__(self):
        super().__init__("simulation")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["simulation"] = {"status": "processed", "components": ['scenario_simulation', 'system_dynamics', 'future_projection']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
