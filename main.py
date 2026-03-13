from __future__ import annotations

import asyncio

from black_origin import RuntimeEngine


async def main() -> None:
    engine = RuntimeEngine(tick_interval=1.0)
    await engine.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
