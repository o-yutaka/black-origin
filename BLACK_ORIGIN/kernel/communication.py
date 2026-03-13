from __future__ import annotations
from typing import Dict, Any


def run_communication(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["communication"] = "ok"
    return result
