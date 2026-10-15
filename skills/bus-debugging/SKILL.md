---
name: bus-debugging
description: Diagnose SPI, UART, CAN and I2C protocol failures using transaction evidence and electrical constraints. Use when requests involve corrupt bytes, wrong SPI mode, framing, bus-off, chip-select timing or DMA transfers; use I2C bring-up for basic discovery.
metadata: {triggers: "Bus Debugging, embedded diagnosis"}
---

# Bus Debugging

Read [the shared embedded contract](../../docs/arduino-skill-contract.md) and
keep source/build, device and physical evidence separate.

Read [protocol branches](references/workflow.md). Identify exact controller,
peripheral, voltage domain, pins/mux, clock, transfer mode, payload and capture
point. Separate electrical, framing, driver and application interpretation.
Do not assume a decoded analyzer trace proves voltage margin or signal quality.

Choose a minimal transaction with a datasheet-defined response. Compare the
actual wire capture with the requested byte order, edges, framing and timeout.
For I2C discovery/pull-ups route to `i2c-bringup-diagnostician`; use this skill
for transaction framing and cross-layer diagnosis. Scans/transfers can write
or trigger devices, so keep attached actuators in the required safe state.

For DMA inspect buffer lifetime, alignment/cache coherency where applicable,
completion/error path and concurrent ownership before adding arbitrary delays.
Compare a bounded polling transfer to DMA only when the test is appropriate
and authorized. Keep the failing configuration and change one causal variable.

Deliver annotated expected/observed transaction, evidence location and next
check. Distinguish MCU peripheral errors, analyzer decoding assumptions and
what remains electrically unmeasured.

See [platform coverage](../../docs/platform-support.md) for the exact tested
combination. A source procedure is not a claim that every target was tested.
