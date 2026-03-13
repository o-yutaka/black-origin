from __future__ import annotations
from typing import Dict, Any


def run_parallel_executor(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["parallel_executor"] = "ok"
    return result
