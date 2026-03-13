from __future__ import annotations
from typing import Dict, List
from BLACK_ORIGIN.common import Signal

LOOP_STAGES = ['observe', 'discover', 'ingest', 'learn', 'reason', 'simulate', 'research', 'decide', 'act', 'evolve', 'generate', 'design']


class IntelligenceLoop:
    def __init__(self):
        self.stage_index = 0

    def observe(self, state: Dict[str, str]) -> List[Signal]:
        return [Signal(source="sensor", stage="observe", payload={"state": state}, score=0.1)]

    def next_stage(self) -> str:
        stage = LOOP_STAGES[self.stage_index % len(LOOP_STAGES)]
        self.stage_index += 1
        return stage
