from __future__ import annotations
from typing import Dict, Any


def run_climate_model(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["climate_model"] = "ok"
    return result
