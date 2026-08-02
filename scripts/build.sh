#!/usr/bin/env sh
set -eu

PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

python3 "$PROJECT_ROOT/tools/build.py"
python3 "$PROJECT_ROOT/tools/validate.py" \
  "$PROJECT_ROOT/dist/bypass-flag-secure-android-magisk-v0.1.0.zip" \
  "$PROJECT_ROOT/dist/bypass-flag-secure-android-kernelsu-v0.1.0.zip"
python3 -m unittest discover -s "$PROJECT_ROOT/tests" -v
