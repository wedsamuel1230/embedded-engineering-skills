---
name: embedded-build-workflow
description: Inspect, reproduce or migrate embedded build workflows with PlatformIO, native ESP-IDF, Arduino CLI, Zephyr/west, Pico SDK, STM32Cube or MicroPython. Use when a request concerns build environments, mixed frameworks, dependency pins, CI, SDK migration or flash/PSRAM configuration. Do not use for ordinary application logic, GPIO lookup or flashing an unknown device.
metadata: {triggers: "PlatformIO, ESP-IDF, mixed firmware builds, SDK migration, sdkconfig, CI, Zephyr, Pico SDK, STM32Cube, MicroPython"}
---

# Embedded Build Workflow

Produce an explicit project/environment matrix and the smallest reproducible
build path. A framework name is not target support or a successful build.

## Workflow

1. Read [the shared contract](../../docs/arduino-skill-contract.md). Preserve
   source locations and existing pinned tooling before proposing migration.
2. Run the offline inspector:
   `uv run scripts/inspect_build.py --project PATH`. It never builds, flashes,
   opens ports, installs packages or executes project scripts. It returns
   argument arrays, not shell commands. Treat custom build scripts as code to
   review before a separately authorized build.
3. Read [toolchain branches](references/toolchain-branches.md) for the detected
   framework. Choose the repository's build manager, not an Arduino default.
   If PlatformIO contains `extra_configs`, `extends` or interpolation, obtain
   its native computed configuration and retain unresolved status meanwhile.
   Do not share raw computed config when it contains credentials.
4. Record board/carrier revision, module suffix, flash and PSRAM separately,
   environment, host OS, tool versions and dependency resolution. For ESP32-S3
   memory work, read [memory evidence](references/memory-evidence.md); use
   `scripts/check_memory_config.py` only with the explicit physical profile and
   provenance of the selected generated sdkconfig.
5. Build every declared program/environment in scope. If an input program has
   no build path, report it; do not infer that every sketch needs a sibling INI
   when a root project already owns its source. Reuse the same matrix in CI.
6. Keep migration staged: baseline build, bounded API/driver adaptation, host
   tests, native build, then authorized target tests. Arduino libraries may rely
   on `Wire`, timing, callbacks and runtime initialization unavailable natively.
7. Report the inspected evidence and unverified stages. Use the
   [support matrix](../../docs/platform-support.md), not a family-wide badge.

## Outputs

- project paths; all declared environments; framework and manager;
- explicit versions, unresolved inheritance and custom-script trust boundary;
- build/test argument arrays and actual results, when execution was authorized;
- four memory outcomes: `confirmed-mismatch`, `consistent-with-inspected-evidence`,
  `unresolved`, `not-applicable`;
- source revision/input hashes, selected environment and artifact identity;
- upload, physical memory population and runtime behavior marked unverified.

## Ownership

The workflow router retains combined board/wiring/application work.
`arduino-cli-skill` owns Arduino CLI commands; native projects stay here.
`board-support` resolves board identity; this skill checks build configuration.
`realtime-control-design`, `freertos-patterns` and `wireless-telemetry` own their
respective designs. Keep pin and electrical claims outside the inspector.

## Sources and verification

The helpers use the Python standard library. Run
`uv run -m unittest discover -s tests -p test_embedded_workflows.py` from the
package root. See [source lessons](../../docs/research/2026-10-15-bottlesumo-lessons.md)
and [research lineage](../../docs/research/2026-10-15-universal-embedded-skills.md).
Tests of the helper prove its output and uncertainty handling, not a firmware
build. Run the trusted compile fixtures separately before claiming build proof.


## Platform procedures

Use the selected specialist for concrete native mechanics:
[Zephyr](../zephyr-development/SKILL.md),
[STM32Cube](../stm32-development/SKILL.md),
[Pico SDK](../pico-sdk-development/SKILL.md),
[MicroPython](../micropython-development/SKILL.md).
Rust is outside the current implementation scope.
