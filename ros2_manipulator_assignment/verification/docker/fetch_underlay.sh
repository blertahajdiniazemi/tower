#!/bin/bash
# Fetch the upstream Humble release sources of xacro and joint_state_publisher
# (used only because packages.ros.org was unreachable from the preparation environment;
#  on a normal Ubuntu 22.04 + Humble machine install ros-humble-xacro and
#  ros-humble-joint-state-publisher-gui with apt instead).
set -e
cd "$(dirname "$0")"
mkdir -p underlay_src && cd underlay_src
[ -d xacro ] || git clone --depth 1 --branch 2.1.1 https://github.com/ros/xacro.git
[ -d joint_state_publisher ] || git clone --depth 1 --branch 2.4.0 https://github.com/ros/joint_state_publisher.git
