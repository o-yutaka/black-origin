from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Iterable, Mapping, Sequence

from BLACK_ORIGIN.recomposition.archive import CandidateArchive
from BLACK_ORIGIN.recomposition.decomposer import StructuralDecomposer
from BLACK_ORIGIN.recomposition.fusion import CrossBranchFusion
from BLACK_ORIGIN.recomposition.models import Candidate, Evaluation, PromotionDecision, ReconstructionPlan
from BLACK_ORIGIN.recomposition.promotion_gate import PromotionGate
from BLACK_ORIGIN.recomposition.selector import DiversityAwareSelector, SelectionScore


def _stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


class RecompositionCore:
    """BLACK's decomposition -> archive -> fusion -> promotion infrastructure."""

    def __init__(
        self,
        archive: CandidateArchive | None = None,
        decomposer: StructuralDecomposer | None = None,
    ) -> None:
        self.archive = archive or CandidateArchive()
        self.decomposer = decomposer or StructuralDecomposer()
        self.selector = DiversityAwareSelector()
        self.fusion = CrossBranchFusion()

    def register(
        self,
        value: Any,
        *,
        parent_ids: Sequence[str] = (),
        metadata: Mapping[str, Any] | None = None,
    ) -> Candidate:
        components, edges = self.decomposer.decompose(value)
        content_hash = hashlib.sha256(_stable_json(value).encode("utf-8")).hexdigest()
        candidate = Candidate(
            candidate_id="cand_" + content_hash[:20],
            content_hash=content_hash,
            status="experimental",
            parent_ids=tuple(parent_ids),
            metadata={
                **dict(metadata or {}),
                "component_count": len(components),
                "decomposition_edges": len(edges),
            },
        )
        return self.archive.add_candidate(candidate, components)

    def evaluate(
        self,
        candidate_id: str,
        metrics: Mapping[str, float],
        *,
        evaluator: str = "default",
        notes: str = "",
    ) -> Evaluation:
        if self.archive.get_candidate(candidate_id) is None:
            raise KeyError(candidate_id)
        evaluation = Evaluation(
            candidate_id=candidate_id,
            metrics={str(key): float(value) for key, value in metrics.items()},
            evaluator=evaluator,
            notes=notes,
        )
        self.archive.add_evaluation(evaluation)
        return evaluation

    def rank_parents(
        self,
        candidate_ids: Sequence[str],
        performance_by_id: Mapping[str, float],
    ) -> list[SelectionScore]:
        candidates = []
        children = {}
        for candidate_id in candidate_ids:
            candidate = self.archive.get_candidate(candidate_id)
            if candidate is None:
                continue
            candidates.append(candidate)
            children[candidate_id] = self.archive.children_count(candidate_id)
        return self.selector.rank(candidates, performance_by_id, children)

    def propose_fusion(
        self,
        parent_ids: Sequence[str],
        component_scores: Dict[str, float] | None = None,
    ) -> ReconstructionPlan:
        components = {
            parent_id: self.archive.components_for(parent_id)
            for parent_id in parent_ids
        }
        missing = [parent_id for parent_id, rows in components.items() if not rows]
        if missing:
            raise KeyError("missing parent candidates: " + ", ".join(missing))
        plan = self.fusion.build_plan(parent_ids, components, component_scores)
        return self.archive.add_plan(plan)

    def promotion_decision(
        self,
        candidate_id: str,
        required_metrics: Sequence[str],
        *,
        min_improvement: float = 0.0,
        max_regression: float = 0.0,
        metric_regression_limits: Mapping[str, float] | None = None,
    ) -> PromotionDecision:
        candidate = self.archive.get_candidate(candidate_id)
        if candidate is None:
            raise KeyError(candidate_id)
        stable = self.archive.stable_candidate()
        gate = PromotionGate(
            required_metrics=required_metrics,
            min_improvement=min_improvement,
            max_regression=max_regression,
            metric_regression_limits=metric_regression_limits,
        )
        stable_evaluations: Iterable[Evaluation] = ()
        if stable is not None and stable.candidate_id != candidate_id:
            stable_evaluations = self.archive.evaluations_for(stable.candidate_id)
        return gate.decide(
            self.archive.evaluations_for(candidate_id),
            stable_evaluations,
        )

    def promote(
        self,
        candidate_id: str,
        required_metrics: Sequence[str],
        *,
        min_improvement: float = 0.0,
        max_regression: float = 0.0,
        metric_regression_limits: Mapping[str, float] | None = None,
    ) -> PromotionDecision:
        decision = self.promotion_decision(
            candidate_id,
            required_metrics,
            min_improvement=min_improvement,
            max_regression=max_regression,
            metric_regression_limits=metric_regression_limits,
        )
        if not decision.allowed:
            self.archive.set_status(candidate_id, "rejected")
            return decision
        self.archive.promote(candidate_id, decision.reasons)
        return decision
