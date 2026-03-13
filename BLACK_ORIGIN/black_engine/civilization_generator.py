from __future__ import annotations
from typing import Dict, Any


def run_civilization_generator(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["civilization_generator"] = "ok"
    return result
