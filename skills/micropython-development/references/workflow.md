# MicroPython ports, REPL and recovery

The fixture builds the pinned v1.26.1 Unix **minimal** variant (macOS with pthread enabled) and executes a
pure-Python smoke script. Minimal lacks optional modules/features; it validates
that port only. ESP32, STM32 and RP2 firmware need their own port/BOARD,
submodules/SDK/compiler and device tests.

```sh
make -C ports/unix VARIANT=minimal
# macOS v1.26.1: add MICROPY_PY_THREAD=1 CFLAGS_EXTRA=-Wno-error=gnu-folding-constant
ports/unix/build-minimal/micropython smoke.py
```

Check the selected revision's README before adding submodules or firmware
features. Keep mpy-cross and frozen bytecode compatible with the target build.
Run `uv run --group micropython mpremote --help` from this package, or pin the
same package in the consuming project's UV configuration. Inspect the port
before `connect DEVICE`; even REPL operations can alter runtime state.

A crash in `main.py` differs from corrupt firmware: attempt the documented
interrupt/safe-mode procedure for that board before considering erase. Never
advertise one universal safe-mode button sequence. Secure local backups may
contain Wi-Fi credentials; do not copy them into a report or Git.

Primary sources: [MicroPython Unix port](https://github.com/micropython/micropython/tree/v1.26.1/ports/unix),
[mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html),
[interrupt handlers](https://docs.micropython.org/en/latest/reference/isr_rules.html),
[time/ticks](https://docs.micropython.org/en/latest/library/time.html).

On the tested Apple Clang host, unmodified minimal first fails on a constant-
folding warning promoted by upstream `-Werror`, then on Darwin realtime helpers
whose pthread declarations are hidden when threads are off. The fixture runner
uses the two explicit macOS flags above in a fresh build directory. It preserves
other warnings/errors and does not patch SDK source. This validates that exact
minimal-with-pthread configuration and smoke script, not MicroPython threading
or every port. Linux retains ordinary minimal. See the release's
[Darwin realtime code](https://github.com/micropython/micropython/blob/v1.26.1/ports/unix/mpthreadport.c)
and [minimal configuration](https://github.com/micropython/micropython/blob/v1.26.1/ports/unix/variants/minimal/mpconfigvariant.mk).
