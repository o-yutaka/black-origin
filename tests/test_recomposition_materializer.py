from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from BLACK_ORIGIN.recomposition.archive import CandidateArchive
from BLACK_ORIGIN.recomposition.core import RecompositionCore


class RecompositionMaterializerTests(unittest.TestCase):
    def make_core(self, tmp: str) -> RecompositionCore:
        return RecompositionCore(
            archive=CandidateArchive(str(Path(tmp) / "recomposition.sqlite3"))
        )

    @staticmethod
    def component_id(core: RecompositionCore, candidate_id: str, path: str) -> str:
        matches = [
            component.component_id
            for component in core.archive.components_for(candidate_id)
            if component.path == path
        ]
        if len(matches) != 1:
            raise AssertionError(f"expected one component at {path}, got {matches}")
        return matches[0]

    @staticmethod
    def root_value(core: RecompositionCore, candidate_id: str) -> object:
        roots = [
            component.value
            for component in core.archive.components_for(candidate_id)
            if component.path == "$"
        ]
        if len(roots) != 1:
            raise AssertionError(f"expected one root, got {len(roots)}")
        return roots[0]

    def test_materializes_true_cross_branch_hybrid_as_experimental(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            left = core.register({"planner": {"depth": 2}, "memory": "A"})
            right = core.register({"planner": {"depth": 4}, "memory": "B"})

            scores = {
                self.component_id(core, right.candidate_id, "$.planner.depth"): 10.0,
                self.component_id(core, left.candidate_id, "$.memory"): 10.0,
            }
            plan = core.propose_fusion(
                [left.candidate_id, right.candidate_id],
                component_scores=scores,
            )
            candidate = core.materialize_plan(plan.plan_id)

            self.assertEqual(
                self.root_value(core, candidate.candidate_id),
                {"planner": {"depth": 4}, "memory": "A"},
            )
            self.assertNotEqual(candidate.candidate_id, left.candidate_id)
            self.assertNotEqual(candidate.candidate_id, right.candidate_id)
            self.assertEqual(candidate.status, "experimental")
            self.assertEqual(
                set(candidate.parent_ids),
                {left.candidate_id, right.candidate_id},
            )
            self.assertEqual(candidate.metadata["reconstruction_plan"], plan.plan_id)
            self.assertTrue(candidate.metadata["materialized"])
            self.assertIsNone(core.archive.stable_candidate())

    def test_materialization_never_replaces_existing_stable_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            stable = core.register({"planner": {"depth": 2}, "memory": "A"})
            core.evaluate(stable.candidate_id, {"quality": 0.8})
            self.assertTrue(core.promote(stable.candidate_id, ["quality"]).allowed)

            branch = core.register({"planner": {"depth": 4}, "memory": "B"})
            scores = {
                self.component_id(core, branch.candidate_id, "$.planner.depth"): 10.0,
                self.component_id(core, stable.candidate_id, "$.memory"): 10.0,
            }
            plan = core.propose_fusion(
                [stable.candidate_id, branch.candidate_id],
                component_scores=scores,
            )
            candidate = core.materialize_plan(plan.plan_id)

            self.assertEqual(candidate.status, "experimental")
            self.assertEqual(core.archive.stable_candidate().candidate_id, stable.candidate_id)
            self.assertEqual(core.archive.get_candidate(stable.candidate_id).status, "stable")

    def test_sequence_materialization_can_extend_from_another_branch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            left = core.register({"steps": ["a", "b"]})
            right = core.register({"steps": ["x", "y", "z"]})
            scores = {
                self.component_id(core, right.candidate_id, "$.steps[2]"): 10.0,
            }
            plan = core.propose_fusion(
                [left.candidate_id, right.candidate_id],
                component_scores=scores,
            )
            candidate = core.materialize_plan(plan.plan_id)

            self.assertEqual(
                self.root_value(core, candidate.candidate_id),
                {"steps": ["a", "b", "z"]},
            )

    def test_set_materialization_fails_explicitly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            left = core.register({"values": {1, 2}})
            right = core.register({"values": {2, 3}})
            plan = core.propose_fusion([left.candidate_id, right.candidate_id])

            with self.assertRaisesRegex(TypeError, "set materialization is unsupported"):
                core.materialize_plan(plan.plan_id)

    def test_missing_plan_fails_without_creating_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            before = core.archive.stats()["candidates"]
            with self.assertRaises(KeyError):
                core.materialize_plan("plan_missing")
            self.assertEqual(core.archive.stats()["candidates"], before)


if __name__ == "__main__":
    unittest.main()
