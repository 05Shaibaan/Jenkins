#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
name=${1:?Choose a new screenshot filename}
path=${2:?Supply the new Jenkins job/build path}
case "$path" in job/shaibaan05-*) ;; *) echo 'Only 05Shaibaan job URLs are allowed.' >&2; exit 2;; esac
destination="$root/evidence/screenshots/$name"
test ! -e "$destination" || { echo 'Refusing to overwrite a screenshot.' >&2; exit 2; }
profile="$HOME/snap/firefox/common/shaibaan05-lab-profile"
mkdir -p "$profile"
exec firefox --headless --no-remote --profile "$profile" --window-size 1440,1050 \
  --screenshot "$destination" "http://127.0.0.1:8080/$path"
