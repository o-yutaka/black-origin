from __future__ import annotations
from typing import Dict, Any


def run_civilization_designer(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["civilization_designer"] = "ok"
    return result
