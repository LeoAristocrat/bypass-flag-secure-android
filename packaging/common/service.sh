#!/system/bin/sh

MODDIR=${0%/*}
STATE_DIR="$MODDIR/state"
STATE_TMP="$STATE_DIR/last_boot.txt.tmp"
STATE_FILE="$STATE_DIR/last_boot.txt"

mkdir -p "$STATE_DIR" || exit 0

{
  printf 'observed_at_utc=%s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  printf 'android_release=%s\n' "$(getprop ro.build.version.release)"
  printf 'android_api=%s\n' "$(getprop ro.build.version.sdk)"
  printf 'device_abi=%s\n' "$(getprop ro.product.cpu.abi)"
  if [ "${KSU:-false}" = "true" ]; then
    printf 'manager=kernelsu\n'
  else
    printf 'manager=magisk\n'
  fi
} > "$STATE_TMP"

chmod 0600 "$STATE_TMP"
mv -f "$STATE_TMP" "$STATE_FILE"
