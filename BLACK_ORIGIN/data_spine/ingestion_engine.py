from __future__ import annotations
from typing import Dict, Any


def run_ingestion_engine(context: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(context)
    result["ingestion_engine"] = "ok"
    return result
