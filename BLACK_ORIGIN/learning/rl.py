from __future__ import annotations


class ReinforcementLearningEngine:
    name = "reinforcement_learning"

    def __init__(self) -> None:
        self.policy_score = 0.5

    def run(self, context: dict[str, object]) -> dict[str, object]:
        active_agents = int(context.get("agent_swarm_execution", {}).get("active_agents", 0))
        self.policy_score = round(min(1.0, self.policy_score + active_agents * 0.01), 3)
        return {"policy_score": self.policy_score, "agent_improvement": active_agents}
