from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from BLACK_ORIGIN.recomposition.archive import CandidateArchive
from BLACK_ORIGIN.recomposition.core import RecompositionCore
from BLACK_ORIGIN.recomposition.rollback import RollbackManager


class RecompositionRollbackTests(unittest.TestCase):
    def make_core(self, tmp: str) -> RecompositionCore:
        return RecompositionCore(
            archive=CandidateArchive(str(Path(tmp) / "recomposition.sqlite3"))
        )

    def test_explicit_rollback_restores_previous_stable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            rollback = RollbackManager(core.archive)

            first = core.register({"version": 1})
            core.evaluate(first.candidate_id, {"quality": 0.80})
            self.assertTrue(core.promote(first.candidate_id, ["quality"]).allowed)

            second = core.register({"version": 2}, parent_ids=[first.candidate_id])
            core.evaluate(second.candidate_id, {"quality": 0.90})
            self.assertTrue(
                core.promote(second.candidate_id, ["quality"], min_improvement=0.01).allowed
            )
            self.assertEqual(core.archive.stable_candidate().candidate_id, second.candidate_id)

            restored = rollback.rollback_last_promotion("post-promotion regression")

            self.assertEqual(restored.candidate_id, first.candidate_id)
            self.assertEqual(core.archive.stable_candidate().candidate_id, first.candidate_id)
            self.assertEqual(core.archive.get_candidate(second.candidate_id).status, "validated")
            history = rollback.history()
            self.assertEqual(len(history), 1)
            self.assertEqual(history[0].from_candidate_id, second.candidate_id)
            self.assertEqual(history[0].to_candidate_id, first.candidate_id)
            self.assertEqual(history[0].reason, "post-promotion regression")

    def test_initial_stable_has_no_rollback_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            rollback = RollbackManager(core.archive)
            first = core.register({"version": 1})
            core.evaluate(first.candidate_id, {"quality": 0.80})
            core.promote(first.candidate_id, ["quality"])

            with self.assertRaisesRegex(RuntimeError, "no previous stable checkpoint"):
                rollback.rollback_last_promotion("cannot rollback initial checkpoint")

            self.assertEqual(core.archive.stable_candidate().candidate_id, first.candidate_id)
            self.assertEqual(rollback.history(), [])

    def test_rollback_requires_reason(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            rollback = RollbackManager(core.archive)
            with self.assertRaisesRegex(ValueError, "reason"):
                rollback.rollback_last_promotion("   ")

    def test_second_rollback_without_new_promotion_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            core = self.make_core(tmp)
            rollback = RollbackManager(core.archive)
            first = core.register({"version": 1})
            core.evaluate(first.candidate_id, {"quality": 0.80})
            core.promote(first.candidate_id, ["quality"])
            second = core.register({"version": 2})
            core.evaluate(second.candidate_id, {"quality": 0.90})
            core.promote(second.candidate_id, ["quality"], min_improvement=0.01)

            rollback.rollback_last_promotion("restore v1")
            with self.assertRaisesRegex(RuntimeError, "no previous stable checkpoint"):
                rollback.rollback_last_promotion("do not over-rollback")

            self.assertEqual(core.archive.stable_candidate().candidate_id, first.candidate_id)


if __name__ == "__main__":
    unittest.main()
