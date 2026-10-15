# Desktop telemetry and bench console

Reuse the existing serial capture skill and project protocol. Choose a
versioned schema, explicit units, device boot/state timing, receiver freshness
and bounded history. Use the same Python entry point on macOS and Windows;
keep dependencies pinned through uv. Test each launcher on its actual host
before labeling it host-validated. A portable script is not Windows evidence.

Opening serial can reset a target through DTR/RTS. Confirm port, chip, transport
and reset requirements before connecting. For wireless traces use
`wireless-telemetry`, its explicit offline schema and interpretation rules.
Do not present receiver age as synchronized one-way latency or sampled state
as a complete transition trace.

If driving is requested, implement the shared
[bench-control contract](../../wireless-telemetry/references/bench-control-contract.md).
The UI must send STOP on emergency input, blur/focus loss and disconnect;
local/browser/bridge/device leases have separate responsibilities. Held-key
auto-repeat or a reconnect must not resume motion after STOP without a fresh
trusted re-arm. Authenticated device mode and bounds remain authoritative.

Start with simulated data and assert stale display, malformed packets, restart,
rapid transitions, capped history, lease expiry and STOP/key-repeat behavior.
Then test the actual device, transport and physical stop. Do not copy robot
passwords, protocol keys or live control interfaces into a general template.
