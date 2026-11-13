# Real-time media telemetry analyzer

This project is a small stream-health kernel for an RTP/WebRTC-style media session. It processes 1,000 synthetic packet arrivals and reports loss, jitter, late-arrival events, and whether the stream should be escalated for investigation. It represents the same class of arithmetic a media-quality service performs continuously for many active calls.

```bash
python3 telemetry_analyzer.py
../.tooling/pixi/pixi run mojo telemetry_analyzer.mojo
```

## What the analyzer measures

Each packet has an expected sequence number, an ideal sender timestamp, and an observed arrival time.

- A sequence gap is counted as packet loss.
- **Transit time** is arrival time minus sender time.
- **Inter-arrival jitter** tracks how much transit time changes from one packet to the next, using the same smoothing idea commonly used in RTP monitoring.
- A large change in transit time is counted as a late-arrival event.
- The final policy raises an escalation flag if loss or jitter crosses a chosen service-quality threshold.

The packet stream is deliberately deterministic: it contains isolated loss and a short burst of timing disruption. That makes it useful as a repeatable regression case—both implementations should report the same metrics.

## Why this is useful at a company

In a communication or real-time product, these metrics can drive a quality dashboard, alerting, adaptive bitrate decisions, customer-support evidence, or a call-quality score. The next practical step would be to feed the same kernel real telemetry exported from a gateway, SFU, client SDK, or log stream.

## Mojo versus Python

| Concern | Python | Mojo |
|---|---|---|
| Role | Clear reference implementation and easy integration with log/HTTP tooling. | Compiled implementation of the tight numerical stream-processing loop. |
| Numeric values | Python objects whose operations are resolved at runtime. | Explicit `Int` counters and `Float64` timing arithmetic. |
| Scaling path | Often uses NumPy, Numba, Cython, or a native extension when load grows. | Can remain in one language while adding SIMD or parallel stream partitioning after profiling. |
| Best use | Product glue, experiments, analysis scripts, and lower-volume processing. | Hot-path analysis when many streams or packets must be scored with predictable overhead. |

The Mojo version is not automatically a production replacement for Python. The valuable idea is architectural: keep the application and integrations in Python if that is productive, and move the measured compute bottleneck into a compiled Mojo component only when profiling justifies it.

## Extension ideas

- Replace the synthetic generator with CSV, JSON, or live RTP statistics.
- Keep per-call rolling windows and publish an alert only after sustained degradation.
- Add codec, region, network type, or customer tier as labels for aggregate analysis.
- Benchmark a batch of thousands of concurrent streams before deciding whether SIMD or parallelism is needed.

## Plain English: what is the point, and what does Mojo add?

Imagine a live call is choppy. This program acts like a tiny call-quality meter: it looks at packet numbers and arrival times, then reports whether packets went missing or arrived unevenly. A real service could use the same measurements to help support teams find bad calls or to trigger a network-quality alert.

The example creates pretend packet data, so it is a demonstration, not a real monitoring product. Its value for learning Mojo is that it puts the repeated math in a compiled language with explicit number types. That gives Mojo a plausible speed advantage when the same work runs at very large scale. We have not benchmarked it against Python here, so this project shows the shape of a suitable Mojo workload, not proof of a speedup. Python is still useful for reading logs, connecting services, and building dashboards.
