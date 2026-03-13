from __future__ import annotations
from typing import Dict, Any


def run_civilization_simulator(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["civilization_simulator"] = "ok"
    return result
