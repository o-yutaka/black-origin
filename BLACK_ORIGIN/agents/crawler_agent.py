from __future__ import annotations

from typing import Any, Dict


def run_crawler_agent(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    seeds = result.get("seed_urls", [])
    observations = [{"url": url, "signal": len(url) / 100.0} for url in seeds]
    result["crawler_agent"] = {"observations": observations, "count": len(observations)}
    return result
