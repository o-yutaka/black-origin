from __future__ import annotations

import tempfile
import threading
import unittest
from pathlib import Path

from BLACK_ORIGIN.recomposition.archive import CandidateArchive
from BLACK_ORIGIN.recomposition.core import RecompositionCore
from BLACK_ORIGIN.recomposition.evaluation import (
    FunctionEvaluator,
    ParallelEvaluationError,
)


class RecompositionEvaluationTests(unittest.TestCase):
    def make_core(self, tmp: str) -> RecompositionCore:
        return RecompositionCore(
            archive=CandidateArchive(str(Path(tmp) / "recomposition.sqlite3"))
        )

    def test_parallel_evaluators_run_concurrently_and_persist_all_results(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            candidate = core.register({"quality": 0.91, "latency": 0.42})
            barrier = threading.Barrier(2, timeout=2.0)

            def quality(value: object) -> dict[str, float]:
                barrier.wait()
                return {"quality": float(value["quality"])}

            def latency(value: object) -> dict[str, float]:
                barrier.wait()
                return {"latency": float(value["latency"])}

            evaluations = core.evaluate_parallel(
                candidate.candidate_id,
                [
                    FunctionEvaluator("quality", quality),
                    FunctionEvaluator("latency", latency),
                ],
                max_workers=2,
            )

            self.assertEqual([row.evaluator for row in evaluations], ["latency", "quality"])
            stored = core.archive.evaluations_for(candidate.candidate_id)
            self.assertEqual(len(stored), 2)
            self.assertEqual(
                {key for row in stored for key in row.metrics},
                {"quality", "latency"},
            )

    def test_parallel_failure_records_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            candidate = core.register({"x": 1})

            def good(value: object) -> dict[str, float]:
                return {"quality": 1.0}

            def bad(value: object) -> dict[str, float]:
                raise RuntimeError("evaluator exploded")

            with self.assertRaises(ParallelEvaluationError):
                core.evaluate_parallel(
                    candidate.candidate_id,
                    [FunctionEvaluator("good", good), FunctionEvaluator("bad", bad)],
                    max_workers=2,
                )

            self.assertEqual(core.archive.evaluations_for(candidate.candidate_id), [])

    def test_evaluator_names_must_be_unique(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            candidate = core.register({"x": 1})
            evaluator = FunctionEvaluator("same", lambda value: {"quality": 1.0})
            with self.assertRaisesRegex(ValueError, "unique"):
                core.evaluate_parallel(candidate.candidate_id, [evaluator, evaluator])

    def test_minimize_metric_counts_lower_value_as_improvement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            stable = core.register({"version": 1})
            core.evaluate(stable.candidate_id, {"quality": 0.80, "latency": 1.00})
            self.assertTrue(
                core.promote(
                    stable.candidate_id,
                    ["quality", "latency"],
                    metric_directions={"latency": "minimize"},
                ).allowed
            )

            candidate = core.register({"version": 2}, parent_ids=[stable.candidate_id])
            core.evaluate(candidate.candidate_id, {"quality": 0.84, "latency": 0.80})
            decision = core.promote(
                candidate.candidate_id,
                ["quality", "latency"],
                min_improvement=0.01,
                metric_directions={"latency": "minimize"},
            )

            self.assertTrue(decision.allowed)
            self.assertAlmostEqual(decision.improvements["quality"], 0.04)
            self.assertAlmostEqual(decision.improvements["latency"], 0.20)
            self.assertEqual(core.archive.stable_candidate().candidate_id, candidate.candidate_id)

    def test_minimize_metric_rejects_latency_regression(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            stable = core.register({"version": "stable"})
            core.evaluate(stable.candidate_id, {"quality": 0.80, "latency": 1.00})
            core.promote(
                stable.candidate_id,
                ["quality", "latency"],
                metric_directions={"latency": "minimize"},
            )

            candidate = core.register({"version": "slow"}, parent_ids=[stable.candidate_id])
            core.evaluate(candidate.candidate_id, {"quality": 0.90, "latency": 1.20})
            decision = core.promote(
                candidate.candidate_id,
                ["quality", "latency"],
                metric_directions={"latency": "minimize"},
            )

            self.assertFalse(decision.allowed)
            self.assertAlmostEqual(decision.improvements["latency"], -0.20)
            self.assertEqual(core.archive.stable_candidate().candidate_id, stable.candidate_id)

    def test_invalid_metric_direction_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            candidate = core.register({"version": 1})
            core.evaluate(candidate.candidate_id, {"quality": 0.8})
            with self.assertRaisesRegex(ValueError, "unsupported metric directions"):
                core.promotion_decision(
                    candidate.candidate_id,
                    ["quality"],
                    metric_directions={"quality": "sideways"},
                )


if __name__ == "__main__":
    unittest.main()
