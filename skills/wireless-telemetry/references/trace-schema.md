# Offline trace schema v1

Use UTF-8 CSV with this exact header order:

```csv
schema_version,kind,session_id,stream,boot_id,seq,rx_ms,clock_id,request_id,request_ms,reply_ms,tx_clock_id
1,telemetry,bench-1,status,boot-a,1,100,pc-monotonic,,,,
1,telemetry,bench-1,status,boot-a,2,120,pc-monotonic,,,,
1,rtt,bench-1,,,,,pc-monotonic,req-1,100,112,pc-monotonic
```

- `schema_version`: literal `1`; `kind`: `telemetry` or completed `rtt`.
- `session_id`: capture/session identity, not a password or authentication key.
- Telemetry needs stream, uint32 sequence, receiver monotonic milliseconds,
  receiver clock identity and device boot identity. Missing boot identity is
  counted as ambiguous; no sequence/timing continuity is inferred for that row.
- RTT needs a session-unique request ID and non-negative request/reply
  milliseconds from the same declared clock. `tx_clock_id` must equal
  `clock_id`. Missing pairs, cross-clock values and negative RTT are rejected.
  These fields declare a clock basis; the analyzer does not verify clock hardware.
- Leave fields unused by the selected kind blank. Times must be finite and
  non-negative. Values cannot exceed 128 characters.

The analyzer streams at most 100,000 rows from a file of at most 25 MB. It
supports explicit schema v1 only; it does not open serial/socket interfaces or
capture live data. Malformed rows have line-numbered error counts and cause a
nonzero exit. Header-only input has zero samples, not a fabricated pass.

Sequence arithmetic is modulo 2^32 per session/stream/boot. Ordering beyond half
the range is stale/late; exactly half-range is ambiguous. The recent duplicate
window is 1,024 distinct sequences. Older repeats may be classified late/stale.
A missing boot change cannot be distinguished from a reset by arithmetic alone.
No initial or tail gap is assumed. Forward gaps are provisional observations:
for `1,3,2` the gap is one and the late arrival is one; actual final loss is not
claimed. Receiver intervals include accepted duplicate arrivals and are grouped
within the same session/stream/boot/clock. Spans are reported per receiver clock.

The report gives counts, means, minimum/maximum and nearest-rank p95 in ms.
Loss rate and one-way latency remain null. Do not pass its synthetic test
results off as RF quality, synchronized latency or actuator response.
