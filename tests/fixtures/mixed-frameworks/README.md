# Trusted build fixtures

These minimal, non-actuating projects exercise Arduino and native ESP-IDF
build dispatch on the same declared ESP32-S3-DevKitC-1 N16R8 profile.
Arduino uses a pinned pioarduino release for core 3.3.8; native uses
PlatformIO Espressif32 7.0.1 / ESP-IDF 6.0.1. Record actual packages in each log.
Native selects DIO flash operation on quad-capable flash and octal PSRAM; DIO
versus QIO is an explicit build choice, not a different physical capacity.

Run from the repository root after reviewing these fixture sources:

```sh
uv sync --frozen --group firmware
uv run --frozen --group firmware platformio run --project-dir tests/fixtures/mixed-frameworks/arduino -e arduino-n16r8
uv run --frozen --group firmware platformio run --project-dir tests/fixtures/mixed-frameworks/native -e native-n16r8
```

No upload, port opening or board behavior is tested. Build outputs remain
ignored. Record OS, Python/PlatformIO/compiler/framework versions, source hashes,
commands and exits in the evolution acceptance record. These commands use the
same uv interface on Windows, but only an actually run host earns build credit.
