#!/bin/bash
# Stage 00: identify the execution environment
source "$(dirname "$0")/common.sh"
run cat /etc/os-release
run uname -srm
echo; echo "ROS_DISTRO=$ROS_DISTRO  ROS_VERSION=$ROS_VERSION  RMW_IMPLEMENTATION=${RMW_IMPLEMENTATION:-<default>}"
run python3 --version
run g++ --version
run cmake --version
run rosdep --version
run bash -c "dpkg-query -W -f='\${Package} \${Version}\n' python3-colcon-core python3-colcon-ros python3-colcon-cmake python3-colcon-python-setup-py 2>/dev/null || pip3 list 2>/dev/null | grep -i colcon"
run bash -c "dpkg-query -W -f='\${Package} \${Version}\n' ros-humble-rclcpp ros-humble-rclpy ros-humble-robot-state-publisher ros-humble-rviz2 ros-humble-tf2-ros ros-humble-urdf ros-humble-fastrtps ros-humble-rmw-fastrtps-cpp 2>/dev/null"
run bash -c "for p in xacro joint_state_publisher joint_state_publisher_gui; do echo \"\$p \$(ros2 pkg prefix \$p) \$(grep -o '<version>[^<]*' \$(ros2 pkg prefix \$p)/share/\$p/package.xml | cut -c10-)\"; done"
run bash -c "ros2 pkg prefix ros_gz_sim ros_gz_bridge 2>&1 | head -2"
run python3 -c "from rclpy.utilities import get_rmw_implementation_identifier as g; print('default RMW implementation:', g())"
run bash -c "which Xvfb xdotool import 2>/dev/null; echo DISPLAY=\${DISPLAY:-<unset>}"
