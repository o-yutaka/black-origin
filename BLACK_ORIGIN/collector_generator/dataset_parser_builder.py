from __future__ import annotations
from typing import Dict, Any


def run_dataset_parser_builder(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["dataset_parser_builder"] = "ok"
    return result
