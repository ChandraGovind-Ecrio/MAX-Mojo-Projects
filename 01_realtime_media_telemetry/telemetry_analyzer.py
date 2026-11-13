"""Deterministic RTP-style stream-quality analysis; standard library only."""

PACKETS = 1_000


def absolute(value: float) -> float:
    return -value if value < 0.0 else value


previous_transit = 0.0
jitter = 0.0
expected_sequence = 1
lost = 0
late_arrivals = 0

for packet in range(1, PACKETS + 1):
    received_sequence = packet + (1 if packet % 53 == 0 else 0)
    if received_sequence > expected_sequence:
        lost += received_sequence - expected_sequence
    expected_sequence = received_sequence + 1

    sender_ms = float(packet * 20)
    variation = float(packet % 7 - 3) * 1.75
    if 320 <= packet <= 335:
        variation += 55.0
    arrival_ms = sender_ms + 18.0 + variation
    transit = arrival_ms - sender_ms
    delta = absolute(transit - previous_transit)
    jitter += (delta - jitter) / 16.0
    if delta > 20.0:
        late_arrivals += 1
    previous_transit = transit

loss_percent = 100.0 * lost / PACKETS
escalate = loss_percent >= 1.0 or jitter >= 8.0
print("packets:", PACKETS)
print("lost packets:", lost)
print("loss percent:", loss_percent)
print("smoothed jitter (ms):", jitter)
print("late-arrival events:", late_arrivals)
print("escalate investigation:", escalate)
