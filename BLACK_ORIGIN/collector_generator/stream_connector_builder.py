from __future__ import annotations
from typing import Dict, Any


def run_stream_connector_builder(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["stream_connector_builder"] = "ok"
    return result
