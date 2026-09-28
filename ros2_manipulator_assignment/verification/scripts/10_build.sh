#!/bin/bash
# Stage 10: workspace layout, dependency check, build, install layout, tests
source "$(dirname "$0")/common.sh"
cd "$WS"
run colcon list
run colcon graph
UNDERLAY_SRC=""; [ -d /opt/underlay/src ] && UNDERLAY_SRC=/opt/underlay/src
run rosdep check --from-paths src $UNDERLAY_SRC --ignore-src --rosdistro humble
run colcon build --symlink-install --event-handlers console_cohesion+
source install/setup.bash
run ros2 pkg executables arduinobot_py_examples
run ros2 pkg executables arduinobot_cpp_examples
run bash -c "cd install/arduinobot_description/share/arduinobot_description && find launch urdf rviz meshes -type f | sort"
run ros2 launch arduinobot_description display.launch.py --show-args
run colcon test --event-handlers console_cohesion+
run colcon test-result --all --verbose
