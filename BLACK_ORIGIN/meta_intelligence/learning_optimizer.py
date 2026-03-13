from __future__ import annotations
from typing import Dict, Any


def run_learning_optimizer(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["learning_optimizer"] = "ok"
    return result
