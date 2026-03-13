from __future__ import annotations
from typing import Dict, Any


def run_vector_memory(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["vector_memory"] = "ok"
    return result
