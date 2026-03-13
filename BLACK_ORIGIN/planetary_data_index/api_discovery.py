from __future__ import annotations
from typing import Dict, Any


def run_api_discovery(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["api_discovery"] = "ok"
    return result
