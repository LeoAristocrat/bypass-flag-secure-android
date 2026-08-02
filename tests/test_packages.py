from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.build import ROOT, build, sha256
from tools.validate import ValidationError, validate_package


class PackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.artifacts = build()

    def test_manager_packages_validate(self) -> None:
        packages = [path for path in self.artifacts if "magisk" in path.name or "kernelsu" in path.name]
        self.assertEqual(2, len(packages))
        for package in packages:
            with self.subTest(package=package.name):
                validate_package(package)

    def test_build_is_reproducible(self) -> None:
        first = {path.name: path.read_bytes() for path in self.artifacts if path.suffix == ".zip"}
        second_paths = build()
        second = {path.name: path.read_bytes() for path in second_paths if path.suffix == ".zip"}
        self.assertEqual(first, second)

    def test_manager_packages_have_only_expected_root_entries(self) -> None:
        for package in [ROOT / "dist" / "bypass-flag-secure-android-magisk-v0.1.0.zip", ROOT / "dist" / "bypass-flag-secure-android-kernelsu-v0.1.0.zip"]:
            with self.subTest(package=package.name), zipfile.ZipFile(package) as archive:
                self.assertTrue(all("/" not in name for name in archive.namelist()))

    def test_checksum_manifest_matches_release_artifacts(self) -> None:
        checksum_path = ROOT / "dist" / "SHA256SUMS"
        entries = {}
        for line in checksum_path.read_text(encoding="utf-8").splitlines():
            digest, name = line.split("  ", 1)
            entries[name] = digest

        expected_names = {
            "bypass-flag-secure-android-magisk-v0.1.0.zip",
            "bypass-flag-secure-android-kernelsu-v0.1.0.zip",
            "bypass-flag-secure-android-source-v0.1.0.zip",
        }
        self.assertEqual(expected_names, entries.keys())
        for name, digest in entries.items():
            self.assertEqual(digest, sha256(ROOT / "dist" / name))

    def test_tampered_manager_identity_is_rejected(self) -> None:
        source = ROOT / "dist" / "bypass-flag-secure-android-magisk-v0.1.0.zip"
        with tempfile.TemporaryDirectory() as temporary:
            tampered = Path(temporary) / source.name
            with zipfile.ZipFile(source) as original, zipfile.ZipFile(tampered, "w") as output:
                for info in original.infolist():
                    data = b"kernelsu\n" if info.filename == "manager.id" else original.read(info)
                    output.writestr(info, data)
            with self.assertRaises(ValidationError):
                validate_package(tampered)


if __name__ == "__main__":
    unittest.main()
