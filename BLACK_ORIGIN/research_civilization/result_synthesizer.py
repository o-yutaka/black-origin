from __future__ import annotations
from typing import Dict, Any


def run_result_synthesizer(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["result_synthesizer"] = "ok"
    return result
