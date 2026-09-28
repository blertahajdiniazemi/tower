#!/bin/bash
# Stage 40: robot description processing, model checks, joint states and TF
source "$(dirname "$0")/common.sh"
export ROS_DOMAIN_ID=41
SHARE=$(ros2 pkg prefix arduinobot_description)/share/arduinobot_description
run bash -c "xacro $SHARE/urdf/arduinobot.urdf.xacro > $OUT/arduinobot_expanded.urdf"
run check_urdf "$OUT/arduinobot_expanded.urdf"
run python3 "$(dirname "$0")/check_model.py" "$OUT/arduinobot_expanded.urdf" "$OUT/model_report.json"
run bash -c "cd $OUT && urdf_to_graphviz arduinobot_expanded.urdf arduinobot_urdf_graph"
echo; echo "# robot_state_publisher + joint_state_publisher with fixed example joint values"
RSP=$(start_bg "$OUT/40_rsp.log" ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro $SHARE/urdf/arduinobot.urdf.xacro)")
JSP=$(start_bg "$OUT/40_jsp.log" ros2 run joint_state_publisher joint_state_publisher --ros-args \
      -p zeros.joint_1:=0.5 -p zeros.joint_2:=0.3 -p zeros.joint_3:=-0.4 -p zeros.joint_4:=-0.6)
sleep 4
run ros2 node list --no-daemon --spin-time 5
run ros2 topic info -v /joint_states --no-daemon --spin-time 5
run timeout -s INT 15 ros2 topic echo --once /joint_states sensor_msgs/msg/JointState
run ros2 topic info -v /robot_description --no-daemon --spin-time 5
run timeout -s INT 15 ros2 topic echo --once --qos-durability transient_local --qos-reliability reliable /tf_static tf2_msgs/msg/TFMessage
run timeout -s INT 15 ros2 topic echo --once /tf tf2_msgs/msg/TFMessage
run timeout -s INT 12 ros2 topic hz /joint_states --window 5
run timeout -s INT 4 ros2 run tf2_ros tf2_echo world claw_support
run timeout -s INT 4 ros2 run tf2_ros tf2_echo claw_support gripper_left
run bash -c "cd $OUT && timeout 30 ros2 run tf2_tools view_frames"
stop_bg "$JSP"; stop_bg "$RSP"
echo "--- robot_state_publisher log"; cat "$OUT/40_rsp.log"
echo "--- joint_state_publisher log"; cat "$OUT/40_jsp.log"
