from __future__ import annotations


class AgentSwarmEngine:
    name = "swarm"

    AGENT_TYPES = ["research", "analysis", "crawler", "simulation", "monitoring"]

    def run(self, context: dict[str, object]) -> dict[str, object]:
        tasks = []
        decision = context.get("decision_engine", {}).get("policy_recommendation", "observe")
        for agent in self.AGENT_TYPES:
            tasks.append({"agent": f"{agent}_agent", "task": f"{decision}_{agent}"})
        return {"active_agents": len(tasks), "tasks": tasks}
