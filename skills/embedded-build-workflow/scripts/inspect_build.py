#!/usr/bin/env python3
"""Offline embedded build intake. Never executes a project or device command."""
from __future__ import annotations

import argparse
import configparser
import hashlib
import json
import os
import re
from pathlib import Path
from urllib.parse import urlsplit

ENV_NAME = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.-]*\Z")
SKIP = {".git", ".pio", ".venv", "venv", "build", "node_modules", "__pycache__"}
MAX_BYTES = 262144


def public_value(value: str) -> str | None:
    if "${" in value or "\n" in value:
        return None
    parsed = urlsplit(value)
    if parsed.scheme and (parsed.username or parsed.password or parsed.query or parsed.fragment):
        return "[redacted-url]"
    return value.strip() or None


def inspect_ini(path: Path, root: Path) -> dict:
    result = {"path": path.parent.relative_to(root).as_posix(), "manager": "platformio",
              "configuration_status": "declared", "environments": [], "issues": [],
              "evidence_stage": "intake-only", "executes_commands": False}
    if path.is_symlink() or path.stat().st_size > MAX_BYTES:
        result.update(configuration_status="unresolved", issues=["symlink-or-oversized-config"])
        return result
    raw = path.read_bytes()
    result["config_sha256"] = hashlib.sha256(raw).hexdigest()
    cfg = configparser.ConfigParser(interpolation=None, strict=True, inline_comment_prefixes=(";",))
    try:
        cfg.read_string(raw.decode("utf-8"))
    except (UnicodeError, configparser.Error):
        result.update(configuration_status="unresolved", issues=["invalid-ini"])
        return result
    extra = cfg.get("platformio", "extra_configs", fallback="")
    common = dict(cfg.items("env")) if cfg.has_section("env") else {}
    if extra:
        result["issues"].append("extra-configs-require-native-resolution")
    for section in cfg.sections():
        if not section.startswith("env:"):
            continue
        name = section[4:]
        if not ENV_NAME.fullmatch(name):
            result["issues"].append("unsafe-or-ambiguous-environment-name")
            continue
        values = common | dict(cfg.items(section))
        unresolved = bool(extra or values.get("extends") or any("${" in v for v in values.values()))
        fields = {k: public_value(values.get(k, "")) for k in ("platform", "framework", "board")}
        if any(v is None or v == "[redacted-url]" for v in fields.values()):
            unresolved = True
        result["environments"].append({"name": name, **fields,
            "resolution": "unresolved" if unresolved else "direct-and-common-values-only",
            "custom_scripts_present": bool(values.get("extra_scripts")),
            "build_requires_trusted_project": True,
            "build_argv": ["platformio", "run", "--project-dir", str(path.parent), "--environment", name]})
        if unresolved:
            result["issues"].append("native-resolution-required")
    if not result["environments"]:
        result["issues"].append("no-safe-explicit-environments")
    if result["issues"]:
        result["configuration_status"] = "unresolved"
        result["resolution_argv"] = ["platformio", "project", "config", "--project-dir", str(path.parent), "--json-output"]
    result["issues"] = sorted(set(result["issues"]))
    return result


def inspect(root: Path) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError("project-directory-required")
    projects = []
    hints = []
    count = 0
    for base, dirs, files in os.walk(root, followlinks=False):
        count += 1
        if count > 2000:
            raise ValueError("directory-limit-exceeded; choose-a-narrower-project")
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not (Path(base) / d).is_symlink())
        directory = Path(base)
        if "platformio.ini" in files:
            projects.append(inspect_ini(directory / "platformio.ini", root))
            if len(projects) > 100:
                raise ValueError("project-limit-exceeded")
        cmake = directory / "CMakeLists.txt"
        if cmake.is_file() and not cmake.is_symlink() and cmake.stat().st_size <= MAX_BYTES:
            text = cmake.read_text(encoding="utf-8", errors="replace")
            for marker, framework in (("IDF_PATH", "espidf"), ("pico_sdk_init", "pico-sdk"),
                                      ("find_package(Zephyr", "zephyr")):
                if marker in text:
                    hints.append({"path": directory.relative_to(root).as_posix(), "framework_hint": framework,
                                  "status": "reference-only-until-toolchain-target-confirmed"})
        if (directory / "py/mpconfig.h").is_file() and (directory / "ports").is_dir():
            hints.append({"path": directory.relative_to(root).as_posix(), "framework_hint": "micropython",
                          "status": "select-port-board-and-build-configuration"})
    return {"schema_version": 1, "projects": projects, "native_hints": hints,
            "evidence_stage": "intake-only", "executes_commands": False,
            "limits": "No inheritance expansion, dependency resolution, tool execution or hardware discovery."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.project), indent=2))
    except (OSError, ValueError):
        print(json.dumps({"status": "unresolved", "reason": "unreadable-or-out-of-bounds-project"}))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
