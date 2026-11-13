# Network resilience simulator

This project models a real-time media pipeline in 10 ms ticks: a sender produces audio units, a network may stall or recover, a bounded queue applies backpressure, and a receiver consumes one unit per tick. It reports delivery, drops, receiver underruns, and maximum queue depth.

```bash
python3 resilience_simulator.py
../.tooling/pixi/pixi run mojo resilience_simulator.mojo
```

## What happens during a simulation

The deterministic scenario contains three realistic stresses:

1. A sender burst produces two units instead of one.
2. A temporary network outage stops delivery for several ticks.
3. The queue has a strict capacity, so excess work is dropped rather than consuming unbounded memory.

The receiver starts with a small jitter buffer. It consumes one media unit every tick; if the buffer is empty, an **underrun** occurs—the event that would become an audible gap or frozen video frame in a real product.

## Why this is useful at a company

This is a deterministic, explainable test harness for questions such as: “How large should the jitter buffer be?”, “What happens during a 100 ms outage?”, “Do we drop old data or let latency grow?”, and “How do bursty producers affect a bounded service queue?” The simplified policy can be evolved into a replay tool for production traces or a regression test for a transport, media, or backend queueing change.

## Mojo versus Python

| Concern | Python | Mojo |
|---|---|---|
| Role | An easy-to-review model for testing policies and explaining behavior. | A compiled state-machine kernel with explicit integer counters. |
| State updates | Dynamic integers and normal assignment keep experimentation friction low. | Typed `Int` state makes the loop's representation and cost predictable. |
| Production evolution | Good for offline replay, plotting, and policy iteration. | Suitable for a high-volume simulation service or a performance-sensitive embedded loop after profiling. |
| Important shared idea | Both make queue capacity, outage behavior, and underrun policy explicit. | Both make queue capacity, outage behavior, and underrun policy explicit. |

The goal is not to claim that Mojo replaces a full discrete-event simulation platform. It demonstrates how a small, well-specified state machine can start in readable Python and later become compiled Mojo if it must process many what-if scenarios or operate in a latency-sensitive path.

## Extension ideas

- Parameterize the outage, queue capacity, burst rate, and initial jitter-buffer target from a scenario file.
- Compare “drop newest,” “drop oldest,” and adaptive bitrate policies.
- Run thousands of seeded scenarios and produce percentile latency/underrun reports.
- Replay production-safe, anonymized transport metrics to validate a change before rollout.

## Plain English: what is the point, and what does Mojo add?

Think of a media stream as small pieces of audio arriving in a queue. This program asks what happens if the sender gets ahead, the network pauses, or the queue fills up. It counts pieces delivered, pieces dropped, and moments when the receiver has nothing to play. Engineers can use a richer version to compare buffering and queue policies before changing a real service.

Here the network is simulated with simple fixed rules; this is not a full network emulator and it does not predict a real customer's call. The Mojo version runs the same small state machine as compiled code with explicit integer state. That is useful for learning how a hot simulation loop can be expressed in Mojo. The demo does not measure a speedup; the likely benefit would matter when running many larger scenarios, after profiling. Python remains convenient for changing scenarios and analyzing results.
