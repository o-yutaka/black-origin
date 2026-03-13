from __future__ import annotations
from typing import Dict, Any


def run_risk_analysis(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["risk_analysis"] = "ok"
    return result
