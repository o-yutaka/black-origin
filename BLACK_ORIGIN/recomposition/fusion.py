from __future__ import annotations

import hashlib
from typing import Dict, Iterable, List, Sequence

from BLACK_ORIGIN.recomposition.models import AtomicComponent, ReconstructionPlan


class CrossBranchFusion:
    """Construct a reconstruction plan without mutating stable state.

    The planner keeps one component per structural path. When multiple branches
    contribute the same path, the first parent in priority order wins unless an
    explicit component score is provided.
    """

    def build_plan(
        self,
        parent_ids: Sequence[str],
        components_by_parent: Dict[str, Iterable[AtomicComponent]],
        component_scores: Dict[str, float] | None = None,
    ) -> ReconstructionPlan:
        if len(parent_ids) < 2:
            raise ValueError("cross-branch fusion requires at least two parents")
        scores = component_scores or {}
        selected_by_path: Dict[str, tuple[float, int, AtomicComponent]] = {}
        source_by_component: Dict[str, str] = {}

        for parent_index, parent_id in enumerate(parent_ids):
            for component in components_by_parent.get(parent_id, []):
                score = float(scores.get(component.component_id, 0.0))
                current = selected_by_path.get(component.path)
                candidate_key = (score, -parent_index)
                if current is None or candidate_key > (current[0], current[1]):
                    selected_by_path[component.path] = (score, -parent_index, component)
                    source_by_component[component.component_id] = parent_id

        selected = [row[2] for row in sorted(selected_by_path.values(), key=lambda item: item[2].path)]
        fingerprint = "|".join(parent_ids) + "|" + "|".join(component.component_id for component in selected)
        plan_id = "plan_" + hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()[:20]
        return ReconstructionPlan(
            plan_id=plan_id,
            parent_ids=tuple(parent_ids),
            selected_components=tuple(component.component_id for component in selected),
            metadata={
                "component_sources": {
                    component.component_id: source_by_component.get(component.component_id, "unknown")
                    for component in selected
                },
                "paths": {component.component_id: component.path for component in selected},
            },
        )
