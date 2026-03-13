from __future__ import annotations
from typing import Dict, Any


def run_global_memory(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["global_memory"] = "ok"
    return result
