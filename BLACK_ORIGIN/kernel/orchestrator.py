from __future__ import annotations

from typing import Any

from BLACK_ORIGIN.core.contracts import Engine
from BLACK_ORIGIN.kernel.planetary_loop import LOOP_STAGES, PlanetaryLoop


class KernelOrchestrator:
    def __init__(self, engines: dict[str, Engine]) -> None:
        self.engines = engines
        self.loop = PlanetaryLoop()

    def run_cycle(self) -> dict[str, Any]:
        context: dict[str, Any] = {"cycle": self.loop.state.cycle}
        for stage in LOOP_STAGES:
            engine = self.engines.get(stage)
            if engine is not None:
                output = engine.run(context)
                context[stage] = output
            self.loop.advance(stage, context)
        self.loop.next_cycle()
        return context
