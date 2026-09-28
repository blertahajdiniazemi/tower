# Source provenance and change record

## 1. Retrieved instructor material (category B)

| Item | Value |
|---|---|
| Repository | <https://github.com/AntoBrandi/Robotics-and-ROS-2-Learn-by-Doing-Manipulators> |
| Retrieval | `git clone` over HTTPS, 2026-09-28 (UTC) |
| Remote refs found | `main` → `4936385347e477c59927382c904883c432c9b33d`; `gz-classic` → `07440a5f771b6fcc6c6f4a0b2ff6d40e4eb6ccb2`; `refs/pull/2/head`; **no tags** |
| Selected revision | branch `main`, commit `4936385347e477c59927382c904883c432c9b33d` ("added motor calibration", author AntoBrandi, 2025-10-06) |
| Selected baseline | `Section4_Digital_Twin/arduinobot_ws/src` (36 files, packages `arduinobot_py_examples`, `arduinobot_cpp_examples`, `arduinobot_description`) |
| Licence | Apache License 2.0 (`LICENSE` at repository root) – copied to `arduinobot_ws/LICENSE` and `third_party_notices/INSTRUCTOR_REPOSITORY_LICENSE` |
| Instructor README | copied unchanged to `third_party_notices/INSTRUCTOR_README_at_4936385.md` |
| Reference clone | kept outside the delivered tree (it is not part of the active workspace) |

No instructor project ZIP, electronics ZIP or standalone STL ZIP was supplied with the
assignment, and none is needed: the repository contains the source, the meshes and the
firmware sketches. No electronics schematics, wiring diagrams, bill of materials or CAD
source files (e.g. STEP/SolidWorks) were found in the repository or in the notes; this is
recorded as a limitation and does not affect the software demonstration.

### 1.1 Why this revision and baseline

* The repository holds **seven cumulative snapshots** of the same workspace
  (`Section3_Introduction_to_ROS_2` … `Section9_Build`), each with packages of the same
  names. Only one snapshot may be placed in an active `src/` directory; otherwise colcon
  finds duplicate package names.
* **Section 4 (Digital Twin)** is the smallest snapshot that contains all three packages
  needed for the assignment scope (publisher/subscriber, parameters, robot description, TF,
  RViz). Section 3 has no parameter nodes and no description package. From Section 5 on,
  the description's Xacro includes `arduinobot_ros2_control.xacro`/`arduinobot_gazebo.xacro`
  and calls `$(find arduinobot_controller)`, so even the RViz display would depend on the
  control package (audit finding, see `INSTRUCTOR_REPOSITORY_AUDIT.md`).
* **`main` rather than `gz-classic`**: `main` contains the instructor's own Humble updates
  of 2024-10-06 (commit `53c1593` "support to ROS 2 humble", `e82de27` "update section 4",
  which adds the missing `rcl_interfaces` dependencies) and uses `ros_gz` (modern Gazebo).
  `gz-classic` uses `gazebo_ros` (Gazebo Classic) and lacks the `rcl_interfaces`
  declarations. The student's notes (1.2, lesson 14) record the installation of
  `ros-humble-ros-gz*`, `ros-humble-ign-ros2-control*`, `ros-humble-ros2-control`,
  `ros-humble-ros2-controllers` and `ros-humble-moveit*`, i.e. the modern-Gazebo stack
  that `main` expects, and no Gazebo Classic packages.
* The Section 4 robot model (`arduinobot.urdf.xacro`) and the 13 STL meshes are byte-identical
  on both branches and in Sections 4–9 (audit), so the choice does not change the robot.

## 2. File-level status of the delivered workspace

| Status | Files |
|---|---|
| Identical to the instructor snapshot (27) | all 13 meshes, `urdf/arduinobot.urdf.xacro` (sha256 `e6b06b5b…`), `arduinobot.pdf`, both `CMakeLists.txt`/`package.xml` of the example packages, `setup.py`, `setup.cfg`, `resource/`, `__init__.py`, instructor tests, C++ publisher and subscriber |
| Modified for the assignment (9) | listed in section 3 |
| Added for the assignment (1) | `arduinobot_py_examples/test/test_simple_parameter.py` |

The complete difference is in `patches/section4_4936385_to_delivered.diff`
(apply to a checkout of the snapshot with `patch -p1` from the `arduinobot_ws` directory).

## 3. Changes made for the assignment (category C)

| # | File | Change | Reason / evidence |
|---|---|---|---|
| C1 | `arduinobot_py_examples/simple_publisher.py` | `create_timer(1.0 / self.frequency_, …)`; log `"%.1f Hz"`; comment | `create_timer()` takes a **period in seconds**; the variable `frequency_` was passed directly. At 1.0 the behaviour is identical, but any other value would invert the rate. `%d` of a float printed "1 Hz". |
| C2 | `simple_publisher.py`, `simple_subscriber.py`, `simple_parameter.py` | `try/except (KeyboardInterrupt, ExternalShutdownException)` around `spin`, `rclpy.try_shutdown()` | The original printed a Python traceback and `ros2run` reported "Process exited with failure 1" on Ctrl+C (`verification/logs/baseline_instructor/05_baseline_instructor.log`). |
| C3 | `simple_subscriber.py` | variable renamed from `simple_publisher` to `simple_subscriber`; removed the no-op statement `self.sub_` | Readability only. |
| C4 | `arduinobot_py_examples/simple_parameter.py` | Callback validates the whole request first (type of `simple_int_param` / `simple_string_param`), returns `successful=False` with a reason on the first violation, accepts parameters it does not manage (e.g. `use_sim_time`), then logs the accepted changes. Names and defaults (28, "Antonio") kept. | Original started from `SetParametersResult()` (`successful=False`) and set `True` only for a recognised parameter, so `ros2 param set /simple_parameter use_sim_time true` failed, while the same change **succeeded** when bundled with a valid parameter in one atomic request (baseline log). |
| C5 | `arduinobot_cpp_examples/src/simple_parameter.cpp` | Same callback logic as C4 | Same defect in the C++ version (baseline log). The C++ parameter example is instructor material; it is not documented as a lesson in the notes. |
| C6 | `arduinobot_py_examples/test/test_simple_parameter.py` (new) | 6 pytest cases: defaults, valid updates, `use_sim_time`, wrong type, atomic batch with one invalid parameter, callback on a mixed batch | Guards the parameter contract that C4 establishes. |
| C7 | Python files of `arduinobot_py_examples` | whitespace, import order, line length, final newline | The package's own `test_flake8` failed with 8 findings on the instructor code; it now passes. |
| C8 | `arduinobot_description/launch/display.launch.py` | new launch argument `gui` (`true` default → `joint_state_publisher_gui`; `false` → `joint_state_publisher`), exactly one joint-state source started | Allows the model/TF pipeline to run without a slider window (headless checks, remote sessions) and avoids two conflicting `/joint_states` publishers. Default behaviour is unchanged. |
| C9 | `arduinobot_description/rviz/display.rviz` | removed 3 entries for `tool_link`; RobotModel *Description Topic* durability `Volatile` → `Transient Local` | `tool_link` does not exist in the URDF (it survives from the older `arduinobot.pdf` diagram). `robot_state_publisher` publishes `/robot_description` as transient local; the setting now states the QoS that RViz 11.2.28 actually used in the test (`ros2 topic info -v` showed a TRANSIENT_LOCAL subscription even with the old value, and a late-started RViz displayed the model in both cases). |
| C10 | `arduinobot_description/package.xml` | added `exec_depend` on `ament_index_python`, `launch`, `launch_ros` (imported directly by the launch files) and `joint_state_publisher` (C8); comment that `ros_gz_sim`/`ros_gz_bridge` serve only the optional Gazebo launch file | Direct dependencies must be declared; previously they arrived only transitively. |
| C11 | `arduinobot_description/CMakeLists.txt` | `set(ament_cmake_copyright_FOUND TRUE)` in the test block, with comment | The files carry no per-file copyright headers; adding headers on the author's behalf would be inappropriate. Same pattern as the `ros2 pkg create` template. |
| C12 | `arduinobot_description/launch/gazebo.launch.py` | formatting only (closing brackets) and removal of the unused variable `ros_distro` | `flake8` findings (E124, W293, F841). The launch logic is unchanged and **was not executed** (see VERIFICATION.md). |

Not changed on purpose:

* **Robot model** – link and joint names, origins, axes, limits, mimic relation, inertials,
  mesh scale `0.01` and all mesh files are exactly as supplied. The mesh-scale observation
  (model ≈ 10× the size implied by millimetre mesh units) is recorded in the audit, not
  "fixed", because no measured dimensions of the physical robot are available.
* Publisher/subscriber topic (`/chatter`), type (`std_msgs/msg/String`), queue depth (10),
  node names, message texts (the C++ text keeps its missing space after the colon) and
  executable names.
* `display.rviz` fixed frame `base_link` (valid: `world → base_link` is an identity fixed joint).
* The C++ package declares `ament_lint_auto`/`ament_lint_common` test dependencies but
  registers no tests; left as supplied.

## 4. Deliberate exclusions

| Excluded | Reason |
|---|---|
| Sections 3, 5–9 of the repository | Separate snapshots with duplicate package names; controllers, MoveIt 2, custom interfaces, task server, Alexa integration and firmware belong to later course material whose completion is not documented in the notes (category D). Summarised in `INSTRUCTOR_REPOSITORY_AUDIT.md`. |
| `images/` course covers | Marketing images, not technical evidence. |
| `build/`, `install/`, `log/` | Generated by colcon; never delivered. |
| The student's original notes | Kept by the student; referenced by file name and locator only. Screenshots reproduced in the report are identified as historical evidence. |

## 5. Tools used for preparation (not part of the delivery)

| Tool | Version / revision | Use |
|---|---|---|
| Docker image `osrf/ros:humble-desktop` | Ubuntu 22.04.5, ROS 2 Humble (rclcpp 16.0.19, rclpy 3.3.21, rviz2 11.2.28, robot_state_publisher 3.0.3) | build and runtime verification |
| `ros/xacro` | tag `2.1.1` (`390772ab…`) | built from source in the test image because `packages.ros.org` was not reachable |
| `ros/joint_state_publisher` | tag `2.4.0` (`bbcac1eb…`), packages `joint_state_publisher`, `joint_state_publisher_gui` | as above |
| `ros2/ros2_documentation` | branch `humble`, commit `35b00f1f3c1ab7c14bf85e35fa895f9f580ea279` | source of the cited docs.ros.org pages (docs.ros.org itself was blocked by the network policy) |
| LibreOffice 24.2 Writer, python-docx, PyMuPDF, tesseract | – | reading and converting the notes; building and rendering the report |
