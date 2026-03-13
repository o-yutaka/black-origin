from __future__ import annotations
from typing import Dict, Any


def run_browser_operator(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["browser_operator"] = "ok"
    return result
