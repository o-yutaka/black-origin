from __future__ import annotations
from typing import Dict, Any


def run_task_executor(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["task_executor"] = "ok"
    return result
