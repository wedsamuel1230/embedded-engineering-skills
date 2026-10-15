# Protocol branches

| Bus | Check before changing firmware | Distinguishing evidence |
|---|---|---|
| SPI | CPOL/CPHA, bit order, frequency, CS polarity/setup/hold, dummy bytes | capture CS/SCK/MOSI/MISO together; shared-bus device releases MISO |
| UART | logic UART versus RS-232/RS-485, voltage, baud/error, parity/data/stop, flow control | raw bytes and framing/overrun flags; differential transceiver direction where present |
| I2C | 7-bit versus shifted address, repeated START, ACK/NACK phase, clock stretching | exact transaction with pull-up/rise-time scope evidence separately |
| CAN | transceiver, nominal/data phase rates, sample point, termination and shared reference | error counters, error frames/bus-off, known peer ACK; loopback alone is not physical-bus proof |

A logic analyzer sample rate and threshold must resolve the fastest edge/event
of interest; capture setup itself can alias or misdecode traffic. An oscilloscope
addresses ringing/levels/rise time. Do not infer a universal safe frequency or
resistor from a framework name. Consult the exact device/board datasheets.

Primary sources: [Zephyr SPI](https://docs.zephyrproject.org/latest/hardware/peripherals/spi.html),
[Zephyr UART](https://docs.zephyrproject.org/latest/hardware/peripherals/uart.html),
[Zephyr CAN](https://docs.zephyrproject.org/latest/hardware/peripherals/can/controller.html),
[Pico hardware APIs](https://www.raspberrypi.com/documentation/pico-sdk/hardware.html).
