from __future__ import annotations

from copy import deepcopy
from typing import Dict, Iterable, Mapping

from BLACK_ORIGIN.recomposition.models import AtomicComponent, ReconstructionPlan


_CONTAINER_KINDS = {"mapping", "sequence", "set"}


class ReconstructionMaterializer:
    """Turn a persisted fusion plan into a new JSON-like value.

    Materialization follows the selected component at every structural path.
    Container nodes define the shape; leaf nodes provide the values. This avoids
    replacing the root with one parent's entire object and allows true cross-
    branch reconstruction.

    Sets are intentionally unsupported: their decomposition paths use sorted
    positional indices, which are not stable enough to support safe member-wise
    recomposition after persistence.
    """

    def materialize(
        self,
        plan: ReconstructionPlan,
        components_by_parent: Mapping[str, Iterable[AtomicComponent]],
    ) -> object:
        component_by_id: Dict[str, AtomicComponent] = {}
        by_parent_path: Dict[str, Dict[str, AtomicComponent]] = {}
        for parent_id in plan.parent_ids:
            path_map: Dict[str, AtomicComponent] = {}
            for component in components_by_parent.get(parent_id, ()):
                path_map[component.path] = component
                component_by_id.setdefault(component.component_id, component)
            by_parent_path[parent_id] = path_map

        selected_by_path: Dict[str, AtomicComponent] = {}
        for component_id in plan.selected_components:
            component = component_by_id.get(component_id)
            if component is None:
                raise KeyError(f"selected component missing from parents: {component_id}")
            selected_by_path[component.path] = component

        root = selected_by_path.get("$")
        if root is None:
            raise ValueError("reconstruction plan has no selected root component")

        def materialize_path(path: str) -> object:
            selected = selected_by_path.get(path)
            if selected is None:
                raise KeyError(f"selected structural path missing: {path}")

            if selected.kind not in _CONTAINER_KINDS:
                return deepcopy(selected.value)

            if selected.kind == "set":
                raise TypeError(
                    f"set materialization is unsupported for path {path}; "
                    "treat the set as an opaque resource or normalize it before decomposition"
                )

            if selected.kind == "mapping":
                keys: list[str] = []
                seen: set[str] = set()
                for parent_id in plan.parent_ids:
                    container = by_parent_path[parent_id].get(path)
                    if container is None or container.kind != "mapping" or not isinstance(container.value, dict):
                        continue
                    for raw_key in container.value:
                        key = str(raw_key)
                        child_path = f"{path}.{key}"
                        if child_path in selected_by_path and key not in seen:
                            seen.add(key)
                            keys.append(key)
                result: dict[str, object] = {}
                for key in keys:
                    result[key] = materialize_path(f"{path}.{key}")
                return result

            # Tuples and lists share the "sequence" decomposition kind. The
            # durable reconstruction format deliberately normalizes both to list.
            indices: list[int] = []
            index = 0
            while f"{path}[{index}]" in selected_by_path:
                indices.append(index)
                index += 1
            return [materialize_path(f"{path}[{index}]") for index in indices]

        return materialize_path("$")
