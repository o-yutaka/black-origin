from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
import time


@dataclass
class Signal:
    source: str
    stage: str
    payload: Dict[str, Any]
    score: float = 0.0
    ts: float = field(default_factory=time.time)


class ModuleBase:
    name: str

    def __init__(self, name: str):
        self.name = name

    def process(self, signals: List[Signal]) -> List[Signal]:
        return signals
