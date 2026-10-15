# Probe session boundaries

Offline GDB commands such as `file FIRMWARE.elf`, `info files`, `info functions`
and `disassemble FUNCTION` do not establish a target connection. A server
configuration can itself assert reset or halt; inspect its init sequence.

For a planned session, document the exact command argv and transport ports,
loopback bind policy, chosen adapter serial, target config and initial halt/
reset behavior. Verify a server's own version/help for options; OpenOCD,
pyOCD, J-Link and ST-LINK server switches are not interchangeable.

In GDB distinguish `attach`/`target remote` from `load`. Preserve the initial
PC, SP and fault registers before reset; continuing may destroy evidence.
A peripheral/DMA can keep running while the CPU is halted. Watchdog freeze bits
and multicore halt behavior are device-specific and change the observed fault.

Primary sources: [GDB remote debugging](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Remote-Debugging.html),
[OpenOCD debugging](https://openocd.org/doc/html/GDB-and-OpenOCD.html),
[OpenOCD reset](https://openocd.org/doc/html/Reset-Configuration.html),
[pyOCD](https://pyocd.io/docs/).
