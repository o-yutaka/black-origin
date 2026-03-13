from __future__ import annotations
from typing import Dict, Any


def run_dataset_crawler(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["dataset_crawler"] = "ok"
    return result
