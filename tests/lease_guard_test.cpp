#include <cassert>
#include <cstdint>
#include "../skills/wireless-telemetry/examples/lease_guard.h"

int main() {
  LeaseGuard guard(100);
  assert(!guard.arm(false, true, 7, 0));
  assert(!guard.accept(7, 1, 1));
  assert(!guard.arm(true, false, 7, 0));
  assert(guard.arm(true, true, 7, 0));
  assert(!guard.accept(8, 1, 1));
  assert(guard.accept(7, 1, 10));
  assert(!guard.accept(7, 1, 99)); // duplicate cannot renew authority
  assert(!guard.live(110));
  assert(!guard.accept(7, 2, 111)); // expiry requires fresh trusted re-arm
  assert(guard.arm(true, true, 8, 200));
  assert(guard.accept(8, 0xffffffffu, 210));
  assert(guard.accept(8, 0, 220)); // sequence wrap
  assert(!guard.accept(8, 0xffffffffu, 230));
  assert(!guard.accept(8, 0x80000000u, 230)); // half-range is not newer
  guard.stop();
  assert(!guard.accept(8, 1, 240));
  assert(guard.arm(true, true, 9, 0xfffffff0u));
  assert(guard.accept(9, 1, 0xfffffffeu));
  assert(guard.live(20)); // local timer wrap
  assert(!guard.live(98));
  LeaseGuard zero(0), ambiguous(0x80000000u);
  assert(!zero.arm(true, true, 1, 0));
  assert(!ambiguous.arm(true, true, 1, 0));
}
