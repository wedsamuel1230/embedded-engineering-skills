#!/usr/bin/env python3
"""Read-only ESP32-S3 generated sdkconfig check against a declared profile."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def digest(path: Path) -> str:
    if path.stat().st_size > 2_000_000:
        raise ValueError("input-too-large")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(root: Path, name: str) -> Path:
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError("input-outside-project-or-missing")
    return path


def check(root: Path, sdkconfig: Path, expected: dict, environment: str, provenance: dict) -> dict:
    result = {"status": "unresolved", "findings": [],
        "unverified": ["physical-board-identity", "physical-memory-capacity", "runtime-operation"],
        "scope": "ESP-IDF 6.0.1 generated ESP32-S3 configuration; supplied input list is not a certified complete dependency graph."}
    if expected.get("chip") != "esp32s3":
        result["status"] = "not-applicable"
        return result
    required = ("board_identity", "module", "flash_mb", "flash_mode", "psram_mb", "psram_mode")
    if any(expected.get(k) in (None, "", "unknown") for k in required):
        result["findings"] = ["incomplete-declared-physical-profile"]
        return result
    if (any(not isinstance(expected[k], str) or not expected[k].strip() for k in ("board_identity", "module")) or
        type(expected["flash_mb"]) is not int or expected["flash_mb"] not in (2,4,8,16,32,64,128) or
        type(expected["psram_mb"]) is not int or expected["psram_mb"] <= 0 or
        expected["flash_mode"] not in ("qio", "qout", "dio", "dout") or
        expected["psram_mode"] not in ("quad", "octal")):
        result["findings"] = ["unsupported-declared-profile"]
        return result
    if (provenance.get("environment") != environment or provenance.get("framework") != "espidf" or
        provenance.get("framework_version") != "6.0.1" or
        not isinstance(provenance.get("tool_versions"), dict) or not provenance["tool_versions"] or
        any(not isinstance(v, str) or not v for v in provenance["tool_versions"].values())):
        result["findings"] = ["missing-or-wrong-environment-sdk-provenance"]
        return result
    inputs = provenance.get("input_hashes")
    if not isinstance(inputs, dict) or "platformio.ini" not in inputs:
        result["findings"] = ["missing-input-hashes"]
        return result
    try:
        sdkconfig = inside(root, str(sdkconfig))
        if digest(sdkconfig) != provenance.get("sdkconfig_sha256"):
            raise ValueError("stale-sdkconfig")
        for name, sha in inputs.items():
            if digest(inside(root, name)) != sha:
                raise ValueError("changed-build-input")
        text = sdkconfig.read_text(encoding="utf-8")
    except (OSError, UnicodeError, ValueError, TypeError):
        result["findings"] = ["stale-unreadable-or-out-of-project-artifact"]
        return result
    values = {}
    duplicates = set()
    for line in text.splitlines():
        match = re.fullmatch(r"(CONFIG_[A-Z0-9_]+)=(.*)", line)
        disabled = re.fullmatch(r"# (CONFIG_[A-Z0-9_]+) is not set", line)
        if disabled:
            match = re.fullmatch(r"(CONFIG_[A-Z0-9_]+)=(.*)", disabled.group(1) + "=n")
        if match:
            key, value = match.groups()
            if key in values:
                duplicates.add(key)
            values[key] = value.strip('"')
    size_keys = [k for k,v in values.items() if re.fullmatch(r"CONFIG_ESPTOOLPY_FLASHSIZE_\d+MB", k) and v == "y"]
    psram_keys = [k for k in ("CONFIG_SPIRAM_MODE_QUAD", "CONFIG_SPIRAM_MODE_OCT") if values.get(k) == "y"]
    flash_keys = [k for k in ("QIO", "QOUT", "DIO", "DOUT") if values.get("CONFIG_ESPTOOLPY_FLASHMODE_" + k) == "y"]
    relevant = {k for k in values if k.startswith(("CONFIG_ESPTOOLPY_FLASHSIZE_", "CONFIG_ESPTOOLPY_FLASHMODE_", "CONFIG_SPIRAM_MODE_"))}
    relevant.update(("CONFIG_IDF_TARGET", "CONFIG_ESPTOOLPY_FLASHMODE", "CONFIG_SPIRAM"))
    if (duplicates & relevant or len(size_keys) != 1 or
        (values.get("CONFIG_SPIRAM") == "y" and len(psram_keys) != 1) or
        values.get("CONFIG_SPIRAM") not in ("y", "n") or len(flash_keys) > 1 or
        (flash_keys and flash_keys[0].lower() != values.get("CONFIG_ESPTOOLPY_FLASHMODE")) or
        any(k not in values for k in ("CONFIG_IDF_TARGET", "CONFIG_ESPTOOLPY_FLASHMODE", "CONFIG_SPIRAM"))):
        result["findings"] = ["missing-or-conflicting-generated-settings"]
        return result
    if values["CONFIG_IDF_TARGET"] != "esp32s3":
        result["findings"] = ["artifact-target-does-not-match-declared-chip"]
        return result
    actual = {"flash_mb": int(re.search(r"_(\d+)MB$", size_keys[0]).group(1)),
              "flash_mode": values["CONFIG_ESPTOOLPY_FLASHMODE"],
              "psram_mode": ("octal" if psram_keys[0].endswith("OCT") else "quad") if psram_keys else None,
              "psram_enabled": values["CONFIG_SPIRAM"] == "y"}
    result["inspected"] = actual
    result["findings"] = [k + "-mismatch" for k in ("flash_mb", "flash_mode", "psram_mode")
                          if actual[k] is not None and actual[k] != expected[k]]
    if not actual["psram_enabled"]:
        result["findings"].append("psram-disabled")
    result["status"] = "confirmed-mismatch" if result["findings"] else "consistent-with-inspected-evidence"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ("project", "sdkconfig", "expected", "provenance"):
        parser.add_argument("--" + flag, type=Path, required=True)
    parser.add_argument("--environment", required=True)
    args = parser.parse_args()
    try:
        # Read only explicitly selected inputs; never dump their raw contents.
        for path in (args.expected, args.provenance):
            if path.stat().st_size > 2_000_000:
                raise ValueError("input-too-large")
        expected = json.loads(args.expected.read_text())
        provenance = json.loads(args.provenance.read_text())
        result = check(args.project.resolve(), args.sdkconfig, expected, args.environment, provenance)
    except (OSError, ValueError, TypeError, AttributeError):
        result = {"status": "unresolved", "findings": ["invalid-or-missing-input"]}
    print(json.dumps(result, indent=2))
    return {"confirmed-mismatch": 1, "unresolved": 2}.get(result["status"], 0)


if __name__ == "__main__":
    raise SystemExit(main())
