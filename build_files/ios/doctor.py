#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Fail-closed environment preflight for Blender's iOS build packets."""

from __future__ import annotations

import argparse
import json
import os
import plistlib
import shutil
import subprocess
import sys
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path


def env_float(name: str, default: float) -> float:
    """Read a float from the environment, failing loudly instead of at first use."""
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        return float(raw)
    except ValueError as error:
        raise SystemExit(f"{name} must be a number, got {raw!r}") from error


BULK_VOLUME = Path(os.environ.get("BLENDER_IOS_BULK_VOLUME", "/Volumes/BlenderBuild"))
BULK_ROOT_NAME = "blender-ios"
# Upstream pins one specific build volume by UUID. This fork defaults to an empty
# value so the doctor can run on any machine; pass --expected-volume-uuid (or set
# BLENDER_IOS_BULK_VOLUME_UUID) to restore the strict single-machine check.
EXPECTED_VOLUME_UUID = os.environ.get("BLENDER_IOS_BULK_VOLUME_UUID", "")
BASELINE_SHA = "fbe6228777e7d9afefcd61a413844e790ae75db7"
DONOR_SHA = "a1de44dd54af75a4c8c4a29a5fed2a1334a87446"
MINIMUM_BULK_FREE_GIB = env_float("BLENDER_IOS_MIN_BULK_FREE_GIB", 100)
MINIMUM_INTERNAL_FREE_GIB = env_float("BLENDER_IOS_MIN_INTERNAL_FREE_GIB", 20)
REQUIRED_TOOLS = ("cmake", "ninja", "xcodebuild", "xcrun", "git", "patch", "make", "perl")


def run(command: Sequence[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)


def add(checks: list[dict[str, object]], name: str, passed: bool, detail: object) -> None:
    checks.append({"name": name, "status": "GREEN" if passed else "RED", "detail": detail})


def free_gib(path: Path) -> float:
    usage = shutil.disk_usage(path)
    return round(usage.free / (1024**3), 1)


def is_writable(path: Path) -> bool:
    try:
        return os.access(path, os.W_OK)
    except OSError:
        return False


def volume_uuid(volume: Path) -> str:
    info = subprocess.run(
        ["diskutil", "info", "-plist", str(volume)], capture_output=True, check=False
    )
    if info.returncode != 0:
        return ""
    return str(plistlib.loads(info.stdout).get("VolumeUUID", ""))


def collect(
    repository: Path,
    bulk_volume: Path = BULK_VOLUME,
    expected_volume_uuid: str = EXPECTED_VOLUME_UUID,
    minimum_bulk_free_gib: float = MINIMUM_BULK_FREE_GIB,
    minimum_internal_free_gib: float = MINIMUM_INTERNAL_FREE_GIB,
) -> dict[str, object]:
    bulk_root = bulk_volume / BULK_ROOT_NAME
    checks: list[dict[str, object]] = []
    mounted = os.path.ismount(bulk_volume)
    add(checks, "bulk-volume-mounted", mounted, str(bulk_volume))

    actual_uuid = volume_uuid(bulk_volume) if mounted else ""
    if expected_volume_uuid:
        add(checks, "bulk-volume-uuid", actual_uuid == expected_volume_uuid, actual_uuid)
    else:
        add(
            checks,
            "bulk-volume-uuid",
            True,
            f"{actual_uuid or 'unknown'} (not enforced; pass --expected-volume-uuid to pin)",
        )
    writable = mounted and is_writable(bulk_volume)
    add(checks, "bulk-volume-writable", writable, str(bulk_volume))
    if mounted:
        available = free_gib(bulk_volume)
        add(
            checks,
            "bulk-free-space",
            available >= minimum_bulk_free_gib,
            f"{available} GiB (need {minimum_bulk_free_gib})",
        )

    internal_available = free_gib(repository)
    add(
        checks,
        "internal-free-space",
        internal_available >= minimum_internal_free_gib,
        f"{internal_available} GiB (need {minimum_internal_free_gib})",
    )

    for tool in REQUIRED_TOOLS:
        location = shutil.which(tool)
        add(checks, f"tool-{tool}", location is not None, location or "missing")

    sdk = run(["xcrun", "--sdk", "iphonesimulator", "--show-sdk-path"])
    sdk_path = sdk.stdout.strip()
    add(checks, "simulator-sdk", sdk.returncode == 0 and Path(sdk_path).exists(), sdk_path)

    result = run(["git", "rev-parse", "v5.2.0"], repository)
    actual = result.stdout.strip()
    add(checks, "git-v5.2.0", result.returncode == 0 and actual == BASELINE_SHA, actual)

    # The donor is an immutable object, not the current tip of a remote branch.
    # A fetch may legitimately advance origin/ios without changing this port's
    # reviewed 213-file input delta.
    donor = run(["git", "cat-file", "-e", f"{DONOR_SHA}^{{commit}}"], repository)
    add(checks, "git-donor-object", donor.returncode == 0, DONOR_SHA)

    power = run(["pmset", "-g", "batt"])
    power_detail = power.stdout.strip()
    add(checks, "ac-power", "AC Power" in power_detail, power_detail)

    status = "GREEN" if all(item["status"] == "GREEN" for item in checks) else "RED"
    return {
        "schema_version": 1,
        "packet": "N000",
        "status": status,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "repository": str(repository),
        "bulk_root": str(bulk_root),
        "checks": checks,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--bulk-volume",
        type=Path,
        default=BULK_VOLUME,
        help="Dedicated bulk build volume (default: %(default)s).",
    )
    parser.add_argument(
        "--expected-volume-uuid",
        default=EXPECTED_VOLUME_UUID,
        help="Pin the bulk volume by UUID. Empty (the default) skips the check.",
    )
    parser.add_argument(
        "--minimum-bulk-free-gib",
        type=float,
        default=MINIMUM_BULK_FREE_GIB,
        help="Required free space on the bulk volume (default: %(default)s).",
    )
    parser.add_argument(
        "--minimum-internal-free-gib",
        type=float,
        default=MINIMUM_INTERNAL_FREE_GIB,
        help="Required free space on the internal disk (default: %(default)s).",
    )
    arguments = parser.parse_args(sys.argv[1:] if argv is None else argv)
    report = collect(
        arguments.repository.resolve(),
        bulk_volume=arguments.bulk_volume,
        expected_volume_uuid=arguments.expected_volume_uuid,
        minimum_bulk_free_gib=arguments.minimum_bulk_free_gib,
        minimum_internal_free_gib=arguments.minimum_internal_free_gib,
    )
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "output": str(arguments.output)}, indent=2))
    return 0 if report["status"] == "GREEN" else 1


if __name__ == "__main__":
    sys.exit(main())
