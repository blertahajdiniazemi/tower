# Test environment for the assignment: Ubuntu 22.04 + ROS 2 Humble (osrf/ros:humble-desktop)
# packages.ros.org is not reachable from this build environment, so xacro and
# joint_state_publisher(_gui) are built from their upstream Humble release tags.
FROM osrf/ros:humble-desktop
SHELL ["/bin/bash", "-c"]
RUN rm -f /etc/apt/sources.list.d/ros2*.list /etc/apt/sources.list.d/ros2.sources; \
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      xvfb x11-apps x11-utils imagemagick xdotool mesa-utils libgl1-mesa-dri python3-pytest \
    && rm -rf /var/lib/apt/lists/*
COPY underlay_src /opt/underlay/src
RUN source /opt/ros/humble/setup.bash && cd /opt/underlay && \
    colcon build --merge-install --event-handlers console_direct- 2>&1 | tail -5
