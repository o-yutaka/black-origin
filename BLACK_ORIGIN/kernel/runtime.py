from __future__ import annotations

from BLACK_ORIGIN.agents.swarm import AgentSwarmEngine
from BLACK_ORIGIN.autogen.engine import AutogeneratorEngine
from BLACK_ORIGIN.autogen.evolution import SystemEvolutionProtocol
from BLACK_ORIGIN.cluster.engine import ClusterEngine
from BLACK_ORIGIN.core.decision import DecisionEngine
from BLACK_ORIGIN.core.engines import LambdaEngine, build_foundational_engines
from BLACK_ORIGIN.core.models import DatasetRecord
from BLACK_ORIGIN.kernel.orchestrator import KernelOrchestrator
from BLACK_ORIGIN.learning.rl import ReinforcementLearningEngine
from BLACK_ORIGIN.observability.engine import ObservabilityEngine
from BLACK_ORIGIN.planetary_index.index import PlanetaryDataIndex
from BLACK_ORIGIN.security.engine import SecurityEngine
from BLACK_ORIGIN.simulation.engine import PlanetarySimulationEngine
from BLACK_ORIGIN.simulation.world_model import WorldModelEngine


def build_runtime() -> KernelOrchestrator:
    index = PlanetaryDataIndex()
    foundational = build_foundational_engines()

    def update_index(context: dict[str, object]) -> dict[str, object]:
        for item in context.get("data_ingestion", {}).get("records", []):
            index.register(
                DatasetRecord(
                    dataset_id=str(item["dataset_id"]),
                    category=str(item["category"]),
                    source=str(item["source"]),
                    url=str(item["url"]),
                    reliability=float(item["reliability"]),
                    metadata={"normalized_source": item.get("normalized_source", "")},
                )
            )
        return index.summary()

    world_model = WorldModelEngine()
    simulation = PlanetarySimulationEngine()
    decision = DecisionEngine()
    swarm = AgentSwarmEngine()
    rl = ReinforcementLearningEngine()
    autogen = AutogeneratorEngine()
    evolution = SystemEvolutionProtocol()
    cluster = ClusterEngine()
    observability = ObservabilityEngine()
    security = SecurityEngine()

    engines = {
        **foundational,
        "planetary_data_index_update": LambdaEngine("planetary_data_index_update", update_index),
        "world_model_update": world_model,
        "planetary_simulation": simulation,
        "decision_engine": decision,
        "agent_swarm_execution": swarm,
        "reinforcement_learning": rl,
        "system_evolution": LambdaEngine(
            "system_evolution",
            lambda ctx: {
                "bottlenecks": ["stream_lag"] if int(ctx.get("stream_processing", {}).get("events_processed", 0)) > 50 else [],
                "generated_modules": autogen.run(ctx)["generated_modules"],
                "evolution_plan": evolution.expansion_plan(ctx),
                "cluster_nodes": cluster.run(ctx)["distributed_nodes"],
                "security": security.run(ctx),
                "observability": observability.run(ctx),
            },
        ),
    }
    return KernelOrchestrator(engines=engines)
