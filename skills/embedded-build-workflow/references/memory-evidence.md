# ESP32-S3 memory configuration evidence

N16R8 is a memory/module designation, not a complete carrier-board identity.
Confirm the board revision, module marking and physical memory separately.
For the N16R8 example, quad flash and octal PSRAM are independent choices.
Do not import N16R8V or historical N32R16 settings by similarity.

The offline `scripts/check_memory_config.py` compares selected generated
ESP-IDF 6.0.1 settings with an explicitly supplied profile. Other versions stay
unresolved until the config-symbol mapping is verified. It checks enabled
flash-size/mode and PSRAM enable/mode settings, not actual fitted PSRAM capacity
or board wiring. A missing key in `sdkconfig.defaults` is not proof it is off.

Use three inputs:

1. A physical-profile JSON with `chip`, `board_identity`, `module`, `flash_mb`,
   `flash_mode`, `psram_mb` and `psram_mode`. Values are user declarations until
   independently measured.
2. The generated sdkconfig from the selected environment, not an old defaults
   file. Capture its SHA-256.
3. A provenance JSON with `environment`, `framework`, `framework_version`,
   `sdkconfig_sha256`, `tool_versions`, and `input_hashes` mapping project-relative
   inputs to SHA-256. Include `platformio.ini` and every relevant defaults,
   include and board-profile input. The checker validates listed inputs; it
   cannot certify that the supplied dependency list is complete.

Invoke with `--project PATH --sdkconfig FILE --expected PROFILE
--environment ENV --provenance RECORD`. The helper never creates provenance,
repairs config, executes scripts, probes memory or accesses hardware.

- `confirmed-mismatch`: complete, matching provenance and an explicit inspected
  setting conflict with the declared profile.
- `consistent-with-inspected-evidence`: inspected settings agree; capacity,
  board identity and runtime operation are still unverified.
- `unresolved`: missing settings/provenance, wrong environment, changed hashes,
  unsupported SDK mapping, conflicting modes or incomplete identity.
- `not-applicable`: outside this ESP32-S3 checker's scope.

Verify partition bounds with the SDK's partition generator and inspect the
actual build package/config outputs. A config pass does not validate partition
capacity, calibration retention, boot behavior or physical memory. See
[Espressif external RAM](https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-guides/external-ram.html)
and [flash/PSRAM configuration](https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-guides/flash_psram_config.html).
