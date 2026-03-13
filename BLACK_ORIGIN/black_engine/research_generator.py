from __future__ import annotations
from typing import Dict, Any


def run_research_generator(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["research_generator"] = "ok"
    return result
