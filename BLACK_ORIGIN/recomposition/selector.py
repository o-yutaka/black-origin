from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Mapping

from BLACK_ORIGIN.recomposition.models import Candidate


@dataclass(frozen=True)
class SelectionScore:
    candidate_id: str
    performance: float
    diversity_bonus: float
    total: float


class DiversityAwareSelector:
    """Rank parents by empirical performance while preserving exploration."""

    def __init__(self, diversity_weight: float = 0.25):
        if diversity_weight < 0:
            raise ValueError("diversity_weight must be non-negative")
        self.diversity_weight = diversity_weight

    def rank(
        self,
        candidates: Iterable[Candidate],
        performance_by_id: Mapping[str, float],
        children_by_id: Mapping[str, int],
    ) -> List[SelectionScore]:
        ranked: List[SelectionScore] = []
        for candidate in candidates:
            performance = float(performance_by_id.get(candidate.candidate_id, 0.0))
            children = max(0, int(children_by_id.get(candidate.candidate_id, 0)))
            diversity_bonus = self.diversity_weight / (1.0 + children)
            ranked.append(
                SelectionScore(
                    candidate_id=candidate.candidate_id,
                    performance=performance,
                    diversity_bonus=diversity_bonus,
                    total=performance + diversity_bonus,
                )
            )
        return sorted(ranked, key=lambda row: (-row.total, row.candidate_id))
