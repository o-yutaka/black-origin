from __future__ import annotations
from typing import Dict, Any


def run_reason_monitor(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["reason_monitor"] = "ok"
    return result
