from __future__ import annotations

from hashlib import md5


class CrawlerEngine:
    name = "crawler"

    SOURCES = [
        ("news", "Reuters climate pulse"),
        ("scientific", "ArXiv earth systems"),
        ("satellite", "NASA MODIS feed"),
        ("economic", "World Bank indicators"),
        ("climate", "NOAA climate normals"),
        ("government", "EU open data portal"),
        ("public_api", "UN data api"),
        ("technology", "GitHub global ai trends"),
    ]

    def run(self, context: dict[str, object]) -> dict[str, object]:
        cycle = int(context.get("cycle", 0))
        discoveries: list[dict[str, object]] = []
        for category, source in self.SOURCES:
            sig = f"{category}-{source}-{cycle}".encode()
            discoveries.append(
                {
                    "dataset_id": md5(sig).hexdigest()[:12],
                    "category": category,
                    "source": source,
                    "url": f"https://data.blackorigin.ai/{category}/{cycle}",
                    "reliability": round(0.65 + ((cycle + len(category)) % 25) / 100, 2),
                }
            )
        return {"discoveries": discoveries, "count": len(discoveries)}
