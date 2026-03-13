from __future__ import annotations


class DataPipelineEngine:
    name = "pipeline"

    def run(self, context: dict[str, object]) -> dict[str, object]:
        discoveries = context.get("crawler_execution", {}).get("discoveries", [])
        normalized = [
            {
                **item,
                "normalized_source": str(item["source"]).lower().replace(" ", "_"),
                "ingested": True,
            }
            for item in discoveries
        ]
        return {"records": normalized, "ingested_count": len(normalized)}
