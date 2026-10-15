---
name: stm32-development
description: Build and diagnose STM32Cube HAL/LL projects using their existing CMake, Make, CubeIDE or PlatformIO toolchain. Use when requests involve STM32 clocks, startup/linker files, generated code, SWD or HAL peripheral setup.
metadata: {triggers: "STM32 Development, embedded diagnosis"}
---

# STM32 Development

Read [the shared embedded contract](../../docs/arduino-skill-contract.md) and
keep source/build, device and physical evidence separate.

Read [build and target diagnosis](references/workflow.md). Identify exact
STM32 part and board revision, Cube/HAL package, generator, startup file, linker
script, flash/RAM banks and oscillator population. Do not infer an HSE frequency
or pin mux from a Nucleo family name.

Use the existing CMake preset, generated Makefile, CubeIDE headless build or
PlatformIO environment. `STM32CubeCLT` availability does not imply a CMake
project. Preserve `.ioc`, source-controlled generator output and USER CODE
sections; inspect a regeneration diff before replacing manual code.

Retain the ELF/map and compiler options. Verify vector-table location, Reset
handler, stack, heap and memory-region overlap before changing an address to
silence a linker failure. Diagnose clock faults through oscillator readiness,
PLL constraints, bus prescalers, flash latency and error paths for that exact
MCU/reference manual. Distinguish HAL timeout symptoms from their cause.

Use `probe-debugging` for SWD/probe sessions, `fault-forensics` for Cortex-M
fault registers and `bus-debugging` for transfers. Do not turn on a conflicting
peripheral to test a pin on an attached actuator. Deliver the smallest change,
matching build artifacts and measured-versus-unverified behavior.

See [platform coverage](../../docs/platform-support.md) for the exact tested
combination. A source procedure is not a claim that every target was tested.
