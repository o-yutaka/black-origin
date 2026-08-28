from __future__ import annotations

import hashlib
import json
from typing import Any, List, Tuple

from BLACK_ORIGIN.recomposition.models import AtomicComponent


def _stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def _component_id(path: str, kind: str, value: Any) -> str:
    payload = f"{path}|{kind}|{_stable_json(value)}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def _kind(value: Any) -> str:
    if isinstance(value, dict):
        return "mapping"
    if isinstance(value, (list, tuple)):
        return "sequence"
    if isinstance(value, set):
        return "set"
    if value is None:
        return "null"
    return type(value).__name__


class StructuralDecomposer:
    """Deterministically decompose arbitrary nested state into bounded atoms.

    This is intentionally domain-neutral: code, prompts, plans, memories and
    architecture descriptions can all be represented as nested values and fed
    through the same decomposition contract.
    """

    def __init__(self, max_depth: int = 8, max_components: int = 512):
        if max_depth < 0:
            raise ValueError("max_depth must be non-negative")
        if max_components < 1:
            raise ValueError("max_components must be positive")
        self.max_depth = max_depth
        self.max_components = max_components

    def decompose(self, value: Any) -> Tuple[List[AtomicComponent], List[Tuple[str, str]]]:
        components: List[AtomicComponent] = []
        edges: List[Tuple[str, str]] = []

        def visit(item: Any, path: str, parent_path: str | None, depth: int) -> None:
            if len(components) >= self.max_components:
                return
            kind = _kind(item)
            component = AtomicComponent(
                component_id=_component_id(path, kind, item),
                path=path,
                kind=kind,
                value=item,
                parent_path=parent_path,
                depth=depth,
            )
            components.append(component)
            if parent_path is not None:
                edges.append((parent_path, path))
            if depth >= self.max_depth:
                return

            if isinstance(item, dict):
                for key in sorted(item, key=lambda raw: str(raw)):
                    visit(item[key], f"{path}.{key}", path, depth + 1)
                    if len(components) >= self.max_components:
                        return
            elif isinstance(item, (list, tuple)):
                for index, child in enumerate(item):
                    visit(child, f"{path}[{index}]", path, depth + 1)
                    if len(components) >= self.max_components:
                        return
            elif isinstance(item, set):
                for index, child in enumerate(sorted(item, key=lambda raw: str(raw))):
                    visit(child, f"{path}{{{index}}}", path, depth + 1)
                    if len(components) >= self.max_components:
                        return

        visit(value, "$", None, 0)
        return components, edges
