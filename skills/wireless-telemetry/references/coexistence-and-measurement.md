# Coexistence and measurement contract

Define endpoints, framework/SoC version, radio role, channel, packet format,
payload/cadence, provisioning and overload policy. A UDP snapshot may prioritize
freshness; ordered commands and state-change events need their own semantics.
No transport selection alone guarantees a latency or loss target.

ESP-NOW peer/channel/payload behavior varies by target and version. Keep callbacks
short and hand data to bounded worker queues. MAC success is not an application
acknowledgement. AP+STA uses a shared home channel; the station connection can
move the AP to its channel. A remote ESP-NOW receiver must follow or deliberately
remain disconnected. Capture reconnect/channel changes rather than assuming a
peer with channel zero makes every remote peer follow automatically.

| Quantity | Required evidence | Do not substitute |
|---|---|---|
| RTT | matched request/reply on the same endpoint's monotonic clock | difference between unsynchronized device and PC timestamps |
| Receive interval | successive arrivals on one receiver clock/session | control task duration |
| Sample age | defined source or receiver freshness basis | one-way transit latency |
| Observed gaps | boot/stream identity, sequence width and capture behavior | loss rate without an established sender count and complete capture |
| Control response | device trace from input acceptance to actual output | UDP local-send or ESP-NOW callback success |

Record sample count, duration, load, duplicate/reorder/wrap rules and rejected
records. A host clock subtraction is only valid inside its declared clock
domain. Use the [explicit trace schema](trace-schema.md), not generic CSV column
guessing. Also measure stale stops, reconnection, congestion, interference and
safe update behavior on the actual target before claiming system performance.

Primary sources:
[ESP-NOW](https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-reference/network/esp_now.html),
[Wi-Fi/AP+STA](https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32s3/api-guides/wifi-driver/overview.html).
Security checks remain separate: peer keys/provisioning, application command
authentication, replay domain and secret storage require explicit design.
