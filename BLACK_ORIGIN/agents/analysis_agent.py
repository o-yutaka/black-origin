from __future__ import annotations
from typing import Dict, Any


def run_analysis_agent(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["analysis_agent"] = "ok"
    return result
