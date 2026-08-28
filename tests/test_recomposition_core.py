from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from BLACK_ORIGIN.recomposition.archive import CandidateArchive
from BLACK_ORIGIN.recomposition.core import RecompositionCore
from BLACK_ORIGIN.recomposition.decomposer import StructuralDecomposer


class RecompositionCoreTests(unittest.TestCase):
    def make_core(self, tmp: str) -> RecompositionCore:
        archive = CandidateArchive(str(Path(tmp) / "recomposition.sqlite3"))
        return RecompositionCore(archive=archive)

    def test_structural_decomposition_is_bounded_and_deterministic(self) -> None:
        decomposer = StructuralDecomposer(max_depth=4, max_components=8)
        value = {"agent": {"planner": ["search", "verify"]}, "score": 1.0}
        first, first_edges = decomposer.decompose(value)
        second, second_edges = decomposer.decompose(value)

        self.assertLessEqual(len(first), 8)
        self.assertEqual([row.component_id for row in first], [row.component_id for row in second])
        self.assertEqual(first_edges, second_edges)
        self.assertIn("$.agent.planner[0]", {row.path for row in first})

    def test_archive_persists_candidates_evaluations_and_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = self.make_core(tmp)
            parent = first.register({"module": "A", "version": 1})
            child = first.register({"module": "A", "version": 2}, parent_ids=[parent.candidate_id])
            first.evaluate(child.candidate_id, {"quality": 0.8}, evaluator="unit")

            second = self.make_core(tmp)
            restored = second.archive.get_candidate(child.candidate_id)
            self.assertIsNotNone(restored)
            self.assertEqual(tuple(restored.parent_ids), (parent.candidate_id,))
            self.assertEqual(second.archive.children_count(parent.candidate_id), 1)
            self.assertEqual(len(second.archive.evaluations_for(child.candidate_id)), 1)

    def test_duplicate_content_reuses_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            first = core.register({"x": 1})
            second = core.register({"x": 1})
            self.assertEqual(first.candidate_id, second.candidate_id)
            self.assertEqual(core.archive.stats()["candidates"], 1)

    def test_convergent_candidate_preserves_multiple_parent_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            parent_a = core.register({"parent": "A"})
            parent_b = core.register({"parent": "B"})
            first = core.register({"shared": "result"}, parent_ids=[parent_a.candidate_id])
            second = core.register({"shared": "result"}, parent_ids=[parent_b.candidate_id])

            self.assertEqual(first.candidate_id, second.candidate_id)
            restored = core.archive.get_candidate(first.candidate_id)
            self.assertEqual(
                set(restored.parent_ids),
                {parent_a.candidate_id, parent_b.candidate_id},
            )
            self.assertEqual(core.archive.children_count(parent_a.candidate_id), 1)
            self.assertEqual(core.archive.children_count(parent_b.candidate_id), 1)

    def test_cross_branch_fusion_builds_and_persists_plan_without_promotion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            left = core.register({"planner": {"depth": 2}, "memory": "A"})
            right = core.register({"planner": {"depth": 4}, "memory": "B"})
            plan = core.propose_fusion([left.candidate_id, right.candidate_id])

            self.assertEqual(tuple(plan.parent_ids), (left.candidate_id, right.candidate_id))
            self.assertTrue(plan.selected_components)
            restored = core.archive.get_plan(plan.plan_id)
            self.assertIsNotNone(restored)
            self.assertEqual(tuple(restored.selected_components), tuple(plan.selected_components))
            self.assertEqual(core.archive.stats()["reconstruction_plans"], 1)
            self.assertIsNone(core.archive.stable_candidate())

    def test_promotion_gate_rejects_regression_and_preserves_stable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            stable = core.register({"version": "stable"})
            core.evaluate(stable.candidate_id, {"quality": 0.80, "safety": 0.95})
            initial = core.promote(stable.candidate_id, ["quality", "safety"])
            self.assertTrue(initial.allowed)

            candidate = core.register({"version": "candidate"}, parent_ids=[stable.candidate_id])
            core.evaluate(candidate.candidate_id, {"quality": 0.90, "safety": 0.70})
            decision = core.promote(candidate.candidate_id, ["quality", "safety"])

            self.assertFalse(decision.allowed)
            self.assertEqual(core.archive.get_candidate(candidate.candidate_id).status, "rejected")
            self.assertEqual(core.archive.stable_candidate().candidate_id, stable.candidate_id)

    def test_promotion_gate_accepts_non_regressing_improvement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            stable = core.register({"version": 1})
            core.evaluate(stable.candidate_id, {"quality": 0.80, "safety": 0.90})
            core.promote(stable.candidate_id, ["quality", "safety"])

            candidate = core.register({"version": 2}, parent_ids=[stable.candidate_id])
            core.evaluate(candidate.candidate_id, {"quality": 0.86, "safety": 0.91})
            decision = core.promote(
                candidate.candidate_id,
                ["quality", "safety"],
                min_improvement=0.01,
            )

            self.assertTrue(decision.allowed)
            self.assertEqual(core.archive.stable_candidate().candidate_id, candidate.candidate_id)
            self.assertEqual(core.archive.get_candidate(stable.candidate_id).status, "validated")


if __name__ == "__main__":
    unittest.main()
