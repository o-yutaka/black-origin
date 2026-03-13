from __future__ import annotations
from typing import Dict, Any


def run_lifecycle(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["lifecycle"] = "ok"
    return result
