#!/usr/bin/env python3
"""Analyze explicit schema-v1 telemetry/RTT CSV; never infer RF loss or one-way latency."""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import deque
from pathlib import Path
from statistics import mean

FIELDS = ["schema_version", "kind", "session_id", "stream", "boot_id", "seq", "rx_ms",
          "clock_id", "request_id", "request_ms", "reply_ms", "tx_clock_id"]
MAX_ROWS = 100000


def number(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed) or parsed < 0:
        raise ValueError("invalid-time")
    return parsed


def stats(values: list[float]) -> dict:
    if not values:
        return {"samples": 0, "units": "ms"}
    ordered = sorted(values)
    return {"samples": len(values), "units": "ms", "mean": mean(values), "min": ordered[0],
            "max": ordered[-1], "p95": ordered[math.ceil(len(ordered) * .95) - 1],
            "aggregation": "arithmetic mean; nearest-rank p95"}


def analyze(path: Path) -> dict:
    if path.stat().st_size > 25_000_000:
        raise ValueError("file-size-limit-exceeded")
    result = {"schema_version": 1, "status": "analysis-only", "rows": 0, "accepted_rows": 0,
        "rejected_rows": 0, "ambiguous_rows": 0, "duplicates": 0, "late_or_stale": 0,
        "sequence_wraps": 0, "observed_forward_gaps": 0, "duplicate_rtt": 0,
        "errors": [], "ambiguities": [], "loss_rate": None, "one_way_latency": None}
    sequences = {}
    arrivals = {}
    spans = {}
    requests = set()
    intervals, rtts = [], []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDS:
            raise ValueError("unsupported-or-reordered-schema")
        for line, row in enumerate(reader, 2):
            result["rows"] += 1
            if result["rows"] > MAX_ROWS:
                raise ValueError("row-limit-exceeded")
            try:
                if None in row or any(v is None or len(v) > 128 for v in row.values()):
                    raise ValueError("malformed-row")
                if row["schema_version"] != "1" or row["kind"] not in ("telemetry", "rtt"):
                    raise ValueError("unsupported-row-schema")
                if not row["session_id"] or not row["clock_id"]:
                    raise ValueError("missing-session-or-clock")
                if row["kind"] == "rtt":
                    if row["tx_clock_id"] != row["clock_id"] or not row["request_id"]:
                        raise ValueError("unmatched-request-or-cross-clock-rtt")
                    start, reply = number(row["request_ms"]), number(row["reply_ms"])
                    if reply < start:
                        raise ValueError("negative-rtt")
                    key = (row["session_id"], row["request_id"])
                    if key in requests:
                        result["duplicate_rtt"] += 1
                    else:
                        requests.add(key); rtts.append(reply - start)
                else:
                    if not row["stream"]:
                        raise ValueError("missing-stream")
                    rx = number(row["rx_ms"])
                    seq = int(row["seq"])
                    if not 0 <= seq <= 0xFFFFFFFF:
                        raise ValueError("sequence-out-of-range")
                    if not row["boot_id"]:
                        result["ambiguous_rows"] += 1
                        if len(result["ambiguities"]) < 20:
                            result["ambiguities"].append({"line": line, "reason": "missing-boot-identity"})
                        result["accepted_rows"] += 1
                        continue
                    key = (row["session_id"], row["stream"], row["boot_id"], row["clock_id"])
                    if key in arrivals and rx < arrivals[key]:
                        raise ValueError("nonmonotonic-receiver-clock")
                    if key in arrivals:
                        intervals.append(rx - arrivals[key])
                    arrivals[key] = rx
                    clock = (row["session_id"], row["clock_id"])
                    if clock not in spans:
                        spans[clock] = [rx, rx]
                    else:
                        spans[clock][0] = min(spans[clock][0], rx); spans[clock][1] = max(spans[clock][1], rx)
                    # Clock changes cannot manufacture a new sequence epoch.
                    sequence_key = key[:3]
                    if sequence_key not in sequences:
                        sequences[sequence_key] = {"last": seq, "seen": {seq}, "order": deque([seq])}
                    else:
                        state = sequences[sequence_key]
                        delta = (seq - state["last"]) & 0xFFFFFFFF
                        if delta == 0 or seq in state["seen"]:
                            result["duplicates"] += 1
                        elif delta == 0x80000000:
                            result["ambiguous_rows"] += 1
                            if len(result["ambiguities"]) < 20:
                                result["ambiguities"].append({"line": line, "reason": "half-range-sequence-ambiguity"})
                        elif delta < 0x80000000:
                            result["observed_forward_gaps"] += delta - 1
                            result["sequence_wraps"] += int(seq < state["last"])
                            state["last"] = seq
                        else:
                            result["late_or_stale"] += 1
                        if seq not in state["seen"]:
                            state["seen"].add(seq); state["order"].append(seq)
                            if len(state["order"]) > 1024:
                                state["seen"].remove(state["order"].popleft())
                result["accepted_rows"] += 1
            except (ValueError, TypeError):
                result["rejected_rows"] += 1
                if len(result["errors"]) < 20:
                    result["errors"].append({"line": line, "reason": "invalid-schema-field-or-clock"})
    result["sequence_epochs"] = len(sequences)
    result["receiver_interarrival"] = stats(intervals)
    result["rtt"] = stats(rtts)
    result["receiver_clock_spans"] = [{"session_id": key[0], "clock_id": key[1],
                                      "span_ms": times[1] - times[0]} for key, times in spans.items()]
    result["limits"] = "Forward gaps are observations, not loss. No initial/tail gap estimate. Duplicate window: 1024 sequences/epoch; older repeats are late/stale. RTT records declare one local clock; synchronization is not verified."
    if result["rejected_rows"]:
        result["status"] = "invalid-input"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    args = parser.parse_args()
    try:
        result = analyze(args.trace)
    except (OSError, UnicodeError, csv.Error, ValueError):
        print(json.dumps({"status": "invalid-input", "reason": "unsupported-unreadable-or-oversized-trace"}))
        return 2
    print(json.dumps(result, indent=2))
    return 2 if result["status"] == "invalid-input" else 0


if __name__ == "__main__":
    raise SystemExit(main())
