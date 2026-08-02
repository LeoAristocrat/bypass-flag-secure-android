$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot

python "$ProjectRoot/tools/build.py"
python "$ProjectRoot/tools/validate.py" "$ProjectRoot/dist/bypass-flag-secure-android-magisk-v0.1.0.zip" "$ProjectRoot/dist/bypass-flag-secure-android-kernelsu-v0.1.0.zip"
python -m unittest discover -s "$ProjectRoot/tests" -v
