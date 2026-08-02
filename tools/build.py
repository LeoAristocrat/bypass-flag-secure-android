#!/usr/bin/env python3
"""Create deterministic manager packages and a source archive."""

from __future__ import annotations

import hashlib
import shutil
import stat
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
COMMON = ROOT / "packaging" / "common"
VERSION = "0.1.0"
ZIP_TIMESTAMP = (2026, 8, 2, 0, 0, 0)
MANAGERS = ("magisk", "kernelsu")
EXECUTABLE_NAMES = {
    "action.sh",
    "customize.sh",
    "service.sh",
    "uninstall.sh",
    "build.sh",
    "build.py",
    "validate.py",
}
SOURCE_EXCLUDES = {".git", ".idea", ".vscode", "__pycache__", "build", "dist"}


def zip_info(name: str, executable: bool) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, ZIP_TIMESTAMP)
    info.create_system = 3
    mode = 0o755 if executable else 0o644
    info.external_attr = (stat.S_IFREG | mode) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    return info


def write_zip(path: Path, files: list[tuple[str, Path]]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for archive_name, source in sorted(files, key=lambda item: item[0]):
            executable = source.name in EXECUTABLE_NAMES or source.suffix == ".sh"
            archive.writestr(zip_info(archive_name, executable), source.read_bytes())


def module_files(manager: str) -> list[tuple[str, Path]]:
    files: dict[str, Path] = {}
    for source in COMMON.rglob("*"):
        if source.is_file():
            files[source.relative_to(COMMON).as_posix()] = source

    overlay = ROOT / "packaging" / manager
    for source in overlay.rglob("*"):
        if source.is_file():
            files[source.relative_to(overlay).as_posix()] = source

    return list(files.items())


def source_files() -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    for source in ROOT.rglob("*"):
        relative = source.relative_to(ROOT)
        if source.is_dir() or any(part in SOURCE_EXCLUDES for part in relative.parts):
            continue
        files.append((f"bypass-flag-secure-android-{VERSION}/{relative.as_posix()}", source))
    return files


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reset_dist() -> None:
    resolved_root = ROOT.resolve()
    resolved_dist = DIST.resolve()
    if resolved_dist.parent != resolved_root or resolved_dist.name != "dist":
        raise RuntimeError(f"refusing to replace unexpected output directory: {resolved_dist}")
    if resolved_dist.exists():
        shutil.rmtree(resolved_dist)
    resolved_dist.mkdir(parents=True)


def build() -> list[Path]:
    reset_dist()

    artifacts: list[Path] = []
    for manager in MANAGERS:
        path = DIST / f"bypass-flag-secure-android-{manager}-v{VERSION}.zip"
        write_zip(path, module_files(manager))
        artifacts.append(path)

    source_path = DIST / f"bypass-flag-secure-android-source-v{VERSION}.zip"
    write_zip(source_path, source_files())
    artifacts.append(source_path)

    checksum_path = DIST / "SHA256SUMS"
    checksum_path.write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in artifacts),
        encoding="utf-8",
        newline="\n",
    )
    artifacts.append(checksum_path)
    return artifacts


if __name__ == "__main__":
    for artifact in build():
        print(artifact.relative_to(ROOT).as_posix())
