from __future__ import annotations
from typing import Dict, Any


def run_model_designer(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["model_designer"] = "ok"
    return result
