from __future__ import annotations

import asyncio
import signal
from typing import Callable


class SignalSystem:
    """Connect OS signals to runtime stop callbacks."""

    def __init__(self, stop_callback: Callable[[], None]) -> None:
        self._stop_callback = stop_callback

    def install(self) -> None:
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, self._stop_callback)
            except NotImplementedError:
                signal.signal(sig, lambda *_: self._stop_callback())
