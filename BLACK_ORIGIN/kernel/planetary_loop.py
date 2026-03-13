from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from BLACK_ORIGIN.core.models import LoopSnapshot


LOOP_STAGES = [
    "internet_scan",
    "dataset_discovery",
    "crawler_execution",
    "data_ingestion",
    "stream_processing",
    "vector_memory_update",
    "knowledge_graph_update",
    "planetary_data_index_update",
    "world_model_update",
    "planetary_simulation",
    "decision_engine",
    "agent_swarm_execution",
    "reinforcement_learning",
    "system_evolution",
]


@dataclass(slots=True)
class PlanetaryLoopState:
    cycle: int = 0
    stage: str = "boot"


class PlanetaryLoop:
    def __init__(self) -> None:
        self.state = PlanetaryLoopState()
        self.snapshots: list[LoopSnapshot] = []

    def advance(self, stage: str, context: dict[str, Any]) -> LoopSnapshot:
        self.state.stage = stage
        snapshot = LoopSnapshot(
            cycle=self.state.cycle,
            stage=stage,
            summary=f"Stage {stage} completed",
            metrics={"keys": len(context.keys())},
        )
        self.snapshots.append(snapshot)
        return snapshot

    def next_cycle(self) -> None:
        self.state.cycle += 1
