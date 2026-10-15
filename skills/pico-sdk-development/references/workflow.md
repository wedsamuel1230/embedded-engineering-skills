# Native Pico SDK workflow

The package fixture uses Pico SDK 2.2.0 and `PICO_BOARD=pico` (RP2040),
`PICO_PLATFORM=rp2040`, with USB/UART stdio disabled. It builds an idle ELF;
no flash/upload, PIO signal or multicore result is inferred.

```sh
cmake -S APP -B BUILD -G Ninja -DPICO_BOARD=pico -DPICO_PLATFORM=rp2040
cmake --build BUILD
```

Supply the selected SDK through `PICO_SDK_PATH` or the existing project import.
The fixture runner requires a local SDK checkout at its pinned revision and
`PICO_TOOLCHAIN_PATH` containing Arm GCC. It disables picotool output generation
to avoid an implicit utility download during the compile-only check.

Use the matching `arm-none-eabi-size`, `objdump`, `nm` and `addr2line` on the
ELF. Preserve the linker map and resolve source addresses from the same binary.
A UF2 copy may trigger boot/reset; a debugger halt can disrupt USB and the
other core's assumptions. Treat stdio lock/reentrancy, interrupt callbacks and
XIP/flash operations as separate diagnosis branches.

Primary sources: [Pico SDK](https://github.com/raspberrypi/pico-sdk),
[Raspberry Pi C/C++ SDK](https://www.raspberrypi.com/documentation/pico-sdk/),
[Pico debugging](https://www.raspberrypi.com/documentation/microcontrollers/debug-probe.html).
