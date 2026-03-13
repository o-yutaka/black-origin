# Black Origin Runtime Engines

This repository includes a **Task Intelligence Engine** and a **Goal Generation Engine** integrated with a runtime event bus and agent messaging system.

## Core capabilities

- Goal creation
- Task decomposition
- Task graph execution
- Agent assignment
- Task progress tracking
- Goal evaluation

## Main modules

- `task_engine/`
  - `task_manager.py`
  - `task_planner.py`
  - `task_graph.py`
  - `task_executor.py`
  - `task_scheduler.py`
  - `task_memory.py`
- `goal_engine/`
  - `goal_generator.py`
  - `goal_evaluator.py`
  - `goal_memory.py`
  - `goal_scheduler.py`
- `runtime/runtime_engine.py`
- `runtime/event_bus.py`
- `runtime/agent_messaging.py`

## Minimal usage

```python
from runtime import Agent, RuntimeEngine

engine = RuntimeEngine()
engine.register_agents([Agent(agent_id="agent-1", capability="general")])
goal = engine.create_goal(
    title="Launch release",
    description="Gather requirements. Build release notes. Publish package.",
    success_criteria=["all tasks complete"],
)
evaluation = engine.run_goal(goal.goal_id)
print(evaluation.passed, evaluation.score)
```
