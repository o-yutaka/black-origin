from __future__ import annotations
from typing import Dict, Any


def run_research_planner(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["research_planner"] = "ok"
    return result
