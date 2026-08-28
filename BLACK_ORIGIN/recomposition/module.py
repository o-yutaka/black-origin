from __future__ import annotations

from typing import List

from BLACK_ORIGIN.common import ModuleBase, Signal
from BLACK_ORIGIN.recomposition.core import RecompositionCore


class RecompositionModule(ModuleBase):
    """Expose bounded decomposition/archive state to BLACK's evolution stage."""

    def __init__(self):
        super().__init__("recomposition")
        self.core = RecompositionCore()

    def process(self, signals: List[Signal]) -> List[Signal]:
        if not signals or signals[0].stage != "evolve":
            return signals

        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            target = payload.get(
                "recomposition_target",
                {
                    "state": payload.get("state", {}),
                    "goal": payload.get("goal", ""),
                },
            )
            candidate = self.core.register(
                target,
                metadata={"source_stage": signal.stage, "signal_source": signal.source},
            )
            payload["recomposition"] = {
                "candidate_id": candidate.candidate_id,
                "status": candidate.status,
                "content_hash": candidate.content_hash,
                "archive": self.core.archive.stats(),
                "promotion_requires_evidence": True,
            }

            event_bus = payload.get("event_bus")
            if event_bus is not None and hasattr(event_bus, "publish"):
                event_bus.publish(
                    "recomposition.candidate_registered",
                    {
                        "candidate_id": candidate.candidate_id,
                        "status": candidate.status,
                        **self.core.archive.stats(),
                    },
                    source=self.name,
                )

            enriched.append(
                Signal(
                    source=self.name,
                    stage=signal.stage,
                    payload=payload,
                    score=signal.score + 0.04,
                )
            )
        return enriched
