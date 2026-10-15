# 2.0 platform expansion and identity migration acceptance

Date: 2026-10-15. User requested Zephyr, STM32, Pico SDK and MicroPython,
deferring Rust, renaming to embedded-engineering-skills and more debugging.
This record supersedes the earlier 1.9 source positioning decisions.

## Blueprint assessment

Keep the 33 prior bundles and add four independently triggered platform jobs
plus six debugging jobs. Keep standard flat skill discovery, with seven
category folder indexes: the portable standards do not promise deep category
scanning. No duplicated skill body, universal execution engine or speculative
pin database. Canonical skill names stay stable; plugin namespace changes are
an explicit 2.0 compatibility event, with old-host cache state separate.

Primary-source research ran with gpt-6-luna in a bounded separate context.
[Research](2026-10-15-platform-expansion.md) records official docs and source
pins. The actual selected Zephyr fixture uses PlatformIO Zephyr 4.3.0 and
ststm32 19.5.0; the research's newer west 4.4.1 proposal is not a tested claim.

## Scope

Four native workflows: Zephyr/west and generated Kconfig/devicetree; STM32Cube
and startup/linker/clock/HAL; Pico SDK and board/platform/PIO/multicore; and
MicroPython ports, REPL, heap/interrupt/bytecode compatibility.
Six new diagnosis workflows: probe/GDB, captured fault registers, buses,
boot/flash recovery, runtime memory/timing and USB. Retain existing serial,
I2C and circuit ownership. Electrical continuity guidance now preserves
intentional isolation instead of universally bonding every ground.

The offline ARMv7-M decoder refuses unsupported architectures and malformed
32-bit registers. It checks valid fault-address bits, flags imprecise/bad-stack
uncertainty, leaves reserved bits unmapped and never declares a root cause or
device health from a register dump. M3 floating-point-only bits stay unmapped.

## Build findings

STM32Cube's initial platform-only pin resolved F4 1.28.3 and GCC 7.2.1; the
final fixture explicitly pins F4 1.28.3, Arm GCC package 1.120301.0 and linker
scripts 0.2.0, and is rebuilt for that state. Zephyr uses framework 3.40300.0
(Zephyr 4.3.0) and Arm GCC package 1.120301.0. Modules remain those in that
framework's west manifest; platform-only pinning is not a complete lock.

Pico SDK 2.2.0 source a1438dff1d38bd9c65dbd693f0e5db4b9ae91779 built an
RP2040 idle ELF. The fixture initially imported SDK only from its environment;
the runner supplied a CMake cache variable. That mismatch was fixed in the
fixture, then verified via the actual runner in a fresh build directory.

MicroPython v1.26.1 source 647c8b96cae7e202c7a020395b7cfe65e5b8ce04
Unix minimal failed under Apple Clang on a constant-folding warning and missing
Darwin pthread declarations. The final macOS runner explicitly enables pthread
and makes only that warning nonfatal; SDK source is not patched. The interpreter
build and pure-Python smoke pass for that configuration. No threading, MCU
firmware or device I/O is claimed. mpremote 1.26.0 is UV-locked; only its
help command is exercised without a connected device.

## Verification record

Results, final review and remote rename acknowledgement are recorded after the
relevant checks. Installation in live host caches, Windows/Linux execution,
physical probe/flash, buses, RF, actuators and power-cut recovery remain separate.

## Dependency closure correction

The first Zephyr installation began downloading its broad upstream module set;
that attempt was stopped before build completion. Reading the pinned
[PlatformIO STM32 installer](https://github.com/platformio/platform-ststm32/blob/v19.5.0/platform.py)
and packaged Zephyr builder showed support for a project-level `west.yml`.
The final fixture keeps only CMSIS, CMSIS_6 and STM32 HAL at the exact hashes
from framework 3.40300.0's west manifest. Serial/console/GPIO are disabled and
minimal libc is explicit. This closure is for this idle F401 fixture, not a
recommendation to remove modules from an arbitrary application.

## Independent forward probe

A fresh-context agent read the catalogue plus selected skill bodies/references,
without research/eval outputs or intended answers. Eight request handbacks
covered Zephyr devicetree versus Kconfig, generated Makefiles versus CMake,
RP2040 cache versus RP2350 SDK, motor startup with unidentified mpremote target,
M0+ versus the v7-M decoder, native USB versus UART bridge under debugger halt,
CAN loopback versus external bus-off, and a simple Uno millis timer.
The actual handback selected the relevant narrow routes and preserved evidence
limits in each case. It refused unsupported architecture decoding, unsafe
unidentified motor/device operations and physical proof from compilation or
loopback. The simple timer stayed with non-blocking-patterns. This is a bounded
semantic probe, not an aggregate accuracy benchmark or live device test.

## Final scoped code and architecture review

The primary reviewed the connected build plans, SDK revision/status checks,
fault decoder, its caller tests, catalogue inventory, manifests and CI matrix.
Expected load is one trusted local fixture build or a bounded offline dump.
Review repairs included the SDK environment/cache-path mismatch, unsupported
M3 FP status bits, build output/source separation and direct symlink handling.
No project parser executes a build; the fixture runner is a separate explicit
trusted-build command. No target/device command appears in its plans.

Zephyr's host build dependencies are now exact pins in UV's firmware group,
including its required YAML/ELF/schema packages. Transitive host dependencies
are locked in uv.lock, preventing the framework from needing a floating pip
bootstrap in this tested environment. Native SDK/compiler tools remain selected
external dependencies; UV does not pin the firmware SDK or system compiler.

The current native host records UV 0.11.8, CPython 3.12.13, CMake 4.4.4,
Ninja 1.13.2 and Apple Clang 21.0.0. The Pico cross compiler identifies itself
as Arm GCC 14.3.0; this is recorded directly rather than inferred from its
package name. STM32/Zephyr select Arm GCC 12.3.1. STM32's minimal default link
emits newlib I/O-stub and RWX-segment warnings; it has no I/O/use/deployment proof.
Pico's absent optional TinyUSB submodule is not used by the stdio-disabled ELF.

The GitHub rename was acknowledged, old web redirect/API identity verified,
and local source/origin moved to embedded-engineering-skills. Old fixture build
caches were preserved outside source; UV console scripts were reinstalled after
the directory move. The new path then ran package/contract/unit checks and
fresh fixture builds. No source commit/push or installed host cache update was
performed. No powered target test is claimed.

## Final acceptance results

After source-directory migration and UV dependency locking, all six fixture
builds passed: Arduino-ESP32 3.3.8/N16R8, native ESP-IDF 6.0.1/N16R8,
STM32Cube F4 1.28.3/F401RE, Zephyr 4.3.0/F401RE (minimal pinned module closure),
Pico SDK 2.2.0/RP2040 ELF and MicroPython v1.26.1 Unix minimal-with-pthread plus
smoke. The new Zephyr fixture uses modern `find_package(Zephyr)` CMake setup.
No source input changed after these final builds.

At the migrated path, validation covers 43 skill bundles with zero errors,
8/8 shared-contract themes, 20/20 retained deterministic cases and 42 passing
host unit tests. The actual fault CLI accepts its supported synthetic capture
and returns unresolved/exit 2 for M0+ input. C++17 lease tests pass. Real YAML
frontmatter/CI matrix parsing and the portable Agent Plugins JSON Schema pass.
The current native CI definition has four host/platform combinations, not
four remotely executed results. `git diff --check` passes.

The source review archive preserves shared dependencies, catalogue, tests,
fixtures and adapters. It is a repository review/local-source bundle, not a
public Plugin Creator submission: marketplace authoring files are included for
local review. Build caches, Git history, vendor SDKs and historical machine-local
workflow/eval outputs are excluded. Extraction/checksum and package tests are
checked separately. Installed host discovery, Windows/Linux execution and all
physical behavior remain unverified. Stop reason: requested source/platform/
debugging expansion and acknowledged identity rename have their scoped evidence;
publication and live host upgrade were not performed.


## Authorized review-branch delivery

The user subsequently authorized commit/push and invoked
`improve-codebase-architecture`. The review branch is
`codex/universal-embedded-skills`; main was refreshed and still resolves to the
same baseline before delivery. Current package/contract checks and all 42 host
tests pass. Five prior compile proofs remain applicable. Delivery review removed a
generated ESP-IDF per-environment sdkconfig from the staged set and added an
ignore rule; the authored defaults remain tracked. An isolated native ESP-IDF
build from those defaults then passed (exit 0), without the source checkout
generated configuration. Other delivery edits normalize text EOF whitespace
and clarify review-branch installation; they change no firmware behavior.
The scoped code review and independent architecture walk found no confirmed
publishing blocker. Potential deepening work is presented separately in an OS
temporary HTML report, with no speculative refactor or new glossary/ADR added
before the user selects a candidate. Installed host caches remain unchanged.
