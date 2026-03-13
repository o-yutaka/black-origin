from __future__ import annotations

import re
from typing import Any, Dict, List


ENTITY_PATTERN = re.compile(r"\b[A-Z][a-zA-Z0-9_-]{2,}\b")


def extract_entities(text: str) -> List[str]:
    return sorted(set(ENTITY_PATTERN.findall(text)))


def run_entity_extractor(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    text = result.get("text", "")
    entities = extract_entities(text)
    result["entity_extractor"] = {"entities": entities, "count": len(entities)}
    return result
