from __future__ import annotations
from typing import Dict, Any


def run_semantic_index(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["semantic_index"] = "ok"
    return result
