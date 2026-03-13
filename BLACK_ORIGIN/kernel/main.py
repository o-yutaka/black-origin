from __future__ import annotations

import argparse
import json

from BLACK_ORIGIN.kernel.runtime import build_runtime


def main() -> None:
    parser = argparse.ArgumentParser(description="Run BLACK ORIGIN planetary loop")
    parser.add_argument("--cycles", type=int, default=1)
    args = parser.parse_args()

    runtime = build_runtime()
    for _ in range(args.cycles):
        context = runtime.run_cycle()
        print(json.dumps({"cycle": context["cycle"], "stages": len(context.keys()) - 1}))


if __name__ == "__main__":
    main()
