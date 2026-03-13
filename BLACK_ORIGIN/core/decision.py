from __future__ import annotations


class DecisionEngine:
    name = "decision"

    def run(self, context: dict[str, object]) -> dict[str, object]:
        forecast = float(context.get("planetary_simulation", {}).get("impact_forecast", 0.0))
        recommendation = "accelerate_green_infrastructure" if forecast >= 0.5 else "increase_data_collection"
        return {
            "scenario_evaluation": forecast,
            "policy_recommendation": recommendation,
            "optimization_target": "planetary_resilience",
        }
