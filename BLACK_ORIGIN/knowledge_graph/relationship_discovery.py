from __future__ import annotations
from typing import Dict, Any


def run_relationship_discovery(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["relationship_discovery"] = "ok"
    return result
