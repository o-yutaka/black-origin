from __future__ import annotations
from typing import Dict, Any


def run_app_operator(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["app_operator"] = "ok"
    return result
