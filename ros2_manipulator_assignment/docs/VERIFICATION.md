# Verification record (category C)

All checks below were run on **28 Sep 2026** against the delivered sources in
`arduinobot_ws/src`, copied to a scratch workspace so that no `build/`, `install/` or `log/`
directory is created in the delivery. Logs and screenshots are in
`verification/logs/run_2026-09-28/`; probes of the *unmodified* instructor snapshot are in
`verification/logs/baseline_instructor/`. Every stage script is in `verification/scripts/`
and can be re-run with `verification/run_in_docker.sh` or natively after sourcing.

## 1. Execution environment

| Item | Value | Evidence |
|---|---|---|
| Preparation host | cloud container, Ubuntu 24.04.4, Linux 6.18 x86_64, 4 CPUs; **not** the target machine | `uname`, `/etc/os-release` |
| Test environment | Docker image `osrf/ros:humble-desktop` + test layer (`verification/docker/Dockerfile`) | `00_environment.log` |
| OS in container | Ubuntu 22.04.5 LTS (jammy) | `00_environment.log` |
| ROS | ROS 2 Humble: rclcpp 16.0.19, rclpy 3.3.21, rviz2 11.2.28, robot_state_publisher 3.0.3, tf2_ros 0.25.22, urdf 2.6.1, Fast DDS 2.6.12 | `00_environment.log` |
| Default RMW | `rmw_fastrtps_cpp` | `00_environment.log` |
| Toolchain | Python 3.10.12, g++ 11.4.0, CMake 3.22.1, colcon-core 0.21.1, colcon-ros 0.5.0, rosdep 0.26.0 | `00_environment.log` |
| xacro, joint_state_publisher(_gui) | 2.1.1 and 2.4.0, **built from upstream release tags** in `/opt/underlay` because `packages.ros.org` was blocked by the network policy (the student's notes show the same versions installed from apt) | `00_environment.log`, `verification/docker/` |
| Display | Xvfb virtual X server, Mesa software OpenGL ("OpenGl version: 4.5"); no GPU | `50_rviz.log` |
| Network during tests | `--network none` (except fetching the schema in stage 15) | `run_in_docker.sh` |
| Not available | `ros_gz_sim`, `ros_gz_bridge` / Gazebo (blocked repository), physical hardware | `00_environment.log`, `10_build.log` |

## 2. Verification table

Statuses: *Passed by static inspection*, *Passed by build*, *Passed by runtime test*,
*Failed*, *Blocked by environment*, *Not tested*.

| # | Check | Command / method | Files | Result | Evidence | Limitation / next action |
|---|---|---|---|---|---|---|
| V1 | Unique package names, coherent layout | `colcon list`, `colcon graph` | `src/*` | Passed by static inspection – 3 packages, no duplicates, no inter-package dependencies | `10_build.log` | – |
| V2 | package.xml schema (REP 149 format 3) | `xmllint --schema package_format3.xsd` (schema from ros-infrastructure/rep@11ca24a) | 3 × `package.xml` | Passed by static inspection | `15_package_xml_schema.log` | ament's own xmllint test needs download.ros.org (see V6) |
| V3 | Declared vs used dependencies | manual review of imports/includes; `rosdep check --from-paths src /opt/underlay/src --ignore-src` | manifests, launch files | Passed by static inspection; rosdep reports only `ros-humble-ros-gz-sim`, `ros-humble-ros-gz-bridge` missing (optional Gazebo launch) | `10_build.log` | on the target: `rosdep install` or `--skip-keys` |
| V4 | Build | `colcon build --symlink-install` | all | Passed by build – 3 packages finished, no warnings shown | `10_build.log` | – |
| V5 | Executable registration and installed resources | `ros2 pkg executables …`; listing of `share/arduinobot_description` | `setup.py`, `CMakeLists.txt` | Passed by build – 3 Python and 3 C++ executables; `launch/`, `meshes/` (13 STL), `urdf/`, `rviz/` installed | `10_build.log` | – |
| V6 | Package tests | `colcon test`, `colcon test-result --verbose` | tests of both packages | Python package: 9 results, 8 passed (flake8, pep257, 6 parameter tests), 1 skipped by design (copyright template). Description: flake8, lint_cmake, pep257 passed; **xmllint failed – blocked by environment** (schema download). `colcon test-result` prints "18 tests, 2 failures" because the xmllint failure is counted in both the CTest summary and its xunit file | `10_build.log` | re-run with network on the target |
| V7 | Launch arguments | `ros2 launch arduinobot_description display.launch.py --show-args` | `display.launch.py` | Passed by runtime test – `model` (portable default via `get_package_share_directory`) and `gui` (`true`/`false`) | `10_build.log` | – |
| V8 | Python publisher → C++ subscriber | `ros2 run` both; `ros2 node list`, `topic list -t`, `topic info -v`, `topic echo --once`, `topic hz --window 5`; Ctrl+C emulated by SIGINT to the process group | `simple_publisher.py`, `simple_subscriber.cpp` | Passed by runtime test – `/chatter` [std_msgs/msg/String]; 1 publisher + 1 subscription, both RELIABLE/VOLATILE; 33 consecutive messages (counter 0–32) received; measured average rate 1.000 Hz (one window 0.999); no traceback | `20_pubsub.log`, `20_py_to_cpp_*.log` | measured rate ≠ guarantee |
| V9 | C++ publisher → Python subscriber | as V8 | `simple_publisher.cpp`, `simple_subscriber.py` | Passed by runtime test – 33 consecutive messages (0–32); 1.000 Hz; no traceback | `20_pubsub.log`, `20_cpp_to_py_*.log` | – |
| V10 | Python parameter node | `ros2 param list/describe/get/set/dump`; `SetParametersAtomically` service call; start-up override `-p simple_int_param:=42` | `simple_parameter.py` | Passed by runtime test – defaults 28 / "Antonio"; valid updates accepted and logged; `hello` for the integer rejected ("Wrong parameter type…"); `use_sim_time true` accepted; atomic request with one wrong type rejected as a whole, values unchanged; override → 42 | `30_parameters.log`, `30_arduinobot_py_examples_node.log` | – |
| V11 | C++ parameter node (optional) | as V10 | `simple_parameter.cpp` | Passed by runtime test – same contract | `30_parameters.log` | – |
| V12 | Baseline defects of the unmodified snapshot | same probes on Section 4 @ 4936385 | instructor files | Reproduced: Python publisher prints traceback and `ros2run` "exited with failure 1" on Ctrl+C; `use_sim_time` rejected alone but accepted in a batch (Python) and rejected (C++); `tool_link` in RViz config; "Volatile" description QoS | `baseline_instructor/05_baseline_instructor.log` | justification for C1–C5, C9 |
| V13 | Xacro expansion and URDF validity | `xacro …/arduinobot.urdf.xacro`; `check_urdf` | `arduinobot.urdf.xacro` | Passed by static inspection – root `world`, 8 links, tree as expected | `40_model_tf.log`, `arduinobot_expanded.urdf` | – |
| V14 | Topology, joint types, axes, limits, mimic, mesh URIs | `verification/scripts/check_model.py` | expanded URDF, meshes | Passed by static inspection – all checklist joints match; 5 non-fixed joints, 4 independently commanded; `joint_5` mimics `joint_4` (×−1); 14 mesh references resolve with exact case | `40_model_tf.log`, `model_report.json` | – |
| V15 | Joint states and mimic handling | `joint_state_publisher` with fixed values; `ros2 topic echo /joint_states`, `topic hz`, `topic info -v` | – | Passed by runtime test – names `joint_1…joint_5`; `joint_4 = −0.6` → `joint_5 = 0.6`; exactly one publisher; measured 9.99 Hz | `40_model_tf.log` | – |
| V16 | TF | `topic echo /tf_static` (transient local, reliable), `topic echo /tf`, `tf2_echo world claw_support`, `tf2_echo claw_support gripper_left`, `view_frames` | – | Passed by runtime test – fixed joints on `/tf_static`, movable on `/tf` (~10.2 Hz in view_frames); `world→claw_support` = (−0.295, 0.499, 1.339) m, rpy (−0.100, 0.000, 0.500), equal to an independent forward-kinematics calculation | `40_model_tf.log`, `frames_2026-09-28_04.24.17.pdf` | – |
| V17 | `/robot_description` QoS | `ros2 topic info -v /robot_description` | – | Passed by runtime test – publisher TRANSIENT_LOCAL; subscribers (joint_state_publisher, RViz) TRANSIENT_LOCAL | `40_model_tf.log`, `50_rviz.log` | – |
| V18 | RViz display via launch file | `ros2 launch arduinobot_description display.launch.py` under Xvfb; screenshots | launch, rviz | Passed by runtime test – nodes `/joint_state_publisher`, `/robot_state_publisher`, `/rviz2` (+ internal `/transform_listener_impl_…`); one `/joint_states` publisher; Global Status Ok; model and TF drawn | `50_rviz.log`, `50_display_launch_*.png` | software rendering only; on the target use a real display |
| V19 | RViz started after its publisher | RSP + JSP first, `rviz2 -d display.rviz` 8 s later | `display.rviz` | Passed by runtime test – model displayed in the posed configuration | `50_late_join_posed_rviz.png`, `50_rviz.log` | the original "Volatile" setting also worked in RViz 11.2.28 (baseline test), because RViz subscribed TRANSIENT_LOCAL anyway |
| V20 | Clean shutdown | SIGINT to process groups | all nodes | Passed for the delivered nodes (no tracebacks, rclcpp nodes log `signal_handler`); launch reports `robot_state_publisher` and `rviz2` "finished cleanly". Upstream `joint_state_publisher_gui` ends with exit code −2 and upstream `joint_state_publisher` prints an `ExternalShutdownException` traceback – upstream behaviour, not changed | `50_rviz.log`, `40_model_tf.log` | – |
| V21 | Portable paths | `grep` for `/home/`, `/root/`, `/Users/`, `C:\` in all sources | sources | Passed by static inspection – no absolute user paths; resources found through `get_package_share_directory` and `package://` | `21_portable_paths.log` | – |
| V22 | Python syntax / style | flake8 and pep257 via `colcon test` | Python files | Passed by build/test for `arduinobot_py_examples` and the description launch files | `10_build.log` | – |
| V23 | Optional Gazebo launch | – | `gazebo.launch.py` | **Not tested** – `ros_gz_sim` not installable in the preparation environment; static review only (A8, A9 in the audit) | – | run on the target; check mesh resolution with the installed Fortress version |
| V24 | ros2_control, MoveIt 2, application, Alexa, firmware, hardware | – | later sections | **Not tested** (outside scope; no hardware actuated) | – | future work |
| V25 | Portable source archive | extract `dist/arduinobot_ws_source_2026-09-28.tar.gz`, `colcon build --symlink-install` | archive | Passed by build – 3 packages, 6 executables | `60_source_archive_build.log` | – |

## 3. What this verification does not show

* It does not show that the project builds or runs on the student's own Ubuntu 22.04 machine
  with apt-installed packages; the container reproduces that distribution but not that machine.
* RViz ran with software rendering on a virtual display; interactive use of the sliders was not
  performed (joint values were set through parameters of `joint_state_publisher` instead).
* Measured rates are observations of `ros2 topic hz`, not guarantees.
* Historical screenshots from the notes are not re-used as evidence for this verification.

## 4. Checks to run on the target machine

```bash
source /opt/ros/humble/setup.bash
cd ~/arduinobot_ws
rosdep install --from-paths src --ignore-src -r -y --rosdistro humble
colcon build --symlink-install && source install/setup.bash
colcon test && colcon test-result --verbose          # expect all tests to pass with network access
# then the commands of README §3.1–3.4, or natively:
WS=~/arduinobot_ws OUT=/tmp/verify bash <assignment>/verification/scripts/20_pubsub.sh
WS=~/arduinobot_ws OUT=/tmp/verify bash <assignment>/verification/scripts/30_parameters.sh
WS=~/arduinobot_ws OUT=/tmp/verify bash <assignment>/verification/scripts/40_model_tf.sh
WS=~/arduinobot_ws OUT=/tmp/verify bash <assignment>/verification/scripts/50_rviz.sh   # uses $DISPLAY if set
```

Expected results are those of section 2. Additionally: move each slider in
joint_state_publisher_gui and confirm that the left finger mirrors the right one, and,
if Gazebo is to be used, run `ros2 launch arduinobot_description gazebo.launch.py` and check
that the meshes are visible.
