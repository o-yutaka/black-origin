from __future__ import annotations
from typing import Dict, Any


def run_causal_graph(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["causal_graph"] = "ok"
    return result
