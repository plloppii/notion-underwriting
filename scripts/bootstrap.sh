#!/bin/sh
# Set up or refresh a workspace for one underwriting job. Safe on a fresh machine and on an existing one (idempotent).
#
#   [ -d ~/notion-underwriting ] || git clone https://github.com/plloppii/notion-underwriting ~/notion-underwriting
#   sh ~/notion-underwriting/scripts/bootstrap.sh
#
# Clones or pulls this repository and nyc-zr (the Zoning Resolution CLI) under $UW_HOME (default $HOME), installs the Python
# packages, and prints an environment check. Needs git, Python 3.10 or newer with pip, and network access.
# Env: PYTHON (interpreter, default python3), UW_HOME (where the two repositories live), UW_REPO_BASE (clone from here,
# default https://github.com/plloppii), NOTION_TOKEN (needed only to write to Notion), GOOGLE_MAPS_API_KEY (optional).
set -eu
UW_HOME="${UW_HOME:-$HOME}"
BASE="${UW_REPO_BASE:-https://github.com/plloppii}"
PY="${PYTHON:-python3}"

for repo in notion-underwriting nyc-zr; do
  if [ -d "$UW_HOME/$repo/.git" ]; then
    git -C "$UW_HOME/$repo" pull --ff-only --quiet
  else
    git clone --quiet "$BASE/$repo" "$UW_HOME/$repo"
  fi
done

REQ="$UW_HOME/notion-underwriting/requirements.txt"
pip_install() {
  "$PY" -m pip install --quiet --disable-pip-version-check "$@" 2>/dev/null \
    || "$PY" -m pip install --quiet --disable-pip-version-check --user "$@" 2>/dev/null \
    || "$PY" -m pip install --quiet --disable-pip-version-check --break-system-packages "$@"
}
if ! pip_install -r "$REQ"; then
  echo "bootstrap: the map packages did not install; installing requests only (maps will be skipped)" >&2
  pip_install requests || echo "bootstrap: pip could not install requests either; the screen needs it: $PY -m pip install requests" >&2
fi

"$PY" -c "import requests" 2>/dev/null || { echo "bootstrap: requests is not importable, so screen.py cannot run yet" >&2; exit 1; }
"$PY" "$UW_HOME/notion-underwriting/scripts/screen.py" --check
"$PY" "$UW_HOME/nyc-zr/scripts/zr.py" get 23-22 >/dev/null 2>&1 && echo "zr tool ok" || echo "zr tool failed: run $PY $UW_HOME/nyc-zr/scripts/zr.py get 23-22 to see why" >&2
echo "ready: $PY $UW_HOME/notion-underwriting/scripts/screen.py <address> --borough BK --ask <n> --strategy <Flip|Rent|Build> --listing <url> --notion"
