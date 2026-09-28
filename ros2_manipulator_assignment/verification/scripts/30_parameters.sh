#!/bin/bash
# Stage 30: parameters of the Python (and optionally C++) simple_parameter node
source "$(dirname "$0")/common.sh"
check_node() {  # package domain_id
  local pkg=$1; export ROS_DOMAIN_ID=$2
  echo; echo "================ $pkg/simple_parameter (ROS_DOMAIN_ID=$ROS_DOMAIN_ID)"
  local N; N=$(start_bg "$OUT/30_${pkg}_node.log" ros2 run "$pkg" simple_parameter); sleep 3
  run ros2 param list /simple_parameter --no-daemon --spin-time 5
  run ros2 param describe /simple_parameter simple_int_param simple_string_param --no-daemon --spin-time 5
  run ros2 param get /simple_parameter simple_int_param --no-daemon --spin-time 5
  run ros2 param get /simple_parameter simple_string_param --no-daemon --spin-time 5
  run ros2 param set /simple_parameter simple_int_param 30 --no-daemon --spin-time 5
  run ros2 param set /simple_parameter simple_string_param "ROS 2" --no-daemon --spin-time 5
  run ros2 param set /simple_parameter simple_int_param hello --no-daemon --spin-time 5
  run ros2 param set /simple_parameter use_sim_time true --no-daemon --spin-time 5
  echo; echo "# atomic update: valid simple_int_param=5 together with an INTEGER for simple_string_param"
  run ros2 service call /simple_parameter/set_parameters_atomically rcl_interfaces/srv/SetParametersAtomically \
    "{parameters: [{name: simple_int_param, value: {type: 2, integer_value: 5}}, {name: simple_string_param, value: {type: 2, integer_value: 7}}]}"
  run ros2 param get /simple_parameter simple_int_param --no-daemon --spin-time 5
  run ros2 param get /simple_parameter simple_string_param --no-daemon --spin-time 5
  run ros2 param dump /simple_parameter --no-daemon --spin-time 5
  stop_bg "$N"
  echo "--- node log"; cat "$OUT/30_${pkg}_node.log"
  echo; echo "# start-up override from the command line"
  N=$(start_bg "$OUT/30_${pkg}_override.log" ros2 run "$pkg" simple_parameter --ros-args -p simple_int_param:=42); sleep 3
  run ros2 param get /simple_parameter simple_int_param --no-daemon --spin-time 5
  stop_bg "$N"
}
check_node arduinobot_py_examples 31
check_node arduinobot_cpp_examples 32
