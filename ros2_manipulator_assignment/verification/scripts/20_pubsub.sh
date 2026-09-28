#!/bin/bash
# Stage 20: cross-language publisher/subscriber on /chatter (std_msgs/msg/String)
source "$(dirname "$0")/common.sh"
scenario() {  # name publisher_pkg subscriber_pkg domain_id
  local name=$1 pub_pkg=$2 sub_pkg=$3; export ROS_DOMAIN_ID=$4
  echo; echo "================ Scenario $name: $pub_pkg/simple_publisher -> $sub_pkg/simple_subscriber (ROS_DOMAIN_ID=$ROS_DOMAIN_ID)"
  local SUB PUB
  SUB=$(start_bg "$OUT/20_${name}_subscriber.log" ros2 run "$sub_pkg" simple_subscriber); sleep 2
  PUB=$(start_bg "$OUT/20_${name}_publisher.log" ros2 run "$pub_pkg" simple_publisher); sleep 4
  run ros2 node list --no-daemon --spin-time 5
  run ros2 topic list -t --no-daemon --spin-time 5
  run ros2 topic info -v /chatter --no-daemon --spin-time 5
  run timeout -s INT 15 ros2 topic echo --once /chatter std_msgs/msg/String
  run timeout -s INT 12 ros2 topic hz /chatter --window 5
  stop_bg "$PUB"; stop_bg "$SUB"
  echo; echo "--- publisher log"; cat "$OUT/20_${name}_publisher.log"
  echo "--- subscriber log"; cat "$OUT/20_${name}_subscriber.log"
  local heard; heard=$(grep -c "I heard: Hello ROS 2 - counter" "$OUT/20_${name}_subscriber.log")
  echo "RESULT $name: subscriber received $heard message(s); tracebacks in logs: $(cat "$OUT"/20_${name}_*.log | grep -c Traceback)"
}
scenario py_to_cpp arduinobot_py_examples arduinobot_cpp_examples 21
scenario cpp_to_py arduinobot_cpp_examples arduinobot_py_examples 22
