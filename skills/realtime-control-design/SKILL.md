---
name: realtime-control-design
description: Design task ownership, control deadlines and overload behavior for an embedded controller running alongside sensors, networking or flash writes. Use when users ask for action timing, control-loop jitter, watchdog headroom, multicore isolation or keeping a robot responsive. Do not use for a simple single-loop timer or merely to maximize CPU usage.
metadata: {triggers: "control deadlines, robot timing, task ownership, jitter, control latency, realtime budget"}
---

# Realtime Control Design

Produce a task/resource ownership table and an evidence-backed timing budget.
The fastest clock or highest CPU utilization is not the objective.

## Workflow

1. Read [the shared contract](../../docs/arduino-skill-contract.md). Identify
   the framework/RTOS, core count, tick/timebase, actuator safe state and actual
   response requirement. Mark unknown deadlines; do not invent universal values.
2. Give actuator outputs one owner. Define how sensors, network callbacks,
   services and interrupts pass bounded data or requests to it.
3. For each activity record period/event, deadline, worst observed execution,
   priority/affinity, stack/storage location, blocking operations and failure
   response. Define data age separately from task execution duration.
4. Keep I2C waits, logging, sockets, flash/NVS writes and unbounded allocation
   out of a time-sensitive tick unless their blocking time is measured and
   budgeted. A queue's size and overflow policy must be deliberate. Latest-value
   snapshots suit state; events requiring lossless order need a different path.
5. Read [timing and overload](references/timing-and-overload.md). Keep CPU
   headroom for radio, interrupts, idle/watchdogs and contention. Do not put hot
   control data/stacks in PSRAM simply because it is available.
6. Define stale-sensor, deadline-miss and lost-command behavior before tuning.
   Use the shared [bench lease contract](../wireless-telemetry/references/bench-control-contract.md)
   for remote actuation. OTA must coordinate with the actuator owner.
7. Instrument start intervals, durations, queue drops, sensor timestamps and
   state changes under representative load. A sampled dashboard may miss short
   transitions; choose a bounded event trace when exact action timing matters.

## Ownership and limits

This skill owns the control architecture and budget. `freertos-patterns` owns
task/queue/mutex implementation. `non-blocking-patterns` owns simple scheduling.
`wireless-telemetry` owns transport/measurement interpretation.
`ota-deployment-guardian` owns update and rollback gates. Do not create another
scheduler or promise hard real-time performance from a compile result.

The output must identify design values versus measured values, representative
workload, missing measurements and acceptance criteria. Keep the stages in
the shared contract visible. See [source lessons](../../docs/research/2026-10-15-bottlesumo-lessons.md)
for the build-to-hardware boundary.
