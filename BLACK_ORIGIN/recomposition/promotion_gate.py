from __future__ import annotations

from collections import defaultdict
from statistics import fmean
from typing import Dict, Iterable, Mapping, Sequence

from BLACK_ORIGIN.recomposition.models import Evaluation, PromotionDecision


def _mean_metrics(evaluations: Iterable[Evaluation]) -> Dict[str, float]:
    buckets: dict[str, list[float]] = defaultdict(list)
    for evaluation in evaluations:
        for key, value in evaluation.metrics.items():
            buckets[str(key)].append(float(value))
    return {key: fmean(values) for key, values in buckets.items() if values}


class PromotionGate:
    """Require evaluator evidence and reject unacceptable regressions.

    Higher values are assumed better for all required metrics. Metric-specific
    tolerances can be used when a small regression is acceptable.
    """

    def __init__(
        self,
        required_metrics: Sequence[str],
        min_improvement: float = 0.0,
        max_regression: float = 0.0,
        metric_regression_limits: Mapping[str, float] | None = None,
    ) -> None:
        if not required_metrics:
            raise ValueError("at least one required metric is needed")
        if max_regression < 0:
            raise ValueError("max_regression must be non-negative")
        self.required_metrics = tuple(required_metrics)
        self.min_improvement = float(min_improvement)
        self.max_regression = float(max_regression)
        self.metric_regression_limits = {
            str(key): max(0.0, float(value))
            for key, value in (metric_regression_limits or {}).items()
        }

    def decide(
        self,
        candidate_evaluations: Iterable[Evaluation],
        stable_evaluations: Iterable[Evaluation] = (),
    ) -> PromotionDecision:
        candidate_metrics = _mean_metrics(candidate_evaluations)
        stable_metrics = _mean_metrics(stable_evaluations)
        reasons: list[str] = []
        improvements: Dict[str, float] = {}

        missing = [key for key in self.required_metrics if key not in candidate_metrics]
        if missing:
            reasons.append("missing candidate metrics: " + ", ".join(missing))

        for key in self.required_metrics:
            if key not in candidate_metrics:
                continue
            baseline = stable_metrics.get(key)
            if baseline is None:
                improvements[key] = candidate_metrics[key]
                continue
            delta = candidate_metrics[key] - baseline
            improvements[key] = delta
            allowed_regression = self.metric_regression_limits.get(key, self.max_regression)
            if delta < -allowed_regression:
                reasons.append(
                    f"regression {key}: {delta:+.6f} exceeds {-allowed_regression:+.6f}"
                )

        if stable_metrics:
            best_delta = max((improvements.get(key, float("-inf")) for key in self.required_metrics), default=float("-inf"))
            if best_delta < self.min_improvement:
                reasons.append(
                    f"no required metric improves by at least {self.min_improvement:+.6f}"
                )

        return PromotionDecision(
            allowed=not reasons,
            reasons=tuple(reasons) if reasons else ("promotion gate passed",),
            candidate_metrics=candidate_metrics,
            stable_metrics=stable_metrics,
            improvements=improvements,
        )
