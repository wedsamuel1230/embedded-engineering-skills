# Build-only platform fixtures

Run Python through the repository UV lock. These fixtures never select a port,
connect a probe, upload, erase or reset a board. SDK checkout/tool installation
is a separate trusted operation; the runner validates pinned local source.

```sh
uv sync --frozen --group firmware --group micropython
uv run --frozen --group firmware python scripts/validate_platforms.py --platform stm32cube --build-dir /path/to/fresh/stm32-evidence
uv run --frozen --group firmware python scripts/validate_platforms.py --platform zephyr --build-dir /path/to/fresh/zephyr-evidence
uv run --frozen python scripts/validate_platforms.py --platform pico-sdk --source /path/to/pico-sdk-2.2.0 --toolchain /path/to/arm-toolchain --build-dir /path/to/fresh/pico-build
uv run --frozen python scripts/validate_platforms.py --platform micropython --source /path/to/micropython-v1.26.1 --build-dir /path/to/fresh/mp-build
uv run --frozen --group micropython mpremote --help
```

| Fixture | Selected source/target | Scope |
|---|---|---|
| stm32cube | PlatformIO ststm32 19.5.0, F4 1.28.3, Nucleo F401RE | HAL initialization + idle cross-compile |
| zephyr | PlatformIO ststm32 19.5.0, Zephyr 4.3.0, Nucleo F401RE | kernel sleep + idle cross-compile |
| pico-sdk | SDK 2.2.0, commit a1438dff1d38bd9c65dbd693f0e5db4b9ae91779, RP2040/pico | ELF only, no peripheral/stdout configuration |
| micropython | v1.26.1, commit 647c8b96cae7e202c7a020395b7cfe65e5b8ce04, Unix minimal | real interpreter build + pure-Python smoke |

The MicroPython runner applies two explicit Darwin build settings: pthread is
enabled to provide declarations used by the release's Darwin realtime code,
and Apple Clang constant-folding warnings stay warnings under upstream Werror.
All other diagnostics retain their policy. No upstream source is patched;
this is minimal-with-pthread smoke evidence, not a threading test. Ordinary
minimal is used on POSIX Linux. Native Windows Unix-port builds are not offered;
use WSL or an appropriate board-specific Windows workflow.

The runner records command argv, exit code and log hashes in `result.json`.
Use a fresh empty directory; it never deletes old evidence. PlatformIO places
firmware artifacts under its fixture `.pio/`, while the evidence directory holds
logs. Generated firmware, external SDKs and caches are excluded from packages.
The Zephyr fixture's project-level `west.yml` selects CMSIS, CMSIS_6 and
STM32 HAL at fixed upstream hashes. Archive that manifest and resolved module
list for reproducibility; arbitrary projects need their own dependency closure. A source/pin
check is not a supply-chain audit or a complete dependency-graph proof.
