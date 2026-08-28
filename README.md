# BLACK ORIGIN

BLACK ORIGIN is a modular civilization-scale AI operating system composed of interoperable subsystems that execute a continuous intelligence loop:

`observe -> discover -> ingest -> learn -> reason -> simulate -> research -> decide -> act -> evolve -> generate -> design`

## Quick start

1. Clone the repository.
2. Copy `.env.example` to `.env`.
3. Add your OpenAI key to `OPENAI_API_KEY`.
4. Run:

```bash
python run.py
```

The runtime starts core cycles and serves the dark UI at `http://localhost:8080`.

## Architecture

- `BLACK_ORIGIN/kernel`: lifecycle and intelligence loop runtime.
- `BLACK_ORIGIN/planetary_data_index` ... `BLACK_ORIGIN/civilization`: subsystem modules with executable processors and component functions.
- `BLACK_ORIGIN/knowledge_graph`: entity/relation extraction plus a durable SQLite-backed global graph shared across intelligence cycles.
- `BLACK_ORIGIN/ui`: built-in HTTP UI with hamburger navigation, animations, and live telemetry endpoints.

All subsystems expose executable logic and are chained by the kernel into the intelligence loop.

## Persistent intelligence state

BLACK ORIGIN stores its durable knowledge graph in `.black_origin/knowledge_graph.sqlite3` by default. Set `BLACK_ORIGIN_STATE_DIR` to move runtime state elsewhere. The store is bounded and ranked by repeated observations so long-running cycles retain useful knowledge without unbounded growth.
