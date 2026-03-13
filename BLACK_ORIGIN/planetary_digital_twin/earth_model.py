from __future__ import annotations
from typing import Dict, Any


def run_earth_model(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["earth_model"] = "ok"
    return result
