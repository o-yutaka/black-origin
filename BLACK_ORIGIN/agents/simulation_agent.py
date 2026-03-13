from __future__ import annotations
from typing import Dict, Any


def run_simulation_agent(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["simulation_agent"] = "ok"
    return result
