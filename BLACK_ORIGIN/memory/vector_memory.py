from __future__ import annotations

from math import sqrt
from typing import Any, Dict, Iterable, List


def _embed(text: str) -> List[float]:
    buckets = [0.0, 0.0, 0.0, 0.0]
    for idx, ch in enumerate(text.lower()):
        buckets[idx % 4] += (ord(ch) - 96) / 26.0 if "a" <= ch <= "z" else 0.05
    norm = sqrt(sum(v * v for v in buckets)) or 1.0
    return [v / norm for v in buckets]


def cosine_similarity(a: Iterable[float], b: Iterable[float]) -> float:
    a_list, b_list = list(a), list(b)
    return sum(x * y for x, y in zip(a_list, b_list))


def run_vector_memory(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    text = result.get("text", "")
    query = result.get("query", text)
    text_vec, query_vec = _embed(text), _embed(query)
    result["vector_memory"] = {"embedding": text_vec, "similarity": cosine_similarity(text_vec, query_vec)}
    return result
