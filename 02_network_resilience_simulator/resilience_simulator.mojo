"""Compiled version of the deterministic queue and jitter-buffer simulation."""

def main():
    var queue_depth: Int = 0
    var receiver_buffer: Int = 4
    var max_queue_depth: Int = 0
    var sent: Int = 0
    var delivered: Int = 0
    var dropped: Int = 0
    var underruns: Int = 0

    for tick in range(600):
        var produced: Int = 1
        if tick >= 120 and tick < 150:
            produced = 2
        sent += produced

        var available = 12 - queue_depth
        if available < 0:
            available = 0
        var accepted = produced
        if accepted > available:
            accepted = available
        dropped += produced - accepted
        queue_depth += accepted

        var network_capacity: Int = 1
        if tick >= 260 and tick < 278:
            network_capacity = 0
        elif tick % 9 == 0:
            network_capacity = 2
        var delivered_now = queue_depth
        if delivered_now > network_capacity:
            delivered_now = network_capacity
        queue_depth -= delivered_now
        delivered += delivered_now
        receiver_buffer += delivered_now
        if queue_depth > max_queue_depth:
            max_queue_depth = queue_depth

        if receiver_buffer > 0:
            receiver_buffer -= 1
        else:
            underruns += 1

    print("ticks:", 600)
    print("units sent:", sent)
    print("units delivered:", delivered)
    print("units dropped by bounded queue:", dropped)
    print("receiver underruns:", underruns)
    print("maximum queue depth:", max_queue_depth)
    print("final receiver buffer:", receiver_buffer)
