from __future__ import annotations
from typing import Dict, Any


def run_economy_model(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["economy_model"] = "ok"
    return result
