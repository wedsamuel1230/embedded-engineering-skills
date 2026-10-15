# Zephyr workspace, configuration and debugging

- Preserve the repository's pinned west manifest; record `west --version`,
  `west list` revisions and the selected SDK. `west update` downloads and changes
  projects; inspect its scope separately from build-only commands.
- Board qualifiers differ by Zephyr release. Use `west boards` from that
  workspace; retain the exact target, SoC/CPU qualifier and overlays.
- Devicetree is resolved at configure time. Inspect `BUILD/zephyr/zephyr.dts`
  and generated headers for final pinctrl/clock/interrupt relationships.
- `west build -d BUILD -t menuconfig` edits generated configuration; preserve a
  minimal source-controlled `prj.conf`/overlay change after diagnosing it.
- Use build-specific `west debug --context`/runner help where supported before
  connecting. A debugger halt may stop scheduling/watchdogs while DMA or an
  external actuator continues. Account for it in the target setup.
- This package has a pinned PlatformIO Zephyr compile fixture, not a universal
  west workspace or all-board SDK installation. See the support matrix for the
  actual resolved version and host; newer upstream releases are separate proof.

Primary sources: [west build/flash/debug](https://docs.zephyrproject.org/latest/develop/west/build-flash-debug.html),
[manifest](https://docs.zephyrproject.org/latest/develop/west/manifest.html),
[devicetree](https://docs.zephyrproject.org/latest/build/dts/index.html),
[Kconfig](https://docs.zephyrproject.org/latest/build/kconfig/index.html),
[PlatformIO STM32](https://docs.platformio.org/en/latest/platforms/ststm32.html).
