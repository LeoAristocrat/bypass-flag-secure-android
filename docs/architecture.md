# Architecture

## Milestone 0.1

The release contains two manager-specific ZIPs generated from a shared set of BusyBox `ash` scripts. The packages intentionally contain no native library, `/system` overlay, properties, SELinux policy, init injection, or network behavior.

Installation follows this sequence:

1. The root manager extracts the module.
2. `customize.sh` reads the immutable `manager.id` shipped in that release.
3. The installer confirms the running manager, Android API range, and ABI.
4. The manager installs the module under `/data/adb/modules/bypass_flag_secure_android`.
5. On boot, `service.sh` records non-sensitive build metadata inside the module's own `state` directory.
6. `action.sh` prints diagnostics in the root manager.

`skip_mount` is always present, ensuring the module does not request a system overlay.

## Planned native milestone

The eventual native component is designed around the following non-negotiable checks:

1. Exact process/package match.
2. Application is debuggable.
3. Application explicitly opts in through test metadata.
4. Signing-certificate SHA-256 digest matches a compiled research certificate.
5. Unsupported or unverifiable state causes immediate unload without behavioral changes.

Magisk will use its native Zygisk integration. KernelSU packaging will declare an external compatible Zygisk implementation as a prerequisite because KernelSU does not provide Zygisk itself. The core native library can then be identical, while installer and compatibility reporting remain manager-specific.

Global `system_server` injection, wildcard targeting, integrity evasion, root hiding, telemetry, and third-party sensitive-app targeting remain explicitly out of scope.
