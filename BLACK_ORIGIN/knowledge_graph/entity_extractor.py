from __future__ import annotations
from typing import Dict, Any


def run_entity_extractor(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["entity_extractor"] = "ok"
    return result
