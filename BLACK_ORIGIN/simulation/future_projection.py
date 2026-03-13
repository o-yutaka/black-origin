from __future__ import annotations
from typing import Dict, Any


def run_future_projection(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["future_projection"] = "ok"
    return result
