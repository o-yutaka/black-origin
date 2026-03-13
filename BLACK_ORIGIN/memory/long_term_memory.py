from __future__ import annotations
from typing import Dict, Any


def run_long_term_memory(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["long_term_memory"] = "ok"
    return result
