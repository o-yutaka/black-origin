from __future__ import annotations
from typing import Dict, Any


def run_system_coordinator(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["system_coordinator"] = "ok"
    return result
