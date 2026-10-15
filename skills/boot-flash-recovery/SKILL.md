---
name: boot-flash-recovery
description: Diagnose embedded boot, flash layout, image validation and reset loops with a non-destructive recovery path. Use when requests involve bootloader/application offsets, vector tables, partitions, bad firmware or a device that no longer starts.
metadata: {triggers: "Boot and Flash Recovery, embedded diagnosis"}
---

# Boot and Flash Recovery

Read [the shared embedded contract](../../docs/arduino-skill-contract.md) and
keep source/build, device and physical evidence separate.

Read [recovery decision path](references/workflow.md). Preserve original
boot/reset logs and identify board/chip, boot chain, image format, flash map,
security state and intended firmware before proposing a write. Readout may be
restricted; an empty or denied read is not proof the flash is erased.

Inspect available ELF/bin/hex/UF2 metadata offline. Compare partition/linker
addresses, vector-table placement, slot limits and image headers against the
exact target. File extension and binary length do not establish a load address.
Check supply/reset/boot straps and host port/probe ownership separately.

Choose the least destructive recovery supported by that exact board. Protect
calibration, provisioning, user files and security keys. Mass erase, unprotect,
factory reset, fuse changes and bootloader replacement have distinct effects;
never use them as an automatic first repair. A failed upload does not authorize
removing protection or bypassing signature/anti-rollback checks.

Use `probe-debugging` for target access, `usb-debugging` for enumeration and
`ota-deployment-guardian` for update-slot/persistent-schema compatibility.
Deliver the preservation plan, exact artifact/target/address, authorized write
steps if any, and separate verification after reset.

See [platform coverage](../../docs/platform-support.md) for the exact tested
combination. A source procedure is not a claim that every target was tested.
