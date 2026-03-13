from __future__ import annotations
from typing import Dict, Any


def run_pattern_detector(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["pattern_detector"] = "ok"
    return result
