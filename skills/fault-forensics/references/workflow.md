# Fault capture and architecture

Input is JSON with `architecture` equal to cortex-m3, cortex-m4 or cortex-m7,
`cfsr` and `hfsr` unsigned 32-bit values (integers or 0x strings). Optional
`bfar`, `mmfar`, `pc`, `lr`, `sp`, `xpsr` are the captured registers. The helper
ignores unknown fields and never infers the missing stack-frame format.

CFSR bits include MemManage, BusFault and UsageFault status. Report BFAR/MMFAR
only when the corresponding valid bit is set and the register was supplied.
For IMPRECISERR the stacked PC may follow the instruction that caused the bus
fault. STKERR/UNSTKERR also weaken confidence in an ordinary stack unwind.
Unknown/reserved bits stay visible. Do not use a v7-M decoder for M0/M0+,
TrustZone/security faults or an arbitrary RISC-V exception.

For ESP-IDF preserve the full panic/core dump and exact target ELF and SDK.
Use that SDK's panic/core-dump tooling; a build or successful symbolization is
not a reproduced target crash. For MicroPython keep the Python traceback and
port build before routing a native crash here.

Primary sources: [Arm Cortex-M4 Generic User Guide](https://developer.arm.com/documentation/dui0553/latest/),
[CMSIS core registers](https://arm-software.github.io/CMSIS_6/latest/Core/group__Core__Register__gr.html),
[ESP-IDF fatal errors](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/fatal-errors.html).
