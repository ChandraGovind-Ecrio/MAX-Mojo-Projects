# Mojo + MAX systems demos

These are compact, company-oriented systems demos rather than generic ML notebooks. They show where Mojo and MAX fit in a communications, media, or backend product:

| Lab | Idea | What it teaches |
|---|---|---|
| `01_realtime_media_telemetry` | RTP-style stream health analyzer | Typed numerical hot loops and service-quality signals |
| `02_network_resilience_simulator` | Jitter-buffer and backpressure simulator | Mutable state, queueing, outages, and deterministic replay |
| `03_max_incident_copilot` | Structured incident-triage API | MAX model serving with a safe Python application layer |

Mojo is a programming language and compiler/runtime ecosystem—it is **not an OS**. MAX is Modular's inference stack. Neither is a promise that no CUDA is ever involved: MAX can use GPU backends when available, but you use its higher-level commands/APIs rather than authoring CUDA kernels yourself.

## How to read the comparisons

The first two folders hold the same algorithm twice: a straightforward, standard-library Python reference and a Mojo implementation. The Python file is the most approachable statement of the idea; the Mojo file exposes types, ownership, and compiled execution. They should produce the same kind of terminal art, but they are not intended to be a rigorous benchmark—terminal output, machine architecture, and compiler version can easily dominate a tiny timing test.

The third folder is different: its Python file is a deliberately minimal client, while MAX is the engine that loads and runs the neural network behind an HTTP server. It demonstrates a practical division of responsibility: Python for application orchestration, MAX for high-performance inference.

## Run the installed Mojo labs

Modular recommends [Pixi](https://docs.modular.com/pixi) for project environments. Pixi is already installed locally for this workspace at `.tooling/pixi/pixi`. From this directory:

```bash
cd 01_ascii_mandelbrot
../.tooling/pixi/pixi run mojo mandelbrot.mojo
```

Each Mojo lab has its own `pixi.toml`; the local Pixi command resolves `mojo` automatically. The Python counterparts use only Python's standard library and run now with `python3`.

## Suggested order

Start with the telemetry analyzer, then the resilience simulator. Read each `README.md` after running both implementations. Finish with the MAX incident copilot once you want to run a real local model.
