# Compatibility

## Declared installer range

The `v0.1.0` installer accepts Android API 31 through 37, corresponding to Android 12 through Android 17. This is an installer guard, not yet a claim of physical-device validation.

Supported installer ABI identifiers are `arm`, `arm64`, `x86`, and `x64`. The current no-op milestone contains no ABI-specific binaries.

## Verified environments

No physical-device results have been recorded yet. Do not change a status to passing without installing, rebooting, running the manager action, disabling, re-enabling, and uninstalling on the exact environment.

| Android | Device/OEM | Kernel | Root manager | Manager version | Security patch | Status |
|---|---|---|---|---|---|---|
| 12 | Pending | Pending | Magisk | Pending | Pending | Not tested |
| 12 | Pending | Pending | KernelSU | Pending | Pending | Not tested |
| 13 | Pending | Pending | Magisk | Pending | Pending | Not tested |
| 14 | Pending | Pending | Magisk | Pending | Pending | Not tested |
| 15 | Pending | Pending | Magisk | Pending | Pending | Not tested |
| 16 | Pending | Pending | Magisk | Pending | Pending | Not tested |
| 17 | Pending | Pending | Magisk | Pending | Pending | Not tested |

## Acceptance checklist

- Package installs only in its intended manager.
- Unsupported API and ABI values abort installation.
- Device reaches the lock screen after reboot.
- Action output reports the expected environment.
- Boot marker is created only inside the module directory.
- Disabling the module prevents its boot script from running.
- Re-enabling restores the boot marker behavior.
- Uninstall completes and the device reboots normally.
- No `/system` mount, property, SELinux, or network change occurs.
