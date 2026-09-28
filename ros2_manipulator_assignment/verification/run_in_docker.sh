#!/bin/bash
# Run all verification stages inside the Ubuntu 22.04 / ROS 2 Humble test container.
#   ./verification/docker/fetch_underlay.sh
#   docker build --network host -t arduinobot-humble-test verification/docker
#   ./verification/run_in_docker.sh [output_dir]
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
A=$(cd "$HERE/.." && pwd)
OUT=${1:-$HERE/logs/latest}
SCRATCH=${SCRATCH:-/tmp/arduinobot_verify}
IMAGE=${IMAGE:-arduinobot-humble-test}
rm -rf "$SCRATCH/ws" "$OUT"; mkdir -p "$SCRATCH/ws" "$OUT"
cp -r "$A/arduinobot_ws/src" "$SCRATCH/ws/"   # build outside the delivered source tree
for stage in 00_environment 10_build 20_pubsub 30_parameters 40_model_tf 50_rviz 55_display_gui_false; do
  echo "######## $stage"
  docker run --rm --network none -v "$SCRATCH/ws:/ws" -v "$HERE/scripts:/scripts:ro" -v "$OUT:/out" \
    "$IMAGE" bash "/scripts/$stage.sh" > "$OUT/$stage.log" 2>&1 || echo "stage $stage exited with $?"
  tail -3 "$OUT/$stage.log"
done
