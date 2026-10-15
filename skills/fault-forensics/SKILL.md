---
name: fault-forensics
description: Analyze embedded panic logs, Cortex-M fault registers, core dumps and addresses against the matching firmware ELF. Use when requests involve HardFault, BusFault, UsageFault, reset crashes or corrupted backtraces; no unsupported CPU decoding.
metadata: {triggers: "Fault Forensics, embedded diagnosis"}
---

# Fault Forensics

Read [the shared embedded contract](../../docs/arduino-skill-contract.md) and
keep source/build, device and physical evidence separate.

Read [capture and architecture](references/workflow.md). Preserve the original
log/register dump, reset reason, exact ELF/map, revision, build options and
architecture before rebooting or rebuilding. Never symbolize against a newer
binary merely because its filename matches.

For ARMv7-M Cortex-M3/M4/M7, run the offline
`uv run scripts/decode_cortex_fault.py CAPTURE.json` on the documented schema. It
reports set bits, valid fault addresses and unresolved cause. It does not read
hardware or establish that a stacked PC identifies the initiating instruction.
Cortex-M0/M0+ and ARMv8-M have different fault facilities; ESP32 Xtensa/RISC-V
panic formats use the matching vendor decoder instead.

Correlate CFSR/HFSR, stack-frame integrity, EXC_RETURN and the matching ELF.
Check precise versus imprecise bus errors, failed stack/unstack, and valid
MMFAR/BFAR bits before treating an address as evidence. A HardFault escalation
is not a root cause. Use the selected toolchain `addr2line` offline and retain
its version and unknown-address output.

Deliver observed facts, competing explanations and one discriminating next
check. Preserve evidence before changes to watchdogs, assert handling or fault
recovery. Do not hide a crash by disabling detection.

See [platform coverage](../../docs/platform-support.md) for the exact tested
combination. A source procedure is not a claim that every target was tested.
