from __future__ import annotations
from typing import Dict, Any


def run_experiment_orchestrator(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["experiment_orchestrator"] = "ok"
    return result
