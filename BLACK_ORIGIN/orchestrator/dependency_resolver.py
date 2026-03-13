from __future__ import annotations
from typing import Dict, Any


def run_dependency_resolver(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["dependency_resolver"] = "ok"
    return result
