from __future__ import annotations

from core.models import TaskStatus
from runtime.agent_messaging import AgentMessenger
from runtime.event_bus import EventBus
from task_engine.task_memory import TaskMemory


class TaskExecutor:
    def __init__(self, event_bus: EventBus, task_memory: TaskMemory, messenger: AgentMessenger) -> None:
        self._event_bus = event_bus
        self._task_memory = task_memory
        self._messenger = messenger

    def assign_agent(self, task_id: str) -> str:
        task = self._task_memory.get_task(task_id)
        capability = task.metadata.get("capability", "general")
        agent_id = self._messenger.find_agent(capability)
        if not agent_id:
            raise RuntimeError(f"No agent found for capability '{capability}'")
        task.assigned_agent = agent_id
        task.status = TaskStatus.ASSIGNED
        self._event_bus.publish("task.assigned", {"task_id": task.task_id, "agent_id": agent_id})
        return agent_id

    def execute(self, task_id: str) -> None:
        task = self._task_memory.get_task(task_id)
        if not task.assigned_agent:
            self.assign_agent(task_id)
        task.status = TaskStatus.RUNNING
        self._event_bus.publish("task.started", {"task_id": task.task_id, "agent_id": task.assigned_agent})
        self._messenger.send_task(
            task.assigned_agent,
            {"task_id": task.task_id, "goal_id": task.goal_id, "description": task.description},
        )
        task.status = TaskStatus.COMPLETED
        task.progress = 1.0
        self._event_bus.publish("task.completed", {"task_id": task.task_id, "goal_id": task.goal_id})
