from __future__ import annotations
from typing import Dict, Any


def run_keyboard_controller(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["keyboard_controller"] = "ok"
    return result
