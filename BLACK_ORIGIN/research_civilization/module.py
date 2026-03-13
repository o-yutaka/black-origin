from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class ResearchCivilizationModule(ModuleBase):
    def __init__(self):
        super().__init__("research_civilization")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["research_civilization"] = {"status": "processed", "components": ['research_planner', 'experiment_orchestrator', 'simulation_runner', 'result_synthesizer']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
