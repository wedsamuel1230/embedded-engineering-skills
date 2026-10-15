---
name: wireless-telemetry
description: Design and diagnose embedded telemetry, packet freshness and wireless coexistence using UDP, ESP-NOW or a serial bridge. Use when users need AP+STA operation, low-latency data, sequence/boot identifiers, packet-loss analysis or bench-control leases. Do not use for generic web networking, ordinary serial logs or to promise RF latency without measurements.
metadata: {triggers: "UDP telemetry, ESP-NOW, AP+STA, wireless latency, packet freshness, radio coexistence, bench lease"}
---

# Wireless Telemetry

Produce a transport/freshness contract and a reproducible measurement plan.
Separate telemetry observation, command authority and radio delivery.

## Workflow

1. Read [the shared contract](../../docs/arduino-skill-contract.md). Identify
   exact MCU/framework, endpoints, topology, payload size, cadence, channel,
   power-save policy and security/provisioning requirements.
2. Select the transport from constraints, not a latency slogan. UDP is useful
   for freshest state; reliable streams have different backlog semantics.
   ESP-NOW needs target-version payload/channel/peer/security checks. Read
   [coexistence and measurement](references/coexistence-and-measurement.md).
3. Keep callback work bounded; defer heavy processing. Specify queue depth,
   overflow/drop behavior and data age. Networking must not own actuator outputs.
4. Define protocol version, stream identity, boot/session identity, sequence
   width/wrap, clock basis and authentication/replay behavior. A checksum is not
   authentication. A send callback does not establish application receipt.
5. Use the single [bench-control contract](references/bench-control-contract.md)
   when driving is in scope. Autonomous operation rejects steering; expired,
   stale or replayed commands never renew authority. STOP and fresh re-arm are
   separate from reconnecting a dashboard.
6. Record endpoints, units, duration, workload, samples and completeness. Use
   `uv run scripts/analyze_trace.py TRACE.csv` for the explicit
   [trace schema](references/trace-schema.md). It reports observed forward gaps,
   duplicates, late/stale sequence events, receive intervals and same-clock RTT.
   It never calculates loss rate or unsynchronized one-way latency.
7. Test missing/corrupt/replayed packets, reconnects, boot resets, queue pressure
   and channel changes. Host traces prove analysis/protocol logic only; label RF,
   device deadline and actuator-stop behavior unverified until measured.

## Integration and verification

`arduino-serial-monitor` owns serial capture and desktop-console integration;
this skill owns wireless interpretation. `realtime-control-design` owns the
control budget; `ota-deployment-guardian` owns updating. Do not duplicate live
dashboards, transport drivers or schedulers here.

Run the package's `test_embedded_workflows.py` suite and the host
`tests/lease_guard_test.cpp`. See [source lessons](../../docs/research/2026-10-15-bottlesumo-lessons.md).
Deliver the measured/assumed distinction, actual valid/rejected samples, scope
of supported clocks/protocols and recovery/security notes from the shared
contract. CPU affinity, AP setup and a successful compile are not low-loss or
low-latency proof.
