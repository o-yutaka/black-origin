from __future__ import annotations
from typing import Dict, Any


def run_simulation_runner(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["simulation_runner"] = "ok"
    return result
