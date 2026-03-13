from __future__ import annotations
from typing import Dict, Any


def run_decision_auditor(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["decision_auditor"] = "ok"
    return result
