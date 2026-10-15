# Embedded Engineering Skills platform coverage

Package/repository identity: `embedded-engineering-skills` (2.0 candidate).
Four additional platform procedures have dedicated build fixtures; exact
coverage does not imply all boards or host combinations work. Rust is deferred.

| Framework/target | Procedure and fixture | Evidence scope |
|---|---|---|
| Arduino-ESP32 3.3.8 / ESP32-S3 DevKitC-1 N16R8 | existing pinned pioarduino fixture | macOS compile from 1.9 work; unchanged firmware input |
| ESP-IDF 6.0.1 / DevKitC-1 N16R8 | existing PlatformIO 7.0.1 fixture | macOS compile from 1.9 work; unchanged firmware input |
| STM32Cube F4 1.28.3 / Nucleo F401RE | stm32-development; platform fixture | macOS cross-compile, exact resolved packages in acceptance record |
| Zephyr 4.3.0 / Nucleo F401RE | zephyr-development; PlatformIO fixture | result and resolved modules recorded in acceptance record; west procedures separately sourced |
| Pico SDK 2.2.0 / RP2040 pico | pico-sdk-development; native CMake fixture | macOS ELF build, USB/UART stdio disabled |
| MicroPython v1.26.1 / Unix minimal with Darwin pthread option | micropython-development; native Make fixture | macOS interpreter build + smoke; not MCU pin/driver proof |
| MicroPython / ESP32, STM32, RP2 | port/board-specific instructions + mpremote 1.26.0 host tool | no MCU firmware/device session claimed by Unix smoke |
| Other Arduino AVR/Renesas/RP2040 | retained board/skill references | reproduce requested exact FQBN/core/library build |

## Evidence and promotion

Reference guidance includes official source/version and an exact target when
known. Build/host validation names the fixture, source/tool versions, inputs,
command and exit. Hardware validation needs dated measurements for that exact
board and behavior. A debugger connection, successful build, USB enumeration
or Unix interpreter run does not establish actuator, bus, timing or OTA safety.

See [fixture commands](../tests/fixtures/platforms/README.md),
[research](research/2026-10-15-platform-expansion.md), and
[2.0 acceptance record](research/2026-10-15-platform-expansion-implementation.md).
Windows/Linux CI definitions are intended tests until executed. No powered
hardware, RF latency/loss, actual flash recovery or Windows build claim is made.

## Catalogue and routing

[Category folders](../catalog/README.md) group platforms, debugging/recovery,
build/workflow, runtime/connectivity, hardware/power, sensors/memory and docs.
Entrypoints remain flat `skills/<name>/SKILL.md` for portable host discovery.
A platform route never supplies a missing pin map or probe identity.
