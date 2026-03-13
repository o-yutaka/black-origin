from __future__ import annotations
from typing import Dict, Any


def run_scenario_simulation(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["scenario_simulation"] = "ok"
    return result
