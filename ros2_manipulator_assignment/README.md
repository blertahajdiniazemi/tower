# ROS 2 Humble manipulator project – arduinobot (assignment preparation)

This directory contains a clean ROS 2 Humble workspace for the 3-DOF manipulator with
gripper ("arduinobot") from the course *Robotics and ROS 2 – Learn by Doing! Manipulators*,
together with the evidence, verification and report material prepared for the assignment
report *Robot Operating System 2: Architecture, Communication and Application in a
Manipulator Robot*.

The workspace is the instructor's **Section 4 (Digital Twin)** snapshot from
<https://github.com/AntoBrandi/Robotics-and-ROS-2-Learn-by-Doing-Manipulators>,
branch `main`, commit `4936385347e477c59927382c904883c432c9b33d`, with a small number of
documented corrections (see [`docs/PROVENANCE.md`](docs/PROVENANCE.md)).

| Path | Content |
|---|---|
| `arduinobot_ws/src/` | the three ROS 2 packages (the only part you build) |
| `arduinobot_ws/LICENSE` | Apache 2.0 licence of the instructor repository |
| `docs/PROVENANCE.md` | source revision, baseline choice, every change (category C), exclusions |
| `docs/COURSE_PROGRESS_EVIDENCE.md` | what the student's notes establish, with locators (categories A–D) |
| `docs/VERIFICATION.md` | verification table, results, checks still to run on the target machine |
| `docs/INSTRUCTOR_REPOSITORY_AUDIT.md` | sections 3–9 of the instructor repository, stale items, hardware facts |
| `verification/` | scripts, Docker test image, logs and screenshots of the verification runs |
| `patches/` | unified diff from the instructor snapshot to the delivered sources |
| `report/` | the Word report, its PDF rendering, figures (PNG/SVG) and their editable sources |
| `third_party_notices/` | instructor licence and README at the selected commit |
| `dist/` | portable source archive of the workspace |

## Packages

| Package | Build type | Role |
|---|---|---|
| `arduinobot_py_examples` | ament_python | `simple_publisher`, `simple_subscriber`, `simple_parameter` (rclpy) |
| `arduinobot_cpp_examples` | ament_cmake | `simple_publisher`, `simple_subscriber`, `simple_parameter` (rclcpp) |
| `arduinobot_description` | ament_cmake | URDF/Xacro model, STL meshes, `display.launch.py`, RViz configuration, optional `gazebo.launch.py` |

The messaging examples exchange `std_msgs/msg/String` on `/chatter`. They are ROS 2
communication exercises and do **not** move the robot model; the robot model is driven
only by `/joint_states` from `joint_state_publisher(_gui)`.

## 1. Prerequisites (Ubuntu 22.04, ROS 2 Humble)

Install ROS 2 Humble Desktop following the official guide
(<https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html>), then:

```bash
sudo apt update
sudo apt install -y ros-dev-tools ros-humble-xacro \
     ros-humble-joint-state-publisher ros-humble-joint-state-publisher-gui
# only needed for the optional launch/gazebo.launch.py:
sudo apt install -y ros-humble-ros-gz
```

## 2. Build

Copy (or clone) `arduinobot_ws` to your home directory, then in a new terminal:

```bash
source /opt/ros/humble/setup.bash
cd ~/arduinobot_ws
sudo rosdep init   # only once per machine; skip if already initialised
rosdep update
rosdep install --from-paths src --ignore-src -r -y --rosdistro humble
#   without Gazebo: add  --skip-keys "ros_gz_sim ros_gz_bridge"
colcon build --symlink-install
source install/setup.bash
```

`source install/setup.bash` must be repeated in every new terminal that uses the workspace
(the workspace is an *overlay* on the `/opt/ros/humble` *underlay*).

Optional tests (linters of the Python package and description launch files, and the
parameter tests):

```bash
colcon test
colcon test-result --verbose
```

`xmllint` downloads the package.xml schema from `download.ros.org`; without network access
that single test fails for an environmental reason.

## 3. Demonstrations

Each block below uses separate terminals; every terminal first runs
`source /opt/ros/humble/setup.bash && source ~/arduinobot_ws/install/setup.bash`.
Stop programs with `Ctrl+C`.

### 3.1 Python publisher → C++ subscriber

```bash
# terminal 1
ros2 run arduinobot_cpp_examples simple_subscriber
# terminal 2
ros2 run arduinobot_py_examples simple_publisher
# terminal 3 – inspection
ros2 node list
ros2 topic list -t
ros2 topic info -v /chatter
ros2 topic echo /chatter
ros2 topic hz /chatter
```

Expected: the subscriber logs `I heard: Hello ROS 2 - counter: 0`, `… 1`, … once per second.

### 3.2 C++ publisher → Python subscriber

```bash
# terminal 1
ros2 run arduinobot_py_examples simple_subscriber
# terminal 2
ros2 run arduinobot_cpp_examples simple_publisher
```

Expected: `I heard: Hello ROS 2 - counter:0`, … (the C++ publisher's text has no space
after the colon – this is the instructor's original string).

Both publishers are named `/simple_publisher` and both subscribers `/simple_subscriber`.
To run all four nodes at the same time without duplicate node names, rename them at start-up:

```bash
ros2 run arduinobot_py_examples simple_publisher --ros-args -r __node:=py_simple_publisher
ros2 run arduinobot_cpp_examples simple_publisher --ros-args -r __node:=cpp_simple_publisher
```

### 3.3 Parameters

```bash
# terminal 1
ros2 run arduinobot_py_examples simple_parameter
# terminal 2
ros2 param list /simple_parameter
ros2 param describe /simple_parameter simple_int_param simple_string_param
ros2 param get /simple_parameter simple_int_param          # 28
ros2 param set /simple_parameter simple_int_param 30       # accepted, logged by the node
ros2 param set /simple_parameter simple_string_param "ROS 2"
ros2 param set /simple_parameter simple_int_param hello    # rejected: wrong type
ros2 param set /simple_parameter use_sim_time true         # accepted (standard parameter)
ros2 param dump /simple_parameter
```

Start-up override: `ros2 run arduinobot_py_examples simple_parameter --ros-args -p simple_int_param:=42`.
The C++ node `arduinobot_cpp_examples simple_parameter` offers the same parameters
(instructor material, optional).

### 3.4 Robot model, TF and RViz

```bash
ros2 launch arduinobot_description display.launch.py           # sliders (joint_state_publisher_gui)
ros2 launch arduinobot_description display.launch.py gui:=false # no slider window
```

In a second terminal:

```bash
ros2 topic echo --once /joint_states          # joint_1 … joint_5 (joint_5 mirrors joint_4)
ros2 run tf2_ros tf2_echo world claw_support
ros2 run tf2_tools view_frames                # writes frames_<date>.pdf with the TF tree
xacro $(ros2 pkg prefix arduinobot_description)/share/arduinobot_description/urdf/arduinobot.urdf.xacro > /tmp/arduinobot.urdf
check_urdf /tmp/arduinobot.urdf
```

Moving the `joint_1` … `joint_4` sliders moves the model in RViz; `joint_5` (left finger) is
a mimic joint and follows `joint_4` with multiplier −1. When the launch is stopped with
`Ctrl+C`, launch reports `joint_state_publisher_gui … exit code -2`: the upstream GUI
terminates on SIGINT by design; `robot_state_publisher` and `rviz2` finish cleanly.

In a virtual machine without 3D acceleration, RViz may need `export LIBGL_ALWAYS_SOFTWARE=1`.

### 3.5 Optional: Gazebo (not verified in this preparation)

`ros2 launch arduinobot_description gazebo.launch.py` is the instructor's simulation launch
file (ros_gz). It was not executed during the preparation because the Gazebo packages could
not be installed in the preparation environment; see `docs/VERIFICATION.md`.

## 4. Re-running the verification

`verification/run_in_docker.sh` repeats the build, messaging, parameter, model/TF and RViz
checks inside an Ubuntu 22.04 / ROS 2 Humble container and writes logs and screenshots:

```bash
./verification/docker/fetch_underlay.sh
docker build --network host -t arduinobot-humble-test verification/docker
./verification/run_in_docker.sh verification/logs/my_run
```

The stage scripts in `verification/scripts/` can also be run natively after sourcing the
workspace (set `WS` and `OUT`, e.g. `WS=~/arduinobot_ws OUT=/tmp/out bash verification/scripts/20_pubsub.sh`).

## 5. Licence and attribution

The packages, meshes and launch files are the instructor's (Antonio Brandi), distributed
under the Apache License 2.0 (`arduinobot_ws/LICENSE`). The instructor's README acknowledges
the EEZYbotARM and an Arduino Project Hub robotic arm as design sources; their own licences
were not inspected for this assignment. Changes made for the assignment are listed in
`docs/PROVENANCE.md` and in `patches/`.
