#!/bin/bash
# Stage 05: probes of the UNMODIFIED instructor snapshot
# (Section4_Digital_Twin/arduinobot_ws at commit 4936385), used to decide which
# corrections were needed. WS must point at a workspace built from that snapshot.
source "$(dirname "$0")/common.sh"
cd "$WS"
run colcon build --event-handlers console_cohesion-
source install/setup.bash
export ROS_DOMAIN_ID=61
echo; echo "# Python publisher: start-up log and Ctrl+C behaviour"
P=$(start_bg "$OUT/05_py_publisher.log" ros2 run arduinobot_py_examples simple_publisher); sleep 3; stop_bg "$P"
cat "$OUT/05_py_publisher.log"
echo; echo "# Python simple_parameter: updates of the node's own and of a standard parameter"
N=$(start_bg "$OUT/05_py_param.log" ros2 run arduinobot_py_examples simple_parameter); sleep 3
run ros2 param set /simple_parameter simple_int_param 30 --no-daemon --spin-time 5
run ros2 param set /simple_parameter use_sim_time true --no-daemon --spin-time 5
run ros2 param get /simple_parameter use_sim_time --no-daemon --spin-time 5
run ros2 service call /simple_parameter/set_parameters_atomically rcl_interfaces/srv/SetParametersAtomically \
  "{parameters: [{name: simple_int_param, value: {type: 2, integer_value: 6}}, {name: use_sim_time, value: {type: 1, bool_value: true}}]}"
run ros2 param get /simple_parameter use_sim_time --no-daemon --spin-time 5
stop_bg "$N"
echo; echo "# C++ simple_parameter"
N=$(start_bg "$OUT/05_cpp_param.log" ros2 run arduinobot_cpp_examples simple_parameter); sleep 3
run ros2 param set /simple_parameter use_sim_time true --no-daemon --spin-time 5
stop_bg "$N"
echo; echo "# stale RViz entries: links named in display.rviz but absent from the URDF"
SHARE=install/arduinobot_description/share/arduinobot_description
xacro $SHARE/urdf/arduinobot.urdf.xacro > "$OUT/05_instructor.urdf"
run bash -c "grep -o '<link name=\"[a-z_]*\"' $OUT/05_instructor.urdf | cut -d'\"' -f2 | sort > /tmp/urdf_links; grep -n 'tool_link' $SHARE/rviz/display.rviz; grep -c tool_link /tmp/urdf_links"
run grep -n -A3 "Description Topic" $SHARE/rviz/display.rviz
echo; echo "# late-joining RViz with the ORIGINAL display.rviz (Description Topic durability 'Volatile')"
if [ -z "$DISPLAY" ]; then export DISPLAY=:78 LIBGL_ALWAYS_SOFTWARE=1; Xvfb :78 -screen 0 1600x1000x24 >/dev/null 2>&1 & sleep 2; fi
export QT_X11_NO_MITSHM=1
RSP=$(start_bg "$OUT/05_late_rsp.log" ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro $SHARE/urdf/arduinobot.urdf.xacro)")
JSP=$(start_bg "$OUT/05_late_jsp.log" ros2 run joint_state_publisher joint_state_publisher)
sleep 8
RV=$(start_bg "$OUT/05_late_rviz.log" rviz2 -d "$SHARE/rviz/display.rviz")
sleep 25
run ros2 topic info -v /robot_description --no-daemon --spin-time 5
WID=$(xdotool search --name "RViz" 2>/dev/null | tail -1)
import -window "${WID:-root}" "$OUT/05_late_join_original_config.png"; echo "screenshot: 05_late_join_original_config.png"
stop_bg "$RV"; stop_bg "$JSP"; stop_bg "$RSP"
