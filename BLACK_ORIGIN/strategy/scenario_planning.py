from __future__ import annotations
from typing import Dict, Any


def run_scenario_planning(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["scenario_planning"] = "ok"
    return result
