from __future__ import annotations
from typing import Dict, Any


def run_trend_detector(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["trend_detector"] = "ok"
    return result
