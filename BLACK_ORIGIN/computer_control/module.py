from __future__ import annotations
from typing import List
from BLACK_ORIGIN.common import Signal, ModuleBase


class ComputerControlModule(ModuleBase):
    def __init__(self):
        super().__init__("computer_control")

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            payload["computer_control"] = {"status": "processed", "components": ['screen_reader', 'mouse_controller', 'keyboard_controller', 'browser_operator', 'app_operator', 'task_executor']}
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.01))
        return enriched
