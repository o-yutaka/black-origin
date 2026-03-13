from __future__ import annotations
from typing import Dict, Any


def run_node_manager(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["node_manager"] = "ok"
    return result
