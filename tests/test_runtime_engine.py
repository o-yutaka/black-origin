from __future__ import annotations

import asyncio
import unittest

from black_origin.engine import RuntimeEngine
from black_origin.event_bus import Event


class RuntimeEngineTests(unittest.IsolatedAsyncioTestCase):
    async def test_event_bus_delivers_messages(self) -> None:
        engine = RuntimeEngine(tick_interval=0.01)
        received: list[Event] = []

        async def collector(event: Event) -> None:
            received.append(event)
            engine.stop()

        engine.bus.subscribe("agent.messages", collector)

        task = asyncio.create_task(engine.run())
        await asyncio.wait_for(task, timeout=1)

        self.assertTrue(received)
        self.assertEqual(received[0].topic, "agent.messages")


if __name__ == "__main__":
    unittest.main()
