from __future__ import annotations
from typing import Dict, Any


def run_runtime(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["runtime"] = "ok"
    return result
