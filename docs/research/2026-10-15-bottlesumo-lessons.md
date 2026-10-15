# BottleSumo lessons for the source plugin

Source: [BottleSumo commit ee776ca](https://github.com/wedsamuel1230/BottleSumo-2026/commit/ee776ca6cf46892fd439dfc54f8c50377048ed8c).
Evidence labels below are paths at that immutable revision. TypeSafe/Jev adopted
five of six redacted candidates (surface probabilities 0.65–0.80, durability
2.96–2.99); control-task ownership was rejected as a duplicate (coverage 0.52).
Production writers verified the five lesson keys. No installed skill cache or
global governance file was modified. Capture is not automatic future retrieval;
active router/build/wireless links and probes are checked separately.

## Appended lessons

<!-- lesson-key: d6321c591c6e -->
### Build every declared firmware environment

For mixed Arduino and native SDK repositories, keep each source in its original project, enumerate all programs and environments, and fail validation when a discovered sketch has no build configuration. Pin the PlatformIO platform separately from the actual framework/core; a platform name alone does not guarantee the requested Arduino or SDK version. Run the same matrix locally and in CI.

Evidence: BottleSumo-2026@ee776ca/scripts/validate-firmware.sh:24

<!-- lesson-key: d4198ba7e755 -->
### Verify memory population and bus modes separately

An ESP32-S3 target name must include its module suffix and flash/PSRAM population. Cross-check board metadata, sdkconfig and partition capacity; do not reuse a historical board setting after a module change. N16R8 quad flash and octal PSRAM require separate bus-mode choices; more flash or PSRAM does not justify placing control stacks and hot data in external RAM.

Evidence: BottleSumo-2026@ee776ca/docs/ci/platformio-firmware.md:20

<!-- lesson-key: 73db49999a31 -->
### Separate packet freshness from delivery and latency

UDP/ESP-NOW telemetry should carry boot identity and sequence numbers, bound callback work, and drop stale snapshots rather than build a backlog. MAC-send success is not application receipt; receiver age is not one-way latency without clock synchronization. AP+STA and ESP-NOW share channel constraints, so record channel changes and receiver behavior before promising low loss or low latency.

Evidence: BottleSumo-2026@ee776ca/docs/competition/esp-idf-wireless.md:96

<!-- lesson-key: bb4dff6ffdd0 -->
### Treat OTA rollback and actuator stop as separate gates

Dual application slots do not by themselves prove safe rollback. Require actuator-owner acknowledgement of stopped outputs before flash writes, an expiring physical-arm window for an actuator device, bounded boot-health validation, and explicit rollback/power-loss tests. Keep calibration in a separate persistent partition with a schema migration plan; credentials must be provisioned locally and omitted from firmware images.

Evidence: BottleSumo-2026@ee776ca/firmware/bottlesumo_idf/main/wireless.cpp:121

<!-- lesson-key: 5addf98344a5 -->
### Exercise the whole remote-drive lease chain

A bench dashboard needs a physical bench mode plus browser, bridge and robot drive leases. Verify STOP, stale commands, replay, disconnect, held-key repeats and mode changes. A simulator or host test proves the command logic only; powered movement and Windows launcher behavior need separate target/host evidence. Sampled telemetry can miss short transitions, so use a bounded event trace when every action timing matters.

Evidence: BottleSumo-2026@ee776ca/tests/test_bottlesumo_debug.py:1
