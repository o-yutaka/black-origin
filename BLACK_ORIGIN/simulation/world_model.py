from __future__ import annotations

from typing import Dict


def evolve_world_state(state: Dict[str, float], actions: Dict[str, float]) -> Dict[str, float]:
    next_state = dict(state)
    for key, delta in actions.items():
        next_state[key] = next_state.get(key, 0.0) + delta
    return next_state
