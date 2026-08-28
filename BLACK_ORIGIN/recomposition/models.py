from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Sequence
import time


CANDIDATE_STATUSES = {
    "experimental",
    "validated",
    "stable",
    "rejected",
    "archived",
}


@dataclass(frozen=True)
class AtomicComponent:
    component_id: str
    path: str
    kind: str
    value: Any
    parent_path: str | None = None
    depth: int = 0


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    content_hash: str
    status: str = "experimental"
    parent_ids: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        if self.status not in CANDIDATE_STATUSES:
            raise ValueError(f"unsupported candidate status: {self.status}")


@dataclass(frozen=True)
class Evaluation:
    candidate_id: str
    metrics: Mapping[str, float]
    evaluator: str = "default"
    notes: str = ""
    created_at: float = field(default_factory=time.time)


@dataclass(frozen=True)
class ReconstructionPlan:
    plan_id: str
    parent_ids: Sequence[str]
    selected_components: Sequence[str]
    strategy: str = "cross_branch_fusion"
    metadata: Mapping[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)


@dataclass(frozen=True)
class PromotionDecision:
    allowed: bool
    reasons: Sequence[str]
    candidate_metrics: Dict[str, float]
    stable_metrics: Dict[str, float]
    improvements: Dict[str, float]
