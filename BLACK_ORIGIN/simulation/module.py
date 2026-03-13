from __future__ import annotations

from typing import List

from BLACK_ORIGIN.common import ModuleBase, Signal
from BLACK_ORIGIN.simulation.prediction_engine import forecast_metric
from BLACK_ORIGIN.simulation.scenario_engine import generate_scenarios
from BLACK_ORIGIN.simulation.world_model import evolve_world_state


class SimulationModule(ModuleBase):
    def __init__(self):
        super().__init__("simulation")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            base = {"resources": 1.0 + signal.score, "stability": 1.2}
            scenarios = generate_scenarios(base)
            next_state = evolve_world_state(scenarios[1], {"stability": 0.05, "resources": 0.02})
            forecast = forecast_metric([scenario["resources"] for scenario in scenarios])
            payload["simulation"] = {
                "scenario_count": len(scenarios),
                "next_state": next_state,
                "forecast": forecast,
            }
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.03))
        return enriched
