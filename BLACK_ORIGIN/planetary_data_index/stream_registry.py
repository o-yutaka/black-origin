from __future__ import annotations
from typing import Dict, Any


def run_stream_registry(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["stream_registry"] = "ok"
    return result
