from __future__ import annotations
from typing import Dict, Any


def run_temporal_graph(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["temporal_graph"] = "ok"
    return result
