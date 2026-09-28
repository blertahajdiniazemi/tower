#!/bin/bash
# Supplementary check: validate every package.xml against the REP 149 format-3 schema.
# (Equivalent to the ament 'xmllint' test, which downloads the schema from download.ros.org;
#  that host was not reachable from the preparation environment, so the schema is taken
#  from the ros-infrastructure/rep repository at a fixed commit.)
set -e
SRC=${1:-$(dirname "$0")/../../arduinobot_ws/src}
REP=11ca24a41f31480dfb9562ba99f2a5b93d3ebda5
TMP=$(mktemp -d)
for f in package_format3.xsd package_common.xsd; do
  curl -sSf -o "$TMP/$f" "https://raw.githubusercontent.com/ros-infrastructure/rep/$REP/xsd/$f"
done
echo "schema: ros-infrastructure/rep@$REP xsd/package_format3.xsd"
for p in "$SRC"/*/package.xml; do echo "\$ xmllint --noout --schema package_format3.xsd $(basename "$(dirname "$p")")/package.xml"; xmllint --noout --schema "$TMP/package_format3.xsd" "$p"; done
rm -rf "$TMP"
