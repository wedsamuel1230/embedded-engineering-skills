# Embedded Engineering Skills source

The canonical skill content is under `skills/`. Select the smallest matching
`SKILL.md`, and load `references/` or `docs/` only when the skill points to it.

Preserve the raw ordered `constexpr int` pin-declaration convention and
C/C++ conventions for native firmware. For explicitly selected MicroPython,
use that port's Python/runtime conventions instead. Keep compile, upload, hardware, system, and
deployment evidence separate. Do not claim physical success without a user
provided measurement, log, or photo.

For physical or multi-session work, load `skills/embedded-project-loop/SKILL.md`
first, then use the workflow router for specialist routing.

Provider manifests in `.codex-plugin/`, `.claude-plugin/`, and
`.cursor-plugin/` are adapters only; do not duplicate skill instructions there.


Browse `catalog/README.md` by job; keep actual bundles flat under `skills/`.
Current platform routes include Arduino, ESP-IDF, Zephyr, STM32Cube, Pico SDK
and MicroPython. Rust is deferred. Validate with the repository validators and
`uv run --frozen python -m unittest discover -s tests -p 'test_*.py'`.
Build-only platform fixtures use `scripts/validate_platforms.py`; do not infer
hardware success or silently choose a port/probe. New plugin identity is
`embedded-engineering-skills`; old installed IDs need an explicit host upgrade.
