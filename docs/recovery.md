# Recovery and removal

Milestone `v0.1.0` does not alter `/system`, SELinux, Android properties, Zygote, or application processes. Its only runtime state is a small text file under its own module directory.

## Normal removal

1. Open the root manager.
2. Disable or remove **Bypass Android FLAG_SECURE Restrictions**.
3. Reboot.
4. Confirm that `/data/adb/modules/bypass_flag_secure_android` is absent after manager cleanup.

## If the manager UI is unavailable

Use the root framework's documented safe-mode or module-removal procedure. Do not delete broad paths under `/data/adb`; target only the exact `bypass_flag_secure_android` module directory or use the framework-provided removal marker.

- [Magisk FAQ and recovery information](https://topjohnwu.github.io/Magisk/faq.html)
- [KernelSU rescue from bootloop](https://kernelsu.org/guide/rescue-from-bootloop.html)

When native behavior is added in a future version, every release must repeat installation, reboot, disable, removal, and recovery validation before it is published.
