from __future__ import annotations
from typing import Dict, Any


def run_anomaly_detector(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["anomaly_detector"] = "ok"
    return result
