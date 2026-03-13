from __future__ import annotations
from typing import Dict, Any


def run_strategic_planning(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["strategic_planning"] = "ok"
    return result
