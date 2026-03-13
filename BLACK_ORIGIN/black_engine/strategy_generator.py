from __future__ import annotations
from typing import Dict, Any


def run_strategy_generator(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["strategy_generator"] = "ok"
    return result
