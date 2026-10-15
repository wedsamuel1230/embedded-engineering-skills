# Recovery decision path

1. Separate a host transport failure from a running but unhealthy application.
   Retain reset cause and early boot logs; do not repeatedly reboot away evidence.
2. Match the image to the silicon/board, bootloader and memory layout. For
   Cortex-M inspect initial SP/reset vector and linker region without inventing
   universal addresses. ESP-IDF partitions and Pico UF2 are different formats.
3. Retain a known-good image plus a recovery path independent of the failing app.
   Identify persistent regions that survive and which image can read them.
4. If the documented procedure erases or removes protection, name the exact
   effect and require the applicable authorization before executing it.
5. Verify readback/hash where supported, boot outcome and application health
   independently. A tool reporting successful write does not establish all three.

Primary sources: [STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html),
[ESP-IDF partition tables](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/partition-tables.html),
[Pico boot/debug](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html),
[MicroPython firmware deployment](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html).
