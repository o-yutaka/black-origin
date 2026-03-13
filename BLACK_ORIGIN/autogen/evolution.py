from __future__ import annotations


class SystemEvolutionProtocol:
    def detect_bottlenecks(self, context: dict[str, object]) -> list[str]:
        bottlenecks: list[str] = []
        events = int(context.get("stream_processing", {}).get("events_processed", 0))
        if events > 40:
            bottlenecks.append("stream_backpressure")
        graph_nodes = int(context.get("knowledge_graph_update", {}).get("nodes", 0))
        if graph_nodes > 200:
            bottlenecks.append("graph_compaction_needed")
        return bottlenecks

    def expansion_plan(self, context: dict[str, object]) -> dict[str, object]:
        bottlenecks = self.detect_bottlenecks(context)
        return {
            "expand_agents": "stream_backpressure" in bottlenecks,
            "expand_pipelines": len(bottlenecks) > 0,
            "refactor_subsystems": ["pipeline", "graph"] if bottlenecks else [],
        }
