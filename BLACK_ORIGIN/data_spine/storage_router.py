from __future__ import annotations
from typing import Dict, Any


def run_storage_router(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["storage_router"] = "ok"
    return result
