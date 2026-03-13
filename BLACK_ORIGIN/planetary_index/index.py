from __future__ import annotations

from collections import defaultdict
from statistics import mean

from BLACK_ORIGIN.core.models import DatasetRecord


class PlanetaryDataIndex:
    def __init__(self) -> None:
        self.datasets: dict[str, DatasetRecord] = {}
        self.by_category: dict[str, set[str]] = defaultdict(set)

    def register(self, record: DatasetRecord) -> None:
        self.datasets[record.dataset_id] = record
        self.by_category[record.category].add(record.dataset_id)

    def reliability_by_category(self) -> dict[str, float]:
        return {
            category: mean(self.datasets[d].reliability for d in dataset_ids)
            for category, dataset_ids in self.by_category.items()
            if dataset_ids
        }

    def summary(self) -> dict[str, object]:
        return {
            "total": len(self.datasets),
            "categories": {k: len(v) for k, v in self.by_category.items()},
            "reliability": self.reliability_by_category(),
        }
