---
name: usb-debugging
description: Diagnose embedded USB enumeration, descriptors, CDC/REPL ports and intermittent disconnects. Use when requests involve a missing USB device, wrong interface, native USB versus serial bridge, endpoint failures or conflicting monitors.
metadata: {triggers: "USB Debugging, embedded diagnosis"}
---

# USB Debugging

Read [the shared embedded contract](../../docs/arduino-skill-contract.md) and
keep source/build, device and physical evidence separate.

Read [USB diagnosis](references/workflow.md). Identify connector, data-capable
cable, power path, native USB controller versus UART bridge, VID/PID, interfaces,
serial identity and host OS. Record enumeration before and after the event;
a changing port name is not necessarily a different physical board.

Separate no electrical connection, failed enumeration, missing driver/interface,
port ownership and application protocol. Record descriptors, endpoint types,
configuration and host logs with credentials/private serials redacted in public
reports. Check D+/D- wiring, clock/PHY/VBUS expectations and power externally
only against the exact board design.

Close conflicting serial monitors before a selected REPL/debug session.
MicroPython raw REPL and auto-reset tools can change runtime state. Native
USB may disappear during reset, breakpoint halt or firmware reconfiguration;
a UART bridge can remain enumerated while the MCU is stopped.

Use the matching platform skill for USB stack configuration. Deliver the layer
where evidence stops, a reproducible host check and the next targeted test.
Do not erase firmware or reinstall arbitrary drivers to fix an unidentified
transport symptom.

See [platform coverage](../../docs/platform-support.md) for the exact tested
combination. A source procedure is not a claim that every target was tested.
