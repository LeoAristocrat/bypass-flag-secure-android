# Bypass Android FLAG_SECURE Restrictions

Module-only Android security research project by **Leo Aristocrat**, with separate Magisk and KernelSU packages. The current `v0.1.0` milestone is intentionally a safe no-op: it validates installation, records a harmless boot marker, exposes diagnostics through the manager action, and cleanly uninstalls.

It does **not** modify Android secure-window behavior, hook application processes, hide root, bypass Play Integrity, or target third-party applications.

## Current capabilities

- Separate manager-only ZIPs for Magisk and KernelSU
- Android 12 through Android 17 installer guard
- ABI and root-manager validation
- No `/system` overlay, SELinux policy, networking, or native injection
- Diagnostics through `action.sh`; no Android UI application
- Deterministic ZIP creation with SHA-256 checksums
- Automated manifest, path, line-ending, permission, and content validation
- Documented compatibility and recovery procedures

## Build

Python 3.10 or newer is the only build dependency.

```shell
python tools/build.py
python tools/validate.py dist/*.zip
python -m unittest discover -s tests -v
```

On Windows, `scripts/build.ps1` runs the same build and validation flow. On Linux or macOS, use `scripts/build.sh`.

Artifacts are written to `dist/`:

- `bypass-flag-secure-android-magisk-v0.1.0.zip`
- `bypass-flag-secure-android-kernelsu-v0.1.0.zip`
- `bypass-flag-secure-android-source-v0.1.0.zip`
- `SHA256SUMS`

## Installation

Install the ZIP matching the active root manager. These packages are designed for installation inside Magisk Manager or KernelSU Manager; recovery installation is not supported.

After reboot, open the module in the manager and use its **Action** button to print the module status, Android release, API level, ABI, and last observed boot time.

## Project direction

The next milestone adds a native Zygisk skeleton that remains disabled unless the target package is explicitly authorized by package name, debuggable status, opt-in metadata, and signing-certificate hash. A minimal test fixture may live under `tests/fixtures`, but no controller or launcher app is part of the product.

See [Architecture](docs/architecture.md), [Compatibility](docs/compatibility.md), [Recovery](docs/recovery.md), and [Security](SECURITY.md).

## Upstream documentation

- [Magisk developer guides](https://topjohnwu.github.io/Magisk/guides.html)
- [KernelSU module guide](https://kernelsu.org/guide/module.html)
- [Android `FLAG_SECURE`](https://developer.android.com/reference/android/view/WindowManager.LayoutParams#FLAG_SECURE)

## License

Apache-2.0. See [LICENSE](LICENSE).
