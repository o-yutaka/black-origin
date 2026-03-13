from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class DatasetRecord:
    dataset_id: str
    category: str
    source: str
    url: str
    reliability: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EngineEvent:
    stage: str
    payload: dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class LoopSnapshot:
    cycle: int
    stage: str
    summary: str
    metrics: dict[str, Any]
