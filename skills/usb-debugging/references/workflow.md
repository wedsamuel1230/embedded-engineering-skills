# USB diagnosis

On macOS inspect System Information / USB and the exact `/dev/cu.*` identity;
on Windows inspect Device Manager hardware IDs, interfaces and COM ownership;
on Linux use the selected device's `lsusb` descriptors and kernel log. Inventory
commands do not establish CDC, HID or vendor-protocol communication.

For TinyUSB/native USB preserve the exact descriptor/configuration and build
options. Validate total/config/interface/endpoint lengths and endpoint direction,
packet sizes and interface ownership for that speed/controller. Do not infer
high-speed USB capability from a fast CPU or a USB-C connector.

Capture whether failure occurs before enumeration, setting configuration,
opening a class interface or transferring application data. Disconnect/reconnect,
resume and debugger halt are different triggers. Avoid remote debug/trace
exposure as a workaround for local port ownership.

Primary sources: [TinyUSB](https://docs.tinyusb.org/en/latest/),
[Zephyr USB device stack](https://docs.zephyrproject.org/latest/connectivity/usb/device/usb_device.html),
[MicroPython mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html),
[Microsoft USB descriptors](https://learn.microsoft.com/en-us/windows-hardware/drivers/usbcon/usb-descriptors).
