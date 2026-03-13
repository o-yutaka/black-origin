from __future__ import annotations
from typing import Dict, Any


def run_intelligence_analyzer(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["intelligence_analyzer"] = "ok"
    return result
