from __future__ import annotations

from dataclasses import dataclass
import sqlite3
import time
from typing import List

from BLACK_ORIGIN.recomposition.archive import CandidateArchive
from BLACK_ORIGIN.recomposition.models import Candidate


@dataclass(frozen=True)
class RollbackRecord:
    from_candidate_id: str
    to_candidate_id: str
    reason: str
    created_at: float


class RollbackManager:
    """Restore the immediately previous stable candidate on explicit request.

    This manager never triggers itself. Strategic authority remains outside the
    Recomposition Core; callers (ultimately Decision) must explicitly request a
    rollback and provide a reason.
    """

    def __init__(self, archive: CandidateArchive):
        self.archive = archive
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.archive.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS rollbacks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_candidate_id TEXT NOT NULL,
                    to_candidate_id TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    created_at REAL NOT NULL
                )
                """
            )

    def rollback_last_promotion(self, reason: str) -> Candidate:
        reason = str(reason).strip()
        if not reason:
            raise ValueError("rollback reason is required")

        with self._connect() as connection:
            stable = connection.execute(
                "SELECT candidate_id FROM candidates WHERE status = 'stable' "
                "ORDER BY created_at DESC LIMIT 1"
            ).fetchone()
            if stable is None:
                raise RuntimeError("no stable candidate exists")
            current_id = str(stable["candidate_id"])

            promotion = connection.execute(
                """
                SELECT candidate_id, previous_stable_id
                FROM promotions
                WHERE candidate_id = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (current_id,),
            ).fetchone()
            if promotion is None:
                raise RuntimeError("current stable candidate has no promotion record")
            previous_id = promotion["previous_stable_id"]
            if previous_id is None:
                raise RuntimeError("current stable candidate has no previous stable checkpoint")

            previous = connection.execute(
                "SELECT candidate_id FROM candidates WHERE candidate_id = ?",
                (previous_id,),
            ).fetchone()
            if previous is None:
                raise RuntimeError(f"previous stable candidate is missing: {previous_id}")

            connection.execute(
                "UPDATE candidates SET status = 'validated' WHERE candidate_id = ?",
                (current_id,),
            )
            connection.execute(
                "UPDATE candidates SET status = 'stable' WHERE candidate_id = ?",
                (previous_id,),
            )
            created_at = time.time()
            connection.execute(
                """
                INSERT INTO rollbacks(from_candidate_id, to_candidate_id, reason, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (current_id, previous_id, reason, created_at),
            )

        restored = self.archive.get_candidate(str(previous_id))
        if restored is None:
            raise RuntimeError(f"rollback target disappeared after commit: {previous_id}")
        return restored

    def history(self, limit: int = 100) -> List[RollbackRecord]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT from_candidate_id, to_candidate_id, reason, created_at
                FROM rollbacks
                ORDER BY id DESC
                LIMIT ?
                """,
                (max(1, int(limit)),),
            ).fetchall()
        return [
            RollbackRecord(
                from_candidate_id=str(row["from_candidate_id"]),
                to_candidate_id=str(row["to_candidate_id"]),
                reason=str(row["reason"]),
                created_at=float(row["created_at"]),
            )
            for row in rows
        ]
