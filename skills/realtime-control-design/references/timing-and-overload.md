# Timing budget and overload worksheet

| Activity | Trigger/period | Deadline | Measured execution | Owner/core | Blocking bound | Overflow/stale response |
|---|---|---|---|---|---|---|
| Control/actuator | requirement | requirement | unverified until traced | one owner | explicitly bounded | project-specific safe state |
| Sensor/bus | sensor budget/event | freshness requirement | trace including timeouts | separate owner | bus/driver timeout | reject stale sample |
| Wireless | arrival/telemetry cadence | freshness requirement | callback plus deferred work | framework-dependent | bounded handoff | documented drop/backpressure |
| NVS/OTA/logging | service request | service requirement | trace flash/log effects | service owner | measured or isolated | stopped-output handshake |

Record trace timebase, counter wrap, sample count, duration and workload. Test
normal operation, radio reconnect/congestion, sensor timeout, queue overflow,
flash update and log backpressure. Compare both start-to-start jitter and tick
duration with their own criteria. Stack high-water marks and heap minima need
the exact port's units and runtime interpretation.

Choose periods/priorities from requirements and measurement, not from this
worksheet. ESP-IDF task affinity, stack size and critical sections differ from
vanilla FreeRTOS and Arduino-Pico multicore. A high-priority task that spins can
starve idle/watchdog services. Mutual exclusion may also delay a deadline;
record ownership, lock order and worst observed hold time.

For a robotics FSM record each state/action's entry time, elapsed time, exit
condition, timeout and emergency preemption. Timed open-loop motion is a
calibrated approximation, not measured distance or heading. Keep safety checks
active throughout a maneuver and model direction-change interlocks separately.

Primary sources:
[ESP-IDF FreeRTOS](https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-reference/system/freertos_idf.html),
[watchdogs](https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-reference/system/wdts.html),
[external RAM](https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-guides/external-ram.html).
This is design guidance. Target traces and physical stop behavior remain
separate acceptance evidence.
