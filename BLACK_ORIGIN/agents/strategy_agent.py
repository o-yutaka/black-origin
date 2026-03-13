from __future__ import annotations

from typing import Any, Dict


def run_strategy_agent(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    projected = float(result.get("projected", 1.0))
    result["strategy_agent"] = {
        "action": "scale" if projected > 1.0 else "stabilize",
        "confidence": min(0.95, 0.5 + abs(projected - 1.0)),
    }
    return result
