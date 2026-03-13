from __future__ import annotations
from typing import Dict, Any


def run_economic_model(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["economic_model"] = "ok"
    return result
