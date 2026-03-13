# BLACK ORIGIN Continuous Runtime Engine

This repository now includes a continuous, event-driven runtime engine with:

- **Event bus** for publish/subscribe coordination
- **Signal system** for graceful shutdown on `SIGINT` / `SIGTERM`
- **Agent messaging** between runtime subsystems
- **Continuous runtime loop** that orchestrates subsystems automatically

## Run

```bash
python main.py
```

The engine will run continuously until interrupted.

## Test

```bash
python -m unittest discover -s tests
```
