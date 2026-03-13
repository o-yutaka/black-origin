from __future__ import annotations
from typing import Dict, Any


def run_population_model(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["population_model"] = "ok"
    return result
