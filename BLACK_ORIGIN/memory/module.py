from __future__ import annotations

from typing import List

from BLACK_ORIGIN.common import ModuleBase, Signal
from BLACK_ORIGIN.memory.context_memory import ContextMemory
from BLACK_ORIGIN.memory.long_term_memory import LongTermMemoryStore
from BLACK_ORIGIN.memory.memory_retrieval import retrieve_memories
from BLACK_ORIGIN.memory.vector_memory import run_vector_memory


class MemoryModule(ModuleBase):
    def __init__(self):
        super().__init__("memory")
        self.long_term = LongTermMemoryStore()
        self.context_memory = ContextMemory(window=12)

    def process(self, signals: List[Signal]) -> List[Signal]:
        enriched: List[Signal] = []
        for signal in signals:
            payload = dict(signal.payload)
            fact = str(payload.get("state", payload.get("text", signal.stage)))
            memory_item = {"fact": fact, "importance": round(min(1.0, signal.score + 0.1), 2)}
            self.long_term.remember(memory_item)
            self.context_memory.push({"stage": signal.stage, "fact": fact})
            retrieved = retrieve_memories(signal.stage, self.long_term.entries)
            vectorized = run_vector_memory({"text": fact, "query": signal.stage})["vector_memory"]
            payload["memory"] = {
                "long_term_entries": len(self.long_term.entries),
                "context_window": len(self.context_memory.snapshot()),
                "retrieved": retrieved,
                "vector": vectorized,
            }
            enriched.append(Signal(source=self.name, stage=signal.stage, payload=payload, score=signal.score + 0.03))
        return enriched
