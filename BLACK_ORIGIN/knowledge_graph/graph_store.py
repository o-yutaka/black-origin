from __future__ import annotations

import os
import sqlite3
import threading
import time
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

Relation = Tuple[str, str, str]


class KnowledgeGraphStore:
    """Durable, bounded knowledge graph storage backed by SQLite."""

    def __init__(
        self,
        db_path: str | None = None,
        *,
        max_entities: int = 4096,
        max_relations: int = 16384,
    ) -> None:
        state_dir = Path(os.getenv("BLACK_ORIGIN_STATE_DIR", ".black_origin"))
        self.db_path = Path(db_path) if db_path else state_dir / "knowledge_graph.sqlite3"
        self.max_entities = max(1, max_entities)
        self.max_relations = max(1, max_relations)
        self._lock = threading.RLock()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path, timeout=5.0)
        connection.execute("PRAGMA journal_mode=WAL")
        return connection

    def _initialize(self) -> None:
        with self._lock, self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS entities (
                    name TEXT PRIMARY KEY,
                    mentions INTEGER NOT NULL DEFAULT 0,
                    last_seen REAL NOT NULL
                );

                CREATE TABLE IF NOT EXISTS relations (
                    source TEXT NOT NULL,
                    relation TEXT NOT NULL,
                    target TEXT NOT NULL,
                    mentions INTEGER NOT NULL DEFAULT 0,
                    last_seen REAL NOT NULL,
                    PRIMARY KEY (source, relation, target)
                );

                CREATE INDEX IF NOT EXISTS idx_entities_rank
                    ON entities (mentions DESC, last_seen DESC);

                CREATE INDEX IF NOT EXISTS idx_relations_rank
                    ON relations (mentions DESC, last_seen DESC);
                """
            )

    def update(self, entities: Iterable[str], relations: Iterable[Relation]) -> Dict[str, int]:
        now = time.time()
        unique_entities = sorted({entity for entity in entities if entity})
        unique_relations = sorted(
            {
                (source, relation, target)
                for source, relation, target in relations
                if source and relation and target
            }
        )

        with self._lock, self._connect() as connection:
            connection.executemany(
                """
                INSERT INTO entities(name, mentions, last_seen)
                VALUES (?, 1, ?)
                ON CONFLICT(name) DO UPDATE SET
                    mentions = mentions + 1,
                    last_seen = excluded.last_seen
                """,
                [(entity, now) for entity in unique_entities],
            )
            connection.executemany(
                """
                INSERT INTO relations(source, relation, target, mentions, last_seen)
                VALUES (?, ?, ?, 1, ?)
                ON CONFLICT(source, relation, target) DO UPDATE SET
                    mentions = mentions + 1,
                    last_seen = excluded.last_seen
                """,
                [(source, relation, target, now) for source, relation, target in unique_relations],
            )
            self._prune(connection)
            entity_count = connection.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
            relation_count = connection.execute("SELECT COUNT(*) FROM relations").fetchone()[0]

        return {"entities": int(entity_count), "relations": int(relation_count)}

    def _prune(self, connection: sqlite3.Connection) -> None:
        connection.execute(
            """
            DELETE FROM entities
            WHERE name NOT IN (
                SELECT name FROM entities
                ORDER BY mentions DESC, last_seen DESC
                LIMIT ?
            )
            """,
            (self.max_entities,),
        )
        connection.execute(
            """
            DELETE FROM relations
            WHERE source NOT IN (SELECT name FROM entities)
               OR target NOT IN (SELECT name FROM entities)
            """
        )
        connection.execute(
            """
            DELETE FROM relations
            WHERE rowid NOT IN (
                SELECT rowid FROM relations
                ORDER BY mentions DESC, last_seen DESC
                LIMIT ?
            )
            """,
            (self.max_relations,),
        )

    def neighbors(self, entity: str, *, limit: int = 8) -> List[Dict[str, object]]:
        with self._lock, self._connect() as connection:
            rows = connection.execute(
                """
                SELECT source, relation, target, mentions
                FROM relations
                WHERE source = ? OR target = ?
                ORDER BY mentions DESC, last_seen DESC
                LIMIT ?
                """,
                (entity, entity, max(1, limit)),
            ).fetchall()

        return [
            {
                "source": source,
                "relation": relation,
                "target": target,
                "mentions": int(mentions),
            }
            for source, relation, target, mentions in rows
        ]

    def snapshot(self, *, limit: int = 24) -> Dict[str, object]:
        row_limit = max(1, limit)
        with self._lock, self._connect() as connection:
            entity_rows = connection.execute(
                """
                SELECT name, mentions
                FROM entities
                ORDER BY mentions DESC, last_seen DESC
                LIMIT ?
                """,
                (row_limit,),
            ).fetchall()
            relation_rows = connection.execute(
                """
                SELECT source, relation, target, mentions
                FROM relations
                ORDER BY mentions DESC, last_seen DESC
                LIMIT ?
                """,
                (row_limit,),
            ).fetchall()
            entity_count = connection.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
            relation_count = connection.execute("SELECT COUNT(*) FROM relations").fetchone()[0]

        return {
            "stats": {
                "entities": int(entity_count),
                "relations": int(relation_count),
            },
            "top_entities": [
                {"name": name, "mentions": int(mentions)}
                for name, mentions in entity_rows
            ],
            "top_relations": [
                {
                    "source": source,
                    "relation": relation,
                    "target": target,
                    "mentions": int(mentions),
                }
                for source, relation, target, mentions in relation_rows
            ],
        }


# Backward-compatible alias for earlier callers.
GraphStore = KnowledgeGraphStore


def run_graph_store(context: Dict[str, object], store: KnowledgeGraphStore | None = None) -> Dict[str, object]:
    result = dict(context)
    graph_store = store or KnowledgeGraphStore()
    entities = list(result.get("entities", []))
    relations = list(result.get("relations", []))
    stats = graph_store.update(entities, relations)
    result["graph_store"] = {**stats, "snapshot": graph_store.snapshot(limit=12)}
    return result
