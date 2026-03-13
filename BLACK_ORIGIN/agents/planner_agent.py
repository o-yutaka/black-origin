from __future__ import annotations

from typing import Any, Dict, List


def run_planner_agent(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    goal = result.get("goal", "improve-system")
    steps: List[str] = [
        f"decompose-{goal}",
        "prioritize-subtasks",
        "dispatch-to-swarm",
        "evaluate-outcomes",
    ]
    result["planner_agent"] = {"goal": goal, "plan": steps}
    return result
