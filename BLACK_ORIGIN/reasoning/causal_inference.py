from __future__ import annotations
from typing import Dict, Any


def run_causal_inference(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["causal_inference"] = "ok"
    return result
