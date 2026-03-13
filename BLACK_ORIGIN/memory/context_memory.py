from __future__ import annotations
from typing import Dict, Any


def run_context_memory(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["context_memory"] = "ok"
    return result
