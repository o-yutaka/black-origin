from __future__ import annotations


class KnowledgeGraphEngine:
    name = "graph"

    def __init__(self) -> None:
        self.nodes: dict[str, str] = {}
        self.edges: set[tuple[str, str, str]] = set()

    def run(self, context: dict[str, object]) -> dict[str, object]:
        records = context.get("data_ingestion", {}).get("records", [])
        for item in records:
            category = str(item["category"])
            source = str(item["source"])
            dataset_id = str(item["dataset_id"])
            self.nodes[dataset_id] = "dataset"
            self.nodes[category] = "category"
            self.nodes[source] = "source"
            self.edges.add((category, dataset_id, "contains"))
            self.edges.add((source, dataset_id, "publishes"))
        return {
            "neo4j_uri": "bolt://localhost:7687",
            "nodes": len(self.nodes),
            "edges": len(self.edges),
        }
