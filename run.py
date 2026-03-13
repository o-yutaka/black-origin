from __future__ import annotations
import threading
import time
from BLACK_ORIGIN.kernel.system import BlackOriginSystem
from BLACK_ORIGIN.ui.server import run_server


def main() -> None:
    system = BlackOriginSystem()
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(0.2)
    system.run(cycles=2)
    print("UI running on http://localhost:8080")
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
