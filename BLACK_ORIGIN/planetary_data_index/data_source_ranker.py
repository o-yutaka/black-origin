from __future__ import annotations
from typing import Dict, Any


def run_data_source_ranker(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["data_source_ranker"] = "ok"
    return result
