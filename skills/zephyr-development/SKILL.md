---
name: zephyr-development
description: Build and debug Zephyr applications with west, devicetree, Kconfig and versioned workspaces. Use when a request concerns Zephyr board qualifiers, overlays, build failures, runners or RTOS diagnostics.
metadata: {triggers: "Zephyr Development, embedded diagnosis"}
---

# Zephyr Development

Read [the shared embedded contract](../../docs/arduino-skill-contract.md) and
keep source/build, device and physical evidence separate.

Record the exact Zephyr revision, frozen west manifest, SDK/toolchain, host,
board qualifier, application, overlays and build directory. A PlatformIO Zephyr
package and a west workspace can contain different Zephyr releases.

Read [workspace and diagnosis](references/workflow.md). Reproduce with the
existing build manager first. In a west workspace use `west manifest --freeze`
and inspect `west list`; neither a board family nor an old board alias is a
verified target. `west build -b BOARD APP -d BUILD --pristine=auto` configures and
compiles; a pristine build removes generated build state, so use a disposable
build directory. Retain `zephyr.dts`, `.config`, ELF/map and the first failing
compiler/linker command. Inspect final generated settings, not only overlays.

For devicetree failures inspect enabled node status, compatible/binding, pinctrl,
chosen nodes and aliases. For missing Kconfig dependencies inspect warnings
and generated `.config`; never force-select a symbol to silence a warning.
For runtime faults use the matching ELF and `fault-forensics`; for deadlock,
stack or scheduling evidence use `memory-timing-debugging`. Distinguish Zephyr
kernel APIs from FreeRTOS primitives.

`west flash`, `west debug`, `west attach`, runner erase and reset can alter or
halt hardware. Inspect the selected runner, probe serial, target voltage and
reset behavior before an authorized session. Do not infer physical operation
from the non-actuating F401 compile fixture. Deliver reproducible command,
effective configuration, root-cause evidence and the next falsifying check.

See [platform coverage](../../docs/platform-support.md) for the exact tested
combination. A source procedure is not a claim that every target was tested.
