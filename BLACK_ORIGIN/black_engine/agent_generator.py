from __future__ import annotations
from typing import Dict, Any


def run_agent_generator(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["agent_generator"] = "ok"
    return result
