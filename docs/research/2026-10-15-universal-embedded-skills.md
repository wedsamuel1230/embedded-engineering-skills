# Cross-platform embedded skill research

Checked 2026-10-15 by a `gpt-6-luna` background researcher. This is a selective
source-body survey, not a popularity ranking. No upstream skills were installed
or copied. GitHub commit/date/license metadata and body availability were
independently checked; see [verification data](2026-10-15-source-verification.json).
License metadata describes the inspected repository, not a license review of
every dependency. Techniques below are paraphrased and newly implemented.

## Existing skills: useful techniques and boundaries

| Commit-pinned source | License | Technique adopted or used | Deliberately not adopted |
|---|---|---|---|
| [beriberikix Zephyr](https://github.com/beriberikix/zephyr-agent-skills/blob/ed63cdfb8cdfbeb5946ea39c33f4aa6bcf3a5cce/SKILL.md), 2026-05-18 | Apache-2.0 | Separate routing metadata, focused references and executable validation; source-backed Zephyr workflow pointers. | Importing its entire catalog or equating a catalog with tested target support. |
| [magnus919 ESP32](https://github.com/magnus919/agent-skills/blob/b3b45651ffa2ca882911c2ebfeeab8e3dc7b53ce/esp32-development/SKILL.md), 2026-10-13 | MIT | Read-only preflight, exact target/framework intake and distinction between a source index and verified claims. | Treating framework breadth as build proof, or opening serial ports as harmless discovery. |
| [Claudius GPIO](https://github.com/claudius-ars/embedded-agent-skills/blob/51039fe6400b91e792ff723879a68134ceac75ff/embedded-agent-skills/gpio-config/SKILL.md), 2026-02-08 | MIT | Variant-aware constraint checks and negative fixtures for configuration mistakes. | Importing pin databases as authoritative board/schematic facts. |
| [EZRover ESP32](https://github.com/ezrover/ESP32-AI-Agent-Skill/blob/124d298e4ccaa737dbf6d26bbae47722e17f3097/skills/esp32/SKILL.md), 2026-04-14 | MIT | Deterministic checks for easily missed variant and memory configuration details. | Reusing variant tables without Espressif and carrier-board evidence. |
| [lhbsaa embedded](https://github.com/lhbsaa/embedded-dev-skill/blob/69267c3c65157e187250551baf22f5c49311ef91/SKILL.md), 2026-07-21 | MIT | Explicit discovery branches across MCU families. | A large combined skill and universal quick-reference numbers. |
| [rovinax architecture](https://github.com/rovinax/embedded-skills/blob/022ce31b469b1a1d0c1261c2c8d0f3e07b2c0bbc/skills/embedded-architecture/SKILL.md), 2026-05-24 | MIT | Separate portable decision logic from platform drivers. | Imposing one architecture on tiny sketches. |
| [awknode ESP32](https://github.com/awknode/hermes-agent-skills/blob/c47f6044826bbad2f593629815f95c1ce87b3e78/esp32-development/SKILL.md), 2026-07-27 | MIT | Framework choice and exact schematic/datasheet belong in intake. | Broad framework claims without individual validation paths. |
| [embedded Rust](https://github.com/mohitmishra786/low-level-dev-skills/blob/bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608/skills/embedded/embedded-rust/SKILL.md), 2026-06-27 | MIT | Distinct `no_std`, target-triple, probe and logging workflow. | Advertising Rust compilation/target support before a selected fixture runs. |

## Official mechanisms and implementation consequences

- PlatformIO configurations have common and named environments, interpolation
  and external configuration inputs. An offline subset reader must expose its
  limitations; use the native computed-configuration command when resolution
  matters. [Project configuration](https://docs.platformio.org/en/stable/projectconf/index.html),
  [computed configuration](https://docs.platformio.org/en/stable/core/userguide/project/cmd_config.html).
- ESP-NOW callback work belongs outside the high-priority Wi-Fi callback path.
  MAC-layer delivery and application receipt differ. AP+STA channel behavior
  constrains coexistence. These are target/version-specific design inputs.
  [ESP-NOW 6.0.1](https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-reference/network/esp_now.html),
  [Wi-Fi 6.0.1](https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-guides/wifi-driver/overview.html).
- OTA application confirmation follows boot diagnostics; flash slots alone do
  not establish rollback or persistent-data compatibility. Keep actual reset,
  power-loss and NVS recovery tests separate from host logic.
  [OTA 6.0.1](https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-reference/system/ota.html).
- Zephyr's manifest is a multi-repository revision map. Freeze revisions rather
  than assuming a branch gives reproducibility; board/runner identity belongs
  in the build/flash handoff. [West manifests](https://docs.zephyrproject.org/latest/develop/west/manifest.html),
  [build/flash/debug](https://docs.zephyrproject.org/latest/develop/west/build-flash-debug.html).
- Pico SDK uses its own CMake import, SDK initialization and board selection.
  Do not substitute Arduino-Pico settings. [Pico SDK](https://github.com/raspberrypi/pico-sdk/blob/master/README.md).
- STM32Cube CMake presets and CubeCLT's IDE-generated Makefile workflow are
  different paths. Discover the actual project generator before proposing
  commands. [AN5952](https://www.st.com/resource/en/application_note/an5952-how-to-use-cmake-in-stm32cubeide-stmicroelectronics.pdf),
  [UM3088](https://www.st.com/resource/en/user_manual/um3088-stm32cube-commandline-toolset-quick-start-guide-stmicroelectronics.pdf).
- Embedded Rust needs a target, crate/toolchain versions and a compatible probe.
  `probe-rs run` and attachment have different device effects. [Embedded Rust](https://doc.rust-lang.org/embedded-book/intro/tooling.html),
  [`no_std`](https://doc.rust-lang.org/embedded-book/intro/no-std.html),
  [probe-rs](https://probe.rs/docs/tools/probe-rs/).
- Skills benefit from concise trigger descriptions, progressive disclosure,
  positive/negative/near-miss cases and a held-out split. Static term checks do
  not measure activation behavior. [Agent Skills specification](https://agentskills.io/specification),
  [description evaluation](https://agentskills.io/skill-creation/optimizing-descriptions).

## Social-source signals

The researcher used a separate logged-in Brave research tab. The exact phrase
`embedded agent skills` returned no visible Latest results. One broader Top
search `(ESP32 OR Zephyr) (skills OR agent)` produced these inspected posts:

| Post | Observed signal | Corroboration and adoption |
|---|---|---|
| [@wangray](https://x.com/wangray/status/2110216386777882771), displayed 13 hours earlier | ESP32 USB-HID plus desktop vision/feedback automation. | [Linked source repo](https://github.com/onehumanbeing/esp32-iphone-agent) documents controller/firmware boundaries, recovery and emergency stop. Adopt explicit per-action observations and stop/recovery considerations. Cost/popularity/compatibility marketing was not validated. |
| [@KobinFlow](https://x.com/KobinFlow/status/2109967875574509613), displayed Oct 13 | Broad beginner ESP32 platform advice, without a board in hand. | No visible primary-source corroboration. No technical claims adopted. |
| [@Jack_FluxAI](https://x.com/Jack_FluxAI/status/2109680124216156337), displayed Oct 13 | Anecdotal AI flashing failure and recovery. | No visible source repository or reproducible evidence. Use only as a signal that recovery matters. |

These are a small accessible sample, not evidence that no other posts exist.
No Jev browser fallback was needed after direct browser access worked.

## Recommendation and gaps

Implement the three focused workflows first; keep OTA and desktop-console
extensions under existing owners. Run real Arduino and native-IDF builds on
the exact fixture target. Keep other ecosystems reference-only until they earn
their own build/host evidence. BottleSumo constants, pins, timings, passwords
and competition decisions are examples, not global defaults.

The research itself ran no firmware build, model activation benchmark, radio
measurement or powered hardware test. Validation must be recorded separately
in the [evolution record](2026-10-15-plugin-evolution.md).
