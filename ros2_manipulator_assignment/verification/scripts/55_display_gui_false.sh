#!/bin/bash
# Stage 55: display.launch.py gui:=false (joint_state_publisher instead of the slider GUI)
source "$(dirname "$0")/common.sh"
export ROS_DOMAIN_ID=55 QT_X11_NO_MITSHM=1
if [ -z "$DISPLAY" ]; then export DISPLAY=:78 LIBGL_ALWAYS_SOFTWARE=1; Xvfb :78 -screen 0 1920x1080x24 >/dev/null 2>&1 & sleep 2; fi
echo "================ ros2 launch arduinobot_description display.launch.py gui:=false"
L=$(start_bg "$OUT/55_display_gui_false_launch.log" ros2 launch arduinobot_description display.launch.py gui:=false)
sleep 25
run ros2 node list --no-daemon --spin-time 5
run ros2 topic info -v /joint_states --no-daemon --spin-time 5
run timeout 15 ros2 topic echo --once /joint_states
run bash -c "xdotool search --name '.' getwindowname %@ 2>/dev/null | sort -u | grep -v '^$'"
wid=$(xdotool search --name "RViz" 2>/dev/null | tail -1)
[ -n "$wid" ] && import -window "$wid" "$OUT/55_display_gui_false_rviz.png" && echo "screenshot: 55_display_gui_false_rviz.png"
stop_bg "$L"
echo "--- launch log"; cat "$OUT/55_display_gui_false_launch.log"
