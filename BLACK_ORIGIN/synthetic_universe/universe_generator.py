from __future__ import annotations
from typing import Dict, Any


def run_universe_generator(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["universe_generator"] = "ok"
    return result
