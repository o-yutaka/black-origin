from __future__ import annotations

from typing import Any, Dict


def run_analysis_agent(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    observations = result.get("observations", [])
    mean_signal = sum(item.get("signal", 0.0) for item in observations) / max(len(observations), 1)
    result["analysis_agent"] = {"mean_signal": mean_signal, "insight_count": len(observations)}
    return result
