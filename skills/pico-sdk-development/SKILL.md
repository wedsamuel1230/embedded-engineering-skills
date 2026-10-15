---
name: pico-sdk-development
description: Build and debug native Raspberry Pi Pico SDK applications with CMake, RP2040/RP2350 targets, PIO and SWD. Use when requests concern Pico SDK configuration, linker output, multicore/PIO or native SDK migration; distinguish Arduino-Pico.
metadata: {triggers: "Pico SDK Development, embedded diagnosis"}
---

# Pico SDK Development

Read [the shared embedded contract](../../docs/arduino-skill-contract.md) and
keep source/build, device and physical evidence separate.

Read [native SDK workflow](references/workflow.md). Confirm RP2040 versus
RP2350, exact board, flash population, SDK revision, compiler and CMake cache.
Arduino-Pico is a different framework; its core version is not the Pico SDK
version. Preserve a requested CPU architecture and board profile.

Use an out-of-source build with the repository's `PICO_BOARD`, `PICO_PLATFORM`,
SDK path and toolchain. Avoid changing a populated build directory to another
chip or SDK; create a fresh build directory. Build the ELF before producing or
copying a UF2. Keep map/ELF and SDK revision together.

For PIO inspect instruction count, wrap points, clock divider, FIFO direction,
DREQ, pin mapping and DMA ownership; a legal instruction program can still wait
forever on the wrong pin/IRQ. For multicore code identify shared-data ownership,
locks and flash/XIP assumptions. SDK multicore is not automatically FreeRTOS.
Route runtime scheduling to `memory-timing-debugging` and SWD to
`probe-debugging`. USB CDC and UART stdio are distinct transports.

BOOTSEL/UF2 copying, `picotool load`, probe `program` and `flash` write hardware.
Build-only work ends at artifacts. Deliver the exact CMake configuration,
resolved SDK/compiler, compile result and target checks still required.

See [platform coverage](../../docs/platform-support.md) for the exact tested
combination. A source procedure is not a claim that every target was tested.
