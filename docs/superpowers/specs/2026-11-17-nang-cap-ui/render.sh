#!/bin/sh
# Chụp ảnh mẫu: ./render.sh <tên không đuôi> [rộng cao]
cd "$(dirname "$0")"
W=${2:-1200}; H=${3:-540}
"/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" --headless=new --disable-gpu --allow-file-access-from-files --hide-scrollbars --force-device-scale-factor=2 --window-size=$W,$H --virtual-time-budget=2000 --user-data-dir="$(cygpath -w "${TEMP:-/tmp}")\mau_ui_edge" --screenshot="$(cygpath -m "$PWD")/$1.png" "file:///$(cygpath -m "$PWD")/$1.html" 2>&1 | grep "written"
