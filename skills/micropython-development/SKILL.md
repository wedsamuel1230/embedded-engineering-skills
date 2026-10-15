---
name: micropython-development
description: Develop and debug MicroPython firmware and Python applications using mpremote, REPL, board-specific ports and frozen modules. Use when requests involve MicroPython boot failures, heap limits, native firmware builds or device file transfer; not CPython.
metadata: {triggers: "MicroPython Development, embedded diagnosis"}
---

# MicroPython Development

Read [the shared embedded contract](../../docs/arduino-skill-contract.md) and
keep source/build, device and physical evidence separate.

Read [ports, REPL and recovery](references/workflow.md). Record the exact
port/board, MicroPython revision and `sys.implementation`, `sys.platform`,
`os.uname()` when available. Host CPython syntax checking is not MicroPython
execution, and a Unix-port test does not establish MCU driver behavior.

Use a locked `uv` environment for `mpremote`; select an explicit serial device
or hardware serial identity. Check `mpremote --help` and avoid auto-connecting
an arbitrary first port. Commands may enter raw REPL, interrupt execution and
perform a soft reset; this matters when outputs are attached.

Reproduce the smallest script and full traceback without secrets. Distinguish
missing/frozen modules, unsupported CPython APIs, `.mpy` compatibility, heap
fragmentation and interrupt-context allocation. Use `gc.mem_free()` and
`gc.mem_alloc()` as observations, not a guarantee a contiguous allocation fits.
Use wrap-safe `time.ticks_diff()`; `ticks_ms()` is not an unbounded integer clock.
Interrupt code must follow port-specific allocation/exception constraints.

Device file writes, firmware erase/flash, `boot.py`/`main.py` replacement and
reset require the selected target and authorized device state. Back up user
files and preserve a recovery path before changing startup scripts. Unix-port
build/smoke validation and board commissioning are distinct outputs.

See [platform coverage](../../docs/platform-support.md) for the exact tested
combination. A source procedure is not a claim that every target was tested.
