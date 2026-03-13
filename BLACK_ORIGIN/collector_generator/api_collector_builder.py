from __future__ import annotations
from typing import Dict, Any


def run_api_collector_builder(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["api_collector_builder"] = "ok"
    return result
