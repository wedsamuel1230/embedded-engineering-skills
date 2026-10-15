# Bench-only command authority

This is the single drive-lease reference for telemetry, control, desktop
console and OTA guidance. It describes a design contract, not a complete
robot controller or certified stop mechanism.

1. Select bench mode from trusted physical/local state. Autonomous operation
   rejects steering. A remote message cannot select or arm bench mode.
2. Authenticate/validate length, protocol, bounds, session and replay domain
   before accepting commands. Boot and session IDs are not authentication keys.
3. One actuator-owning control task checks authority every tick. A bridge or
   browser lease cannot replace the device-side lease.
4. Accept only newer commands in the current armed session; stale or duplicate
   commands do not refresh expiry. Use device-local monotonic receive time;
   do not trust unsynchronized sender wall time for the watchdog.
5. STOP, lease expiry, mode changes, OTA lock and faults revoke authority and
   request safe outputs. A reconnect or held key must not re-arm automatically.
6. Require stopped outputs plus a fresh trusted re-arm before accepting movement
   again. Choose lease duration from measured command cadence/response limits,
   not from this example. Define the independent hardware stop/recovery path.

[The minimal example](../examples/lease_guard.h) demonstrates session/sequence
and wrap-safe local lease arithmetic. It never touches hardware, receives a
network packet, authenticates a command or proves physical bench selection.
Its `arm` arguments must come from the real trusted physical/control owner.
Call `stop()` on mode/update/fault transitions. Unsigned timer intervals must
remain below half the uint32 range and polling must be frequent enough to stop
within the required response time.

Host verification includes autonomous refusal, wrong session, duplicate/replay,
expiry, timer/sequence wrap, STOP and fresh re-arm. Target testing must establish
that each condition actually yields the required actuator safe state, including
queue backlog, reconnect, browser focus loss, key-repeat and radio dropout.
No host assertion substitutes for that observation.
