from __future__ import annotations
from typing import Dict, Any


def run_crawler_builder(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["crawler_builder"] = "ok"
    return result
