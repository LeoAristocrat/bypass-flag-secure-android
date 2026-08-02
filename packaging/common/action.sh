#!/system/bin/sh

MODDIR=${0%/*}
MANAGER="Magisk"
if [ "${KSU:-false}" = "true" ]; then
  MANAGER="KernelSU"
fi

printf '%s\n' "Bypass Android FLAG_SECURE diagnostics"
printf '%s\n' "-------------------------------------"
printf 'Module version: %s\n' "0.1.0"
printf 'Manager: %s\n' "$MANAGER"
printf 'Android release: %s\n' "$(getprop ro.build.version.release)"
printf 'Android API: %s\n' "$(getprop ro.build.version.sdk)"
printf 'Device ABI: %s\n' "$(getprop ro.product.cpu.abi)"
printf 'Module enabled: %s\n' "$(if [ -f "$MODDIR/disable" ]; then printf 'no'; else printf 'yes'; fi)"
printf 'Native injection present: no\n'
printf 'Secure-window modification present: no\n'

if [ -f "$MODDIR/state/last_boot.txt" ]; then
  printf '%s\n' ""
  printf '%s\n' "Last boot marker:"
  sed 's/^/  /' "$MODDIR/state/last_boot.txt"
else
  printf '%s\n' "Last boot marker: not recorded yet"
fi
