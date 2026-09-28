#!/bin/bash
# Create a portable source archive of the workspace and its documentation
# (no build/, install/, log/, caches, logs or report).
set -e
cd "$(dirname "$0")"
NAME=arduinobot_ws_source_2026-09-28
mkdir -p dist
tar --sort=name --mtime='2026-09-28 00:00Z' --owner=0 --group=0 --numeric-owner \
    --exclude='__pycache__' --exclude='*.pyc' --exclude='build' --exclude='install' --exclude='log' \
    --transform "s,^,$NAME/," -czf "dist/$NAME.tar.gz" \
    README.md arduinobot_ws docs patches third_party_notices \
    verification/scripts verification/docker/Dockerfile verification/docker/fetch_underlay.sh \
    verification/run_in_docker.sh
sha256sum "dist/$NAME.tar.gz" > "dist/$NAME.tar.gz.sha256"
echo "wrote dist/$NAME.tar.gz"
