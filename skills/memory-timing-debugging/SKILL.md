---
name: memory-timing-debugging
description: Diagnose runtime heap/stack failures, deadline misses, deadlocks and queue overload in embedded firmware. Use when requests involve leaks, jitter, watchdog starvation, priority inversion or task stalls; not initial scheduling architecture alone.
metadata: {triggers: "Memory and Timing Debugging, embedded diagnosis"}
---

# Memory and Timing Debugging

Read [the shared embedded contract](../../docs/arduino-skill-contract.md) and
keep source/build, device and physical evidence separate.

Read [runtime evidence](references/workflow.md). Preserve the failing build,
workload, allocation/timing trace, reset cause and reproduction. Identify whether
the fault is exhaustion, fragmentation, overwrite, blocking, starvation or
measurement distortion before changing task priorities or heap size.

Capture minimum free heap, largest free block where supported, stack high-water
marks with the port's units, queue depth/drops and timestamped task/state events.
A free-heap total alone does not establish an allocation fits. Inspect allocator
and capability pools; PSRAM and internal DMA-capable memory are not substitutes.

For jitter separate release interval, execution duration, blocking duration,
data age and interrupt latency. Compare tracing enabled/disabled overhead;
debugger stepping and synchronous logging can destroy the original timing.
Record clock basis, wrap and missed samples. Check lock ownership/order and
priority inheritance; never add a spin loop to hide a deadlock.

Use `realtime-control-design` for a revised ownership/deadline budget,
`freertos-patterns` for the selected FreeRTOS primitives, and the matching
platform skill for Zephyr/SDK/MicroPython semantics. Deliver a falsifiable
hypothesis and a bounded before/after measurement, not a CPU-utilization slogan.

See [platform coverage](../../docs/platform-support.md) for the exact tested
combination. A source procedure is not a claim that every target was tested.
