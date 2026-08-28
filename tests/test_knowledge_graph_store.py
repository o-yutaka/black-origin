from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from BLACK_ORIGIN.knowledge_graph.graph_store import KnowledgeGraphStore


class KnowledgeGraphStoreTests(unittest.TestCase):
    def test_persists_across_instances(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = str(Path(tmp) / "knowledge.sqlite3")
            first = KnowledgeGraphStore(db_path)
            first.update(
                ["Earth", "AI"],
                [("Earth", "co_occurs_with", "AI")],
            )

            second = KnowledgeGraphStore(db_path)
            snapshot = second.snapshot()

            self.assertEqual(snapshot["stats"], {"entities": 2, "relations": 1})
            self.assertEqual(len(second.neighbors("Earth")), 1)

    def test_store_is_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = str(Path(tmp) / "knowledge.sqlite3")
            store = KnowledgeGraphStore(db_path, max_entities=2, max_relations=1)
            store.update(
                ["Earth", "AI", "Science"],
                [
                    ("Earth", "co_occurs_with", "AI"),
                    ("AI", "co_occurs_with", "Science"),
                ],
            )

            stats = store.snapshot()["stats"]
            self.assertLessEqual(stats["entities"], 2)
            self.assertLessEqual(stats["relations"], 1)


if __name__ == "__main__":
    unittest.main()
