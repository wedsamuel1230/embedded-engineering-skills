# Runtime evidence

FreeRTOS stack sizes/high-water units differ by API/port, including ESP-IDF.
Zephyr thread analyzer, runtime statistics and stack guards have configuration
and instrumentation costs. Enable them for the exact version/build and record
how they affect timing. A watchdog reports a failure symptom, not automatically
the task that caused it.

For a suspected overwrite use canaries, bounded buffers, allocator integrity
checks or a target watchpoint appropriate to that MCU. Host sanitizers can test
portable parsing/control code, but do not validate target memory maps/ISRs.
For MicroPython distinguish garbage-collection pause/allocation behavior from
a native C heap leak; exceptions in an IRQ need port-specific handling.

Minimum trace fields: build identity, boot/session, clock/unit, event/task,
start/end or duration, expected release/deadline, queue/drop and relevant
resource owner. Avoid printf on a hot control tick. Preserve event loss counts;
a sampled UI cannot prove every short transition.

Primary sources: [ESP-IDF heap debugging](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/heap_debug.html),
[Zephyr thread analyzer](https://docs.zephyrproject.org/latest/services/debugging/thread-analyzer.html),
[FreeRTOS runtime statistics](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/08-Run-time-statistics),
[MicroPython constrained devices](https://docs.micropython.org/en/latest/reference/constrained.html).
