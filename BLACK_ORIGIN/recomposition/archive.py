from __future__ import annotations

import json
import os
from pathlib import Path
import sqlite3
from typing import Any, Dict, Iterable, List

from BLACK_ORIGIN.recomposition.models import (
    AtomicComponent,
    Candidate,
    Evaluation,
    ReconstructionPlan,
)


def _default_path() -> str:
    root = Path(os.getenv("BLACK_ORIGIN_STATE_DIR", ".black_origin"))
    root.mkdir(parents=True, exist_ok=True)
    return str(root / "recomposition.sqlite3")


class CandidateArchive:
    """Durable archive for experimental, rejected and promoted candidates."""

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or _default_path()
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS candidates (
                    candidate_id TEXT PRIMARY KEY,
                    content_hash TEXT NOT NULL UNIQUE,
                    status TEXT NOT NULL,
                    parent_ids_json TEXT NOT NULL,
                    metadata_json TEXT NOT NULL,
                    created_at REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS components (
                    candidate_id TEXT NOT NULL,
                    component_id TEXT NOT NULL,
                    path TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    value_json TEXT NOT NULL,
                    parent_path TEXT,
                    depth INTEGER NOT NULL,
                    PRIMARY KEY(candidate_id, component_id),
                    FOREIGN KEY(candidate_id) REFERENCES candidates(candidate_id) ON DELETE CASCADE
                );
                CREATE TABLE IF NOT EXISTS lineage (
                    parent_id TEXT NOT NULL,
                    child_id TEXT NOT NULL,
                    relation TEXT NOT NULL DEFAULT 'derived_from',
                    PRIMARY KEY(parent_id, child_id, relation)
                );
                CREATE TABLE IF NOT EXISTS evaluations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id TEXT NOT NULL,
                    evaluator TEXT NOT NULL,
                    metrics_json TEXT NOT NULL,
                    notes TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    FOREIGN KEY(candidate_id) REFERENCES candidates(candidate_id) ON DELETE CASCADE
                );
                CREATE TABLE IF NOT EXISTS reconstruction_plans (
                    plan_id TEXT PRIMARY KEY,
                    parent_ids_json TEXT NOT NULL,
                    selected_components_json TEXT NOT NULL,
                    strategy TEXT NOT NULL,
                    metadata_json TEXT NOT NULL,
                    created_at REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS promotions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id TEXT NOT NULL,
                    previous_stable_id TEXT,
                    reasons_json TEXT NOT NULL,
                    created_at REAL NOT NULL DEFAULT (strftime('%s','now'))
                );
                CREATE INDEX IF NOT EXISTS idx_candidates_status ON candidates(status);
                CREATE INDEX IF NOT EXISTS idx_evaluations_candidate ON evaluations(candidate_id);
                CREATE INDEX IF NOT EXISTS idx_lineage_parent ON lineage(parent_id);
                """
            )

    @staticmethod
    def _json(value: Any) -> str:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)

    def add_candidate(self, candidate: Candidate, components: Iterable[AtomicComponent]) -> Candidate:
        with self._connect() as connection:
            existing = connection.execute(
                "SELECT * FROM candidates WHERE content_hash = ?",
                (candidate.content_hash,),
            ).fetchone()
            if existing is not None:
                existing_parents = list(json.loads(existing["parent_ids_json"]))
                merged_parents = list(dict.fromkeys(existing_parents + list(candidate.parent_ids)))
                if merged_parents != existing_parents:
                    connection.execute(
                        "UPDATE candidates SET parent_ids_json = ? WHERE candidate_id = ?",
                        (self._json(merged_parents), existing["candidate_id"]),
                    )
                for parent_id in candidate.parent_ids:
                    if parent_id != existing["candidate_id"]:
                        connection.execute(
                            "INSERT OR IGNORE INTO lineage(parent_id, child_id) VALUES (?, ?)",
                            (parent_id, existing["candidate_id"]),
                        )
                refreshed = connection.execute(
                    "SELECT * FROM candidates WHERE candidate_id = ?",
                    (existing["candidate_id"],),
                ).fetchone()
                return self._candidate_from_row(refreshed)

            connection.execute(
                """
                INSERT INTO candidates(candidate_id, content_hash, status, parent_ids_json, metadata_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    candidate.candidate_id,
                    candidate.content_hash,
                    candidate.status,
                    self._json(list(candidate.parent_ids)),
                    self._json(dict(candidate.metadata)),
                    candidate.created_at,
                ),
            )
            for component in components:
                connection.execute(
                    """
                    INSERT OR IGNORE INTO components(
                        candidate_id, component_id, path, kind, value_json, parent_path, depth
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        candidate.candidate_id,
                        component.component_id,
                        component.path,
                        component.kind,
                        self._json(component.value),
                        component.parent_path,
                        component.depth,
                    ),
                )
            for parent_id in candidate.parent_ids:
                if parent_id != candidate.candidate_id:
                    connection.execute(
                        "INSERT OR IGNORE INTO lineage(parent_id, child_id) VALUES (?, ?)",
                        (parent_id, candidate.candidate_id),
                    )
        return candidate

    def add_evaluation(self, evaluation: Evaluation) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO evaluations(candidate_id, evaluator, metrics_json, notes, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    evaluation.candidate_id,
                    evaluation.evaluator,
                    self._json(dict(evaluation.metrics)),
                    evaluation.notes,
                    evaluation.created_at,
                ),
            )

    def add_plan(self, plan: ReconstructionPlan) -> ReconstructionPlan:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO reconstruction_plans(
                    plan_id, parent_ids_json, selected_components_json, strategy, metadata_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    plan.plan_id,
                    self._json(list(plan.parent_ids)),
                    self._json(list(plan.selected_components)),
                    plan.strategy,
                    self._json(dict(plan.metadata)),
                    plan.created_at,
                ),
            )
        return plan

    def get_plan(self, plan_id: str) -> ReconstructionPlan | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM reconstruction_plans WHERE plan_id = ?", (plan_id,)
            ).fetchone()
        if row is None:
            return None
        return ReconstructionPlan(
            plan_id=row["plan_id"],
            parent_ids=tuple(json.loads(row["parent_ids_json"])),
            selected_components=tuple(json.loads(row["selected_components_json"])),
            strategy=row["strategy"],
            metadata=json.loads(row["metadata_json"]),
            created_at=float(row["created_at"]),
        )

    def get_candidate(self, candidate_id: str) -> Candidate | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM candidates WHERE candidate_id = ?", (candidate_id,)
            ).fetchone()
        return self._candidate_from_row(row) if row is not None else None

    def stable_candidate(self) -> Candidate | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM candidates WHERE status = 'stable' ORDER BY created_at DESC LIMIT 1"
            ).fetchone()
        return self._candidate_from_row(row) if row is not None else None

    def list_candidates(self, status: str | None = None, limit: int = 100) -> List[Candidate]:
        query = "SELECT * FROM candidates"
        parameters: List[Any] = []
        if status is not None:
            query += " WHERE status = ?"
            parameters.append(status)
        query += " ORDER BY created_at DESC LIMIT ?"
        parameters.append(max(1, int(limit)))
        with self._connect() as connection:
            rows = connection.execute(query, parameters).fetchall()
        return [self._candidate_from_row(row) for row in rows]

    def components_for(self, candidate_id: str) -> List[AtomicComponent]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM components WHERE candidate_id = ? ORDER BY depth, path",
                (candidate_id,),
            ).fetchall()
        return [
            AtomicComponent(
                component_id=row["component_id"],
                path=row["path"],
                kind=row["kind"],
                value=json.loads(row["value_json"]),
                parent_path=row["parent_path"],
                depth=int(row["depth"]),
            )
            for row in rows
        ]

    def evaluations_for(self, candidate_id: str) -> List[Evaluation]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM evaluations WHERE candidate_id = ? ORDER BY created_at",
                (candidate_id,),
            ).fetchall()
        return [
            Evaluation(
                candidate_id=row["candidate_id"],
                evaluator=row["evaluator"],
                metrics=json.loads(row["metrics_json"]),
                notes=row["notes"],
                created_at=float(row["created_at"]),
            )
            for row in rows
        ]

    def children_count(self, candidate_id: str) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS count FROM lineage WHERE parent_id = ?", (candidate_id,)
            ).fetchone()
        return int(row["count"])

    def set_status(self, candidate_id: str, status: str) -> None:
        if status not in {"experimental", "validated", "stable", "rejected", "archived"}:
            raise ValueError(f"unsupported candidate status: {status}")
        with self._connect() as connection:
            cursor = connection.execute(
                "UPDATE candidates SET status = ? WHERE candidate_id = ?", (status, candidate_id)
            )
            if cursor.rowcount == 0:
                raise KeyError(candidate_id)

    def promote(self, candidate_id: str, reasons: Iterable[str]) -> None:
        with self._connect() as connection:
            candidate = connection.execute(
                "SELECT candidate_id FROM candidates WHERE candidate_id = ?", (candidate_id,)
            ).fetchone()
            if candidate is None:
                raise KeyError(candidate_id)
            previous = connection.execute(
                "SELECT candidate_id FROM candidates WHERE status = 'stable' ORDER BY created_at DESC LIMIT 1"
            ).fetchone()
            previous_id = previous["candidate_id"] if previous is not None else None
            if previous_id is not None and previous_id != candidate_id:
                connection.execute(
                    "UPDATE candidates SET status = 'validated' WHERE candidate_id = ?", (previous_id,)
                )
            connection.execute(
                "UPDATE candidates SET status = 'stable' WHERE candidate_id = ?", (candidate_id,)
            )
            connection.execute(
                "INSERT INTO promotions(candidate_id, previous_stable_id, reasons_json) VALUES (?, ?, ?)",
                (candidate_id, previous_id, self._json(list(reasons))),
            )

    def stats(self) -> Dict[str, int]:
        with self._connect() as connection:
            candidate_count = int(connection.execute("SELECT COUNT(*) FROM candidates").fetchone()[0])
            evaluation_count = int(connection.execute("SELECT COUNT(*) FROM evaluations").fetchone()[0])
            lineage_count = int(connection.execute("SELECT COUNT(*) FROM lineage").fetchone()[0])
            plan_count = int(connection.execute("SELECT COUNT(*) FROM reconstruction_plans").fetchone()[0])
        return {
            "candidates": candidate_count,
            "evaluations": evaluation_count,
            "lineage_edges": lineage_count,
            "reconstruction_plans": plan_count,
        }

    @staticmethod
    def _candidate_from_row(row: sqlite3.Row) -> Candidate:
        return Candidate(
            candidate_id=row["candidate_id"],
            content_hash=row["content_hash"],
            status=row["status"],
            parent_ids=tuple(json.loads(row["parent_ids_json"])),
            metadata=json.loads(row["metadata_json"]),
            created_at=float(row["created_at"]),
        )
