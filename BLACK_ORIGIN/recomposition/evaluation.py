from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Protocol, Sequence


class EvaluatorAdapter(Protocol):
    name: str

    def evaluate(self, value: Any) -> Mapping[str, float]:
        ...


@dataclass(frozen=True)
class FunctionEvaluator:
    """Small adapter for deterministic in-process evaluation functions.

    Generated or untrusted code must not be executed through this adapter. A
    separate sandbox executor should be used for that class of evaluation.
    """

    name: str
    function: Callable[[Any], Mapping[str, float]]

    def evaluate(self, value: Any) -> Mapping[str, float]:
        return self.function(value)


@dataclass(frozen=True)
class EvaluatorOutcome:
    evaluator: str
    metrics: Mapping[str, float]


class ParallelEvaluationError(RuntimeError):
    def __init__(self, failures: Mapping[str, BaseException]):
        self.failures = dict(failures)
        detail = "; ".join(
            f"{name}: {type(error).__name__}: {error}"
            for name, error in sorted(self.failures.items())
        )
        super().__init__(f"parallel evaluation failed: {detail}")


class ParallelEvaluatorSuite:
    """Run independent evaluators concurrently and fail atomically on errors."""

    def __init__(self, max_workers: int | None = None):
        if max_workers is not None and max_workers < 1:
            raise ValueError("max_workers must be positive")
        self.max_workers = max_workers

    def run(
        self,
        value: Any,
        evaluators: Sequence[EvaluatorAdapter],
    ) -> list[EvaluatorOutcome]:
        if not evaluators:
            raise ValueError("at least one evaluator is required")
        names = [str(evaluator.name) for evaluator in evaluators]
        if len(names) != len(set(names)):
            raise ValueError("evaluator names must be unique")

        workers = self.max_workers or len(evaluators)
        outcomes: list[EvaluatorOutcome] = []
        failures: dict[str, BaseException] = {}
        with ThreadPoolExecutor(max_workers=min(workers, len(evaluators))) as executor:
            future_to_name = {
                executor.submit(evaluator.evaluate, value): str(evaluator.name)
                for evaluator in evaluators
            }
            for future in as_completed(future_to_name):
                name = future_to_name[future]
                try:
                    raw_metrics = future.result()
                    metrics = {
                        str(key): float(metric_value)
                        for key, metric_value in raw_metrics.items()
                    }
                    if not metrics:
                        raise ValueError("evaluator returned no metrics")
                    outcomes.append(EvaluatorOutcome(name, metrics))
                except BaseException as error:
                    failures[name] = error

        if failures:
            raise ParallelEvaluationError(failures)
        return sorted(outcomes, key=lambda outcome: outcome.evaluator)
