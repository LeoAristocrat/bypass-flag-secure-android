#!/system/bin/sh

MIN_API=31
MAX_API=37

ui_print "*******************************"
ui_print " Bypass Android FLAG_SECURE"
ui_print " Safe packaging milestone 0.1"
ui_print "*******************************"

if [ ! -f "$MODPATH/manager.id" ]; then
  abort "Missing manager.id; package is incomplete"
fi

TARGET_MANAGER="$(tr -d '\r\n[:space:]' < "$MODPATH/manager.id")"
RUNNING_MANAGER="magisk"
if [ "${KSU:-false}" = "true" ]; then
  RUNNING_MANAGER="kernelsu"
fi

if [ "$TARGET_MANAGER" != "$RUNNING_MANAGER" ]; then
  abort "Wrong package: install the $RUNNING_MANAGER release"
fi

case "${API:-}" in
  ''|*[!0-9]*) abort "Unable to determine Android API level" ;;
esac

if [ "$API" -lt "$MIN_API" ] || [ "$API" -gt "$MAX_API" ]; then
  abort "Unsupported Android API $API; supported range is $MIN_API-$MAX_API"
fi

case "${ARCH:-}" in
  arm|arm64|x86|x64) ;;
  *) abort "Unsupported or unknown ABI: ${ARCH:-unset}" ;;
esac

set_perm "$MODPATH/action.sh" 0 0 0755
set_perm "$MODPATH/service.sh" 0 0 0755
set_perm "$MODPATH/uninstall.sh" 0 0 0755
set_perm "$MODPATH/manager.id" 0 0 0644

ui_print "Manager: $RUNNING_MANAGER"
ui_print "Android API: $API"
ui_print "ABI: $ARCH"
ui_print "No system files or application behavior will be modified."
ui_print "Reboot, then use the module Action button for diagnostics."
