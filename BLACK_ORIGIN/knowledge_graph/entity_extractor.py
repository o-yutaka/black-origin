from __future__ import annotations

import re
from typing import Any, Dict, List

TOKEN_PATTERN = re.compile(
    r"\b[A-Za-z][A-Za-z0-9_-]{1,}\b|[一-龥ぁ-んァ-ヶー]{2,}"
)

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "has", "have", "in", "is", "it", "of", "on", "or", "that", "the",
    "this", "to", "was", "were", "will", "with",
}


def extract_entities(text: str) -> List[str]:
    entities: Dict[str, str] = {}
    for token in TOKEN_PATTERN.findall(text):
        canonical = token.casefold()
        if canonical in STOPWORDS:
            continue
        entities.setdefault(canonical, token)
    return sorted(entities.values(), key=str.casefold)


def run_entity_extractor(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    text = result.get("text", "")
    entities = extract_entities(str(text))
    result["entity_extractor"] = {"entities": entities, "count": len(entities)}
    return result
