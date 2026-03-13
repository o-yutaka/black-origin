from __future__ import annotations
from typing import Dict, Any


def run_mouse_controller(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["mouse_controller"] = "ok"
    return result
