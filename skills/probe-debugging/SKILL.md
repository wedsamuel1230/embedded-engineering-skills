---
name: probe-debugging
description: Plan and conduct target-specific GDB, SWD/JTAG and OpenOCD or vendor-probe debugging. Use when requests involve attaching a probe, breakpoints, reset/halt, inaccessible targets or live register inspection; not flashing by default.
metadata: {triggers: "Probe Debugging, embedded diagnosis"}
---

# Probe Debugging

Read [the shared embedded contract](../../docs/arduino-skill-contract.md) and
keep source/build, device and physical evidence separate.

Read [probe session boundaries](references/workflow.md). Confirm MCU/core,
board/probe revision, target reference voltage, SWD/JTAG wiring, probe serial,
server/runner version and the exact ELF/build. Begin with offline ELF inspection.

Inspect the existing launch config or runner instead of guessing an OpenOCD
board file. Binding a debug server to loopback and selecting a probe explicitly
avoids attaching to the wrong board. `target remote`/attach, reset, breakpoint
and register writes can halt or change the target; stop/disable actuators with
the target owner before that session. A debugger connection is not read-only.

Use named hypothesis checks: PC/backtrace and threads; disassembly at the fault;
registers and stack bounds; watchpoint for a suspected overwrite. Optimized
code can inline or eliminate variables; retain the failing binary before
trying a separate debug build. Do not assume stepping reproduces race timing.

`load`, `monitor program`, erase and unprotect operations are separate writes;
never include them in an attach-only recipe. For locked targets distinguish
readout protection, electrical/reset faults and wrong-server configuration.
Unprotect may mass-erase; stop rather than silently recommending it. Return
the selected probe/ELF/server, commands actually run and their effect.

See [platform coverage](../../docs/platform-support.md) for the exact tested
combination. A source procedure is not a claim that every target was tested.
