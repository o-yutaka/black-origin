from __future__ import annotations

from typing import Dict, List


def generate_scenarios(base: Dict[str, float], perturbation: float = 0.1) -> List[Dict[str, float]]:
    scenarios: List[Dict[str, float]] = []
    for direction in (-1, 0, 1):
        scenarios.append({key: value * (1 + direction * perturbation) for key, value in base.items()})
    return scenarios
