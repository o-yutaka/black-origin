from __future__ import annotations
from typing import Dict, Any


def run_screen_reader(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["screen_reader"] = "ok"
    return result
