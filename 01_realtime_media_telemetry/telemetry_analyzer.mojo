"""Compiled version of the RTP-style stream-quality analysis."""

def absolute(value: Float64) -> Float64:
    if value < 0.0:
        return -value
    return value


def main():
    var previous_transit: Float64 = 0.0
    var jitter: Float64 = 0.0
    var expected_sequence: Int = 1
    var lost: Int = 0
    var late_arrivals: Int = 0

    for packet in range(1, 1001):
        var received_sequence = packet
        if packet % 53 == 0:
            received_sequence += 1
        if received_sequence > expected_sequence:
            lost += received_sequence - expected_sequence
        expected_sequence = received_sequence + 1

        var sender_ms = Float64(packet * 20)
        var variation = Float64(packet % 7 - 3) * 1.75
        if packet >= 320 and packet <= 335:
            variation += 55.0
        var arrival_ms = sender_ms + 18.0 + variation
        var transit = arrival_ms - sender_ms
        var delta = absolute(transit - previous_transit)
        jitter += (delta - jitter) / 16.0
        if delta > 20.0:
            late_arrivals += 1
        previous_transit = transit

    var loss_percent = 100.0 * Float64(lost) / 1000.0
    var escalate = loss_percent >= 1.0 or jitter >= 8.0
    print("packets:", 1000)
    print("lost packets:", lost)
    print("loss percent:", loss_percent)
    print("smoothed jitter (ms):", jitter)
    print("late-arrival events:", late_arrivals)
    print("escalate investigation:", escalate)
