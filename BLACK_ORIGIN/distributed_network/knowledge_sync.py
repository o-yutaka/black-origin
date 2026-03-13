from __future__ import annotations
from typing import Dict, Any


def run_knowledge_sync(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["knowledge_sync"] = "ok"
    return result
