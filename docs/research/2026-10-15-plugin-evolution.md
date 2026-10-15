# Embedded Engineering Skills: local evolution record

Date: 2026-10-15. Source branch: `codex/universal-embedded-skills`.
This is the historical 1.9 design, consultation, and acceptance record.
The user subsequently authorized 2.0 platform expansion and identity migration;
see [the current record](2026-10-15-platform-expansion-implementation.md). It is not a
release announcement or hardware certification.

## Scope and architecture assessment

The first job is maintaining or migrating an existing embedded repository.
Keep the original 30 skills and stable `arduino-skills` host identifiers.
Add three independently useful jobs: build intake and migration; control
ownership and deadline design; wireless transport and trace analysis.
Extend existing FreeRTOS, OTA and serial-monitor entry points rather than
introducing duplicate schedulers, deployment engines or dashboards.

The shared intake/evidence contract remains authoritative. Native framework
commands remain distinct. Inspection helpers run offline, never invoke build
scripts or devices, and expose unresolved configuration instead of emulating
PlatformIO. Firmware compile fixtures are a separate trusted execution step.
This blueprint addresses the Arduino-CLI-biased router without requiring a
universal command runner. Physical board identity remains independent of a
module's memory designation.

## Research and consultations

- `research` ran in a clean background context with **gpt-6-luna**, as requested.
  The first attempt using the configured research role failed because its
  `gpt-5.4` model was unavailable. It produced no findings and was replaced by
  the explicitly requested model.
- The [source survey](2026-10-15-universal-embedded-skills.md) examines eight
  commit-pinned GitHub skill bodies, their license metadata and official SDK
  documentation. The primary independently checked commit dates, licenses and
  body availability through GitHub's API and read representative source bodies.
- [BottleSumo lessons](2026-10-15-bottlesumo-lessons.md): TypeSafe/Jev judged six
  redacted candidates. Five were written and verified by lesson keys; one
  control-ownership candidate was dropped as a duplicate. These are reusable
  source notes, not proof that a future agent automatically retrieves them.
- [Poe GPT-6-Astra grilling](https://poe.com/chat/aan9x8m419kdumvwvb) had three
  rounds: scope/support tiers; helper/measurement/OTA failure modes; acceptance
  blockers. Only summarized public engineering facts were submitted. Astra's
  answers are advisory, not authority or technical verification.

## Settled decisions

1. Use **Embedded Engineering Skills** as display positioning, explicitly
   Arduino/ESP-IDF-first. Propose a later identity migration separately.
2. Classify support as reference-only, build/host-validated, or
   hardware-validated for an exact framework/toolchain/target/host combination.
3. Keep four memory-check outcomes: confirmed mismatch, consistent within
   inspected evidence, unresolved, not applicable. Bind generated artifacts to
   environment, input hashes and tool versions. Do not infer runtime PSRAM size.
4. Define one telemetry CSV schema. Report observed forward gaps, duplicate and
   late/stale packets; never infer packet-loss rate from incomplete capture.
   RTT uses one clock and session/request identity. No unsynchronized one-way
   subtraction is offered.
5. Put the bench drive-lease contract in one reference and link desktop/OTA
   guidance to it. Host examples prove logic, not actuator stopping.
6. Define rollback-image compatibility of persistent records explicitly. A
   retained NVS partition is insufficient if the old image cannot read it.
7. Keep Zephyr, Pico SDK, STM32 and embedded Rust as sourced reference routes
   until exact fixtures earn stronger evidence. No extra ecosystem runtime or
   speculative universal pin database is introduced.

## Acceptance record

Baseline: package validators passed for 30 skills, shared contract 8/8 themes,
and deterministic forward-contract cases 20/20. These checks do not invoke a
model or build firmware. Candidate verification recorded:

- package, references, stable host identifiers and install-path checks;
- offline helper and synthetic trace tests, including negative/ambiguous data;
- two pinned, non-actuating Arduino/native-IDF compile fixtures;
- a bounded, clean-context routing comparison, with individual outputs and
  failures; no aggregate trigger-accuracy claim;
- source-note retrieval through active skill/router links;
- known gaps: Windows execution, RF timing/loss, powered hardware, actual OTA
  power interruption, calibrated motor/sensor behavior and remote rename.

## Brand artifact

The logo uses the built-in `imagegen` tool, not the API/CLI fallback. Final
asset: `assets/embedded-engineering-logo.png`, a generated transparent PNG.
Prompt: a compact, platform-neutral microcontroller symbol with a continuous
circuit path, balanced negative space and a strong small-size silhouette;
centered square framing, no text, no vendor marks, no watermark, true alpha.


## Verified local candidate

On macOS, Python 3.12.13 through `uv`, package validation checks 33 skills with
zero errors; the shared contract passes 8/8 themes, the retained deterministic
suite passes 20/20 cases, and 24 new offline parser/provenance/trace tests pass.
The C++17 lease fixture passes with `-Wall -Wextra -Werror`. `git diff --check`
passes. Stable plugin names, repository URLs and marketplace install targets
remain `arduino-skills`. The logo is square 1254 x 1254 RGBA with alpha.

Both separate trusted compile fixtures passed locally: PlatformIO Core 6.2.0,
Arduino-ESP32 3.3.8 via pioarduino 55.03.38-1, and native ESP-IDF 6.0.1 via
platformio/espressif32 7.0.1, DevKitC-1 N16R8. These fixtures contain no actuator
operations. Native generated flash mode is DIO, which is compatible with a
quad-capable flash device; it is not proof of a different physical memory bus.
No fixture input changed after those builds. The new GitHub Actions definition
has not been run remotely; Windows/Linux execution credit is not claimed.

The seven-case [Luna routing comparison](../../evals/embedded-routing-probe.json)
is a primary summary of both handbacks, with individual routes, references and
limitations. Baseline already identified the major safety boundaries. Candidate
provides narrower, directly reachable procedures. The candidate's
`unsafe_action_allowed` field was interpreted inconsistently with its prose;
its raw flags are preserved and excluded from accuracy claims. One alignment
message told both agents to read the same frozen prompts. This was not a
first-shot automatic skill-activation test.

## Final architecture and scoped code review

The primary read the changed helpers, callers, boundary tests, teaching lease,
provider adapters and build fixtures. Expected load is one local user inspecting
bounded repositories or a bounded CSV, not a deployed multi-user service.
The review found a duplicate flash-mode setting that could evade uncertainty
handling, plus non-string physical identity declarations. Both were fixed with
a regression case. An obsolete validator dependency on a workstation-only
research file was removed. No generic execution engine, statistics framework,
persistence migration runtime or firmware deployment tool was added.

Remaining review limits: target timing, RF, physical stop, actual OTA recovery,
Windows execution and remote host installation. The historical system
`plugin-creator` validator was unavailable locally; the repository validators
and current official manifest/image schema checks ran instead. Skill-improver
packaging scripts assume a different `.agents/skills`/Codex Loop layout and were
not presented as validation of this plugin. The whole-root review archive is
verified separately with checksums and extraction checks.

## Source lesson retrieval

The active router and build/control/wireless skills link the adopted lesson
file. A local link/key check verifies all five keys are present and reachable;
the candidate Luna mixed-build handback actually selected the lesson file.
That is bounded retrieval evidence, not proof of automatic future injection or
a measured benefit for every lesson in every request.

## Review archive checks

The whole-root review archive contains 33 skills and 273 files. It includes the
shared references, provider manifests, logo, UV lockfile, tests and two firmware
fixture sources. It omits Git/cache/build output and historical workstation
workflow ledgers/eval outputs; one historical CHANGELOG home-path reference is
normalized to `~/` in the archive only. `PACKAGE-CHECKSUMS.json` records every
payload SHA-256 and that normalization. Extraction verified all checksums; all
three repository validators, 20 deterministic cases, 24 offline tests and the
C++ lease test passed again from the extracted root.

The CI YAML parsed successfully. Push/PR/manual triggers, read-only permissions,
three host entries and both pinned action commits were verified against GitHub.
This checks the definition, not a remote CI run. No plugin cache installation,
Git commit/push, publication or remote rename was performed for this source.
