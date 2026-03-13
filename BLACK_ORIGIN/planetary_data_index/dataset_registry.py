from __future__ import annotations
from typing import Dict, Any


def run_dataset_registry(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["dataset_registry"] = "ok"
    return result
