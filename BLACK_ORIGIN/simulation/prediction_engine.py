from __future__ import annotations

from typing import Dict, List


def forecast_metric(history: List[float], horizon: int = 3) -> List[float]:
    if not history:
        return [0.0] * horizon
    trend = history[-1] - history[-2] if len(history) > 1 else 0.0
    return [history[-1] + trend * step for step in range(1, horizon + 1)]


def run_prediction_engine(context: Dict[str, object]) -> Dict[str, object]:
    result = dict(context)
    history = [float(x) for x in result.get("history", [1.0, 1.1, 1.2])]
    result["prediction_engine"] = {"forecast": forecast_metric(history), "horizon": 3}
    return result
