from __future__ import annotations

from typing import Any, Dict


def run_simulation_agent(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    baseline = float(result.get("baseline", 1.0))
    result["simulation_agent"] = {"projected": baseline * 1.1, "delta": baseline * 0.1}
    return result
