# Native ESP-IDF OTA, stopped outputs and persistent compatibility

Use the selected chip/SDK documentation. This reference is checked against
ESP-IDF 6.0.1 for ESP32-S3; other versions need their own API/config checks.
Follow `embedded-build-workflow` for the build and partition source of truth.

Before implementing updates, identify image authentication/verification, app
slots, OTA metadata, NVS/calibration partitions, fallback images and physical
recovery. Verify the layout using the SDK partition tools and actual image
sizes. Do not equate a CRC, plaintext password or valid image header with a
signed/authenticated deployment.

Keep these gates independent:

- **Motion:** the actuator owner acknowledges stopped outputs before flash
  writes. Networking merely requests the lock. A timeout rejects the update.
- **Authorization:** an actuator system needs a trusted, expiring physical/local
  update arm appropriate to its requirements. See the shared
  [bench authority](../../wireless-telemetry/references/bench-control-contract.md).
- **Boot acceptance:** define bounded boot diagnostics before confirming a new
  image with the SDK rollback API. Do not mark it valid unconditionally at entry.
- **Data validity:** calibration records carry schema version, sensor identity,
  applicability and integrity evidence. Invalid/missing data causes explicitly
  chosen safe defaults or a fault state; it is never silently valid.
- **Recovery:** name exactly which old/recovery images must read retained data.
  Destructive migrations can invalidate fallback even after the current image
  was accepted. Require backward-compatible records, a transactional migration
  with a tested recovery contract, or explicitly retire the incompatible image
  under separate authorization. Do not invent a migration engine.

| Failure case | Host/design check | Separate target evidence |
|---|---|---|
| Update requested during motion/unarmed/expired window | rejection and stop-lock state transitions | actual outputs remain safe |
| Bad/oversized/interrupted image | error path and partition/image bounds | actual interrupted-write recovery |
| New image fails boot diagnostics | no premature confirmation; rollback path | bootloader returns to old image |
| Old reader sees new/corrupt/unknown record | schema compatibility and safe fallback | NVS data survives reset/power loss |
| Calibration belongs to another sensor | applicability rejection | measured sensor identity/behavior |

Retain calibration separately from replaceable apps, but do not claim that
retention alone proves interpretability. Keep secrets provisioned outside
firmware images; don't recommend an unconditional NVS erase as generic recovery.
Report actual OTA/rollback/power-cut behavior unverified until tested.

Primary sources: [OTA and rollback](https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-reference/system/ota.html),
[partition tables](https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-guides/partition-tables.html),
[NVS](https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-reference/storage/nvs_flash.html).
