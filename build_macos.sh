#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${CAMPUSMATE_PYTHON:-$PROJECT_ROOT/.venv/bin/python}"
ARCH="$(uname -m)"

cd "$PROJECT_ROOT"

if [[ ! -x "$PYTHON_BIN" ]]; then
    PYTHON_BIN="python3"
fi

"$PYTHON_BIN" "$PROJECT_ROOT/scripts/build_icon.py"
/usr/bin/iconutil -c icns \
    "$PROJECT_ROOT/build/CampusMate.iconset" \
    -o "$PROJECT_ROOT/assets/CampusMate.icns"

"$PYTHON_BIN" -m PyInstaller \
    --noconfirm \
    --clean \
    CampusMate.spec

ditto -c -k --sequesterRsrc --keepParent \
    "$PROJECT_ROOT/dist/CampusMate.app" \
    "$PROJECT_ROOT/dist/CampusMate-macOS-${ARCH}.zip"

echo "Created dist/CampusMate-macOS-${ARCH}.zip"
