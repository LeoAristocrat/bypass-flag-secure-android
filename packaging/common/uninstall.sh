#!/system/bin/sh

MODDIR=${0%/*}

if [ -n "$MODDIR" ] && [ -d "$MODDIR/state" ]; then
  rm -f "$MODDIR/state/last_boot.txt" "$MODDIR/state/last_boot.txt.tmp"
  rmdir "$MODDIR/state" 2>/dev/null || true
fi
