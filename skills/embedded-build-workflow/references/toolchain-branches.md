# Distinct framework and build-manager branches

Preserve the selected project and environment. Commands below are examples for
an inspected, trusted project; substitute verified identity/version inputs.
Device commands require their target state and existing authorization.

| Framework/manager | Inspect before building | Build-only path | Boundaries |
|---|---|---|---|
| PlatformIO Arduino or ESP-IDF | `platformio.ini`, effective named environments, platform release, framework package, board JSON, dependencies | `uv run --frozen platformio run --project-dir PATH -e ENV` when a locked uv project exists | A PlatformIO platform release does not imply the latest Arduino core. `extra_scripts` can execute code during a build. |
| Native ESP-IDF | SDK revision, exported tool environment, CMake component graph, target, generated sdkconfig and partition table | `idf.py build` in the selected project/tool environment | Do not run `set-target` casually: it changes configuration/build state. Arduino driver APIs need deliberate native adaptation. |
| Arduino CLI | CLI/core/library versions, FQBN and sketch ownership | confirmed CLI `compile` command from `arduino-cli-skill` | Never route an `app_main` native project to Arduino compilation. |
| Zephyr/west | workspace and frozen manifest revision, board qualifier, overlays/Kconfig and SDK | source-backed `west build` for the exact board | A board name, shield and runner can be version-sensitive; see the exact fixture coverage. |
| Pico SDK | SDK revision, CMake toolchain, `PICO_BOARD`, SDK import/init | project CMake configure/build | Arduino-Pico and native Pico SDK are distinct; see the exact fixture coverage. |
| STM32Cube | exact MCU/board, Cube generator, presets or generated Makefiles, linker script, toolchain | existing CMake preset or generated Makefile target | Do not infer CubeCLT means CMake; see the exact fixture coverage. |

| MicroPython | exact port/BOARD, interpreter revision, host tool and .mpy ABI | port-specific firmware build; Unix port smoke test separately | CPython compileall is not target proof. |

For PlatformIO inheritance use `pio project config --json-output`; select only
non-secret environment/version fields for a report. Do not replace PlatformIO
with a homegrown interpolation engine. Resolve locks at their owning layer:
`uv.lock` fixes host Python dependencies, not every firmware framework/library.
Keep immutable platform/library revisions and record the actual package list
from the build. Mutable URLs, branches and floating ranges need an explicit
reproducibility limitation.


## Primary references

- [PlatformIO project configuration](https://docs.platformio.org/en/stable/projectconf/index.html)
  and [computed config](https://docs.platformio.org/en/stable/core/userguide/project/cmd_config.html).
- [PlatformIO Espressif32](https://docs.platformio.org/en/stable/platforms/espressif32.html)
  and [ESP-IDF build system](https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-guides/build-system.html).
- [Zephyr west](https://docs.zephyrproject.org/latest/develop/west/build-flash-debug.html)
  and [manifest](https://docs.zephyrproject.org/latest/develop/west/manifest.html).
- [Pico SDK](https://github.com/raspberrypi/pico-sdk/blob/master/README.md).
- [ST CMake AN5952](https://www.st.com/resource/en/application_note/an5952-how-to-use-cmake-in-stm32cubeide-stmicroelectronics.pdf)
  and [CubeCLT UM3088](https://www.st.com/resource/en/user_manual/um3088-stm32cube-commandline-toolset-quick-start-guide-stmicroelectronics.pdf).

- [MicroPython ports](https://github.com/micropython/micropython/tree/v1.26.1/ports) and [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html).
