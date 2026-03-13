from __future__ import annotations
from typing import Dict, Any


def run_orchestrator_link(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["orchestrator_link"] = "ok"
    return result
