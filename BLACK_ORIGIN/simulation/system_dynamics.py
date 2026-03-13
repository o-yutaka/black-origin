from __future__ import annotations

from typing import Any, Dict


def run_system_dynamics(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    stocks = dict(result.get("stocks", {"capacity": 1.0, "demand": 1.0}))
    flows = dict(result.get("flows", {"capacity": 0.05, "demand": 0.03}))
    for key, flow in flows.items():
        stocks[key] = stocks.get(key, 0.0) + float(flow)
    result["system_dynamics"] = {"stocks": stocks, "flows": flows}
    return result
