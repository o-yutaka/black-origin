from __future__ import annotations
from typing import Dict, Any


def run_crawler_agent(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["crawler_agent"] = "ok"
    return result
