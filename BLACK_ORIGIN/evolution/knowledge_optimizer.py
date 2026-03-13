from __future__ import annotations
from typing import Dict, Any


def run_knowledge_optimizer(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["knowledge_optimizer"] = "ok"
    return result
