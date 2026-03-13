from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from BLACK_ORIGIN.core.contracts import Engine
from BLACK_ORIGIN.crawler.engine import CrawlerEngine
from BLACK_ORIGIN.data.discovery import DataDiscoveryEngine
from BLACK_ORIGIN.graph.engine import KnowledgeGraphEngine
from BLACK_ORIGIN.pipeline.engine import DataPipelineEngine
from BLACK_ORIGIN.stream.engine import StreamEngine
from BLACK_ORIGIN.vector.engine import VectorIntelligenceEngine


@dataclass(slots=True)
class LambdaEngine(Engine):
    name: str
    fn: Callable[[dict[str, Any]], dict[str, Any]]

    def run(self, context: dict[str, object]) -> dict[str, object]:
        return self.fn(context)


def build_foundational_engines() -> dict[str, Engine]:
    discovery = DataDiscoveryEngine()
    crawler = CrawlerEngine()
    pipeline = DataPipelineEngine()
    stream = StreamEngine()
    vector = VectorIntelligenceEngine()
    graph = KnowledgeGraphEngine()

    return {
        "internet_scan": LambdaEngine("internet_scan", lambda ctx: {"scan_targets": 5 + int(ctx.get("cycle", 0))}),
        "dataset_discovery": discovery,
        "crawler_execution": crawler,
        "data_ingestion": pipeline,
        "stream_processing": stream,
        "vector_memory_update": vector,
        "knowledge_graph_update": graph,
    }
