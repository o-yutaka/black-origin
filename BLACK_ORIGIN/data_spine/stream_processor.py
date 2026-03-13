from __future__ import annotations
from typing import Dict, Any


def run_stream_processor(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["stream_processor"] = "ok"
    return result
