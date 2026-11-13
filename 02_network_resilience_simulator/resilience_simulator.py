"""A deterministic queue, jitter-buffer, and outage simulation."""

TICKS = 600
QUEUE_LIMIT = 12
queue_depth = 0
receiver_buffer = 4
max_queue_depth = 0
sent = delivered = dropped = underruns = 0

for tick in range(TICKS):
    produced = 2 if 120 <= tick < 150 else 1
    sent += produced
    available = max(0, QUEUE_LIMIT - queue_depth)
    accepted = min(produced, available)
    dropped += produced - accepted
    queue_depth += accepted

    outage = 260 <= tick < 278
    network_capacity = 0 if outage else (2 if tick % 9 == 0 else 1)
    delivered_now = min(queue_depth, network_capacity)
    queue_depth -= delivered_now
    delivered += delivered_now
    receiver_buffer += delivered_now
    max_queue_depth = max(max_queue_depth, queue_depth)

    if receiver_buffer > 0:
        receiver_buffer -= 1
    else:
        underruns += 1

print("ticks:", TICKS)
print("units sent:", sent)
print("units delivered:", delivered)
print("units dropped by bounded queue:", dropped)
print("receiver underruns:", underruns)
print("maximum queue depth:", max_queue_depth)
print("final receiver buffer:", receiver_buffer)
