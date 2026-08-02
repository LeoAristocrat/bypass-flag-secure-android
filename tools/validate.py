#!/usr/bin/env python3
"""Validate Bypass Android FLAG_SECURE Restrictions release packages."""

from __future__ import annotations

import argparse
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath


REQUIRED_ENTRIES = {
    "action.sh",
    "customize.sh",
    "manager.id",
    "module.prop",
    "service.sh",
    "skip_mount",
    "uninstall.sh",
}
SCRIPT_ENTRIES = {"action.sh", "customize.sh", "service.sh", "uninstall.sh"}
REQUIRED_PROPERTIES = {"id", "name", "version", "versionCode", "author", "description"}
MODULE_ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9._-]+$")
EXPECTED_MANAGER_BY_TOKEN = {"magisk": "magisk", "kernelsu": "kernelsu"}


class ValidationError(ValueError):
    """Raised when a package violates a release invariant."""


def parse_properties(data: bytes) -> dict[str, str]:
    properties: dict[str, str] = {}
    for line_number, line in enumerate(data.decode("utf-8").splitlines(), start=1):
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValidationError(f"module.prop line {line_number} has no '='")
        key, value = line.split("=", 1)
        if not key or not value:
            raise ValidationError(f"module.prop line {line_number} has an empty key or value")
        if key in properties:
            raise ValidationError(f"module.prop contains duplicate key {key!r}")
        properties[key] = value
    return properties


def expected_manager(path: Path) -> str:
    matches = [manager for token, manager in EXPECTED_MANAGER_BY_TOKEN.items() if token in path.name.lower()]
    if len(matches) != 1:
        raise ValidationError("package filename must identify exactly one target manager")
    return matches[0]


def validate_package(path: Path) -> None:
    if not path.is_file():
        raise ValidationError(f"package not found: {path}")

    manager = expected_manager(path)
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]

        if len(names) != len(set(names)):
            raise ValidationError("archive contains duplicate entries")
        if set(names) != REQUIRED_ENTRIES:
            missing = sorted(REQUIRED_ENTRIES - set(names))
            extra = sorted(set(names) - REQUIRED_ENTRIES)
            raise ValidationError(f"unexpected archive contents; missing={missing}, extra={extra}")

        for info in infos:
            name = info.filename
            pure = PurePosixPath(name)
            if "\\" in name or pure.is_absolute() or ".." in pure.parts:
                raise ValidationError(f"unsafe archive path: {name!r}")

            data = archive.read(info)
            if b"\r" in data:
                raise ValidationError(f"CR byte found in LF-only package entry {name!r}")

            if name in SCRIPT_ENTRIES:
                if not data.startswith(b"#!/system/bin/sh\n"):
                    raise ValidationError(f"{name} has an invalid Android shell shebang")
                mode = (info.external_attr >> 16) & 0o777
                if mode & stat.S_IXUSR == 0:
                    raise ValidationError(f"{name} is not executable in the ZIP metadata")

        manager_value = archive.read("manager.id").decode("ascii").strip()
        if manager_value != manager:
            raise ValidationError(f"manager.id is {manager_value!r}; expected {manager!r}")

        properties = parse_properties(archive.read("module.prop"))
        missing_properties = REQUIRED_PROPERTIES - properties.keys()
        if missing_properties:
            raise ValidationError(f"module.prop missing keys: {sorted(missing_properties)}")
        if not MODULE_ID_PATTERN.fullmatch(properties["id"]):
            raise ValidationError("module id does not satisfy manager requirements")
        if not properties["versionCode"].isdigit():
            raise ValidationError("versionCode must be a non-negative integer")
        if properties["id"] != "bypass_flag_secure_android":
            raise ValidationError("published module id must remain stable")

        forbidden = (b"sepolicy.rule", b"system.prop", b"zygisk/")
        joined_names = "\n".join(names).encode("utf-8")
        if any(token in joined_names for token in forbidden):
            raise ValidationError("safe packaging milestone contains forbidden behavior files")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packages", nargs="+", type=Path)
    args = parser.parse_args(argv)

    failed = False
    for package in args.packages:
        try:
            validate_package(package)
        except (OSError, UnicodeError, zipfile.BadZipFile, ValidationError) as error:
            failed = True
            print(f"FAIL {package}: {error}", file=sys.stderr)
        else:
            print(f"PASS {package}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
