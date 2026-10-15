#pragma once
#include <cstdint>

// Teaching fixture only. Caller owns authentication, physical mode and outputs.
class LeaseGuard {
 public:
  explicit LeaseGuard(std::uint32_t duration_ms) : duration_(duration_ms) {}
  bool arm(bool physical_bench, bool outputs_stopped, std::uint32_t session,
           std::uint32_t now) {
    stop();
    if (!physical_bench || !outputs_stopped || !duration_ || duration_ >= 0x80000000u)
      return false;
    armed_ = true; session_ = session; accepted_at_ = now; seen_ = false;
    return true;
  }
  bool live(std::uint32_t now) {
    if (armed_ && now - accepted_at_ >= duration_) stop();
    return armed_;
  }
  bool accept(std::uint32_t session, std::uint32_t sequence, std::uint32_t now) {
    if (!live(now) || session != session_) return false;
    const auto delta = sequence - sequence_;
    if (seen_ && (!delta || delta >= 0x80000000u)) return false;
    sequence_ = sequence; seen_ = true; accepted_at_ = now;
    return true;
  }
  void stop() { armed_ = false; }

 private:
  std::uint32_t duration_, session_ = 0, sequence_ = 0, accepted_at_ = 0;
  bool armed_ = false, seen_ = false;
};
