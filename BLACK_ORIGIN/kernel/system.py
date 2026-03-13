from __future__ import annotations
import os
from typing import Dict, List
from BLACK_ORIGIN.common import Signal
from BLACK_ORIGIN.kernel.intelligence_loop import IntelligenceLoop, LOOP_STAGES
from BLACK_ORIGIN.planetary_data_index.module import PlanetaryDataIndexModule
from BLACK_ORIGIN.collector_generator.module import CollectorGeneratorModule
from BLACK_ORIGIN.data_spine.module import DataSpineModule
from BLACK_ORIGIN.memory.module import MemoryModule
from BLACK_ORIGIN.knowledge_fabric.module import KnowledgeFabricModule
from BLACK_ORIGIN.knowledge_graph.module import KnowledgeGraphModule
from BLACK_ORIGIN.world_model.module import WorldModelModule
from BLACK_ORIGIN.planetary_digital_twin.module import PlanetaryDigitalTwinModule
from BLACK_ORIGIN.simulation.module import SimulationModule
from BLACK_ORIGIN.discovery_engine.module import DiscoveryEngineModule
from BLACK_ORIGIN.reasoning.module import ReasoningModule
from BLACK_ORIGIN.strategy.module import StrategyModule
from BLACK_ORIGIN.research_civilization.module import ResearchCivilizationModule
from BLACK_ORIGIN.agents.module import AgentsModule
from BLACK_ORIGIN.orchestrator.module import OrchestratorModule
from BLACK_ORIGIN.meta_intelligence.module import MetaIntelligenceModule
from BLACK_ORIGIN.evolution.module import EvolutionModule
from BLACK_ORIGIN.recursive_intelligence.module import RecursiveIntelligenceModule
from BLACK_ORIGIN.black_engine.module import BlackEngineModule
from BLACK_ORIGIN.computer_control.module import ComputerControlModule
from BLACK_ORIGIN.distributed_network.module import DistributedNetworkModule
from BLACK_ORIGIN.synthetic_universe.module import SyntheticUniverseModule
from BLACK_ORIGIN.civilization.module import CivilizationModule


class BlackOriginSystem:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.loop = IntelligenceLoop()
        self.modules = [
            PlanetaryDataIndexModule(), CollectorGeneratorModule(), DataSpineModule(), MemoryModule(),
            KnowledgeFabricModule(), KnowledgeGraphModule(), WorldModelModule(), PlanetaryDigitalTwinModule(),
            SimulationModule(), DiscoveryEngineModule(), ReasoningModule(), StrategyModule(),
            ResearchCivilizationModule(), AgentsModule(), OrchestratorModule(), MetaIntelligenceModule(),
            EvolutionModule(), RecursiveIntelligenceModule(), BlackEngineModule(), ComputerControlModule(),
            DistributedNetworkModule(), SyntheticUniverseModule(), CivilizationModule()
        ]

    def run_cycle(self, state: Dict[str, str]) -> Dict[str, str]:
        signals: List[Signal] = self.loop.observe(state)
        for stage in LOOP_STAGES[1:]:
            signals = [Signal(source=s.source, stage=stage, payload=s.payload, score=s.score) for s in signals]
            for module in self.modules:
                signals = module.process(signals)
        final = signals[-1].payload if signals else {"status": "empty"}
        final["api_key_loaded"] = bool(self.api_key)
        return {"status": "ok", "knowledge_keys": str(len(final.keys())), "api_key_loaded": str(final['api_key_loaded'])}

    def run(self, cycles: int = 2) -> None:
        state = {"planet": "earth", "mode": "continuous"}
        for i in range(cycles):
            out = self.run_cycle(state)
            print(f"Cycle {i+1} -> {out}")
