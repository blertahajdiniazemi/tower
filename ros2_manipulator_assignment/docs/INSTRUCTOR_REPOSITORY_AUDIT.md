# Audit of the instructor repository (category B material)

Repository <https://github.com/AntoBrandi/Robotics-and-ROS-2-Learn-by-Doing-Manipulators>,
branch `main` at `4936385347e477c59927382c904883c432c9b33d`, compared with branch
`gz-classic` at `07440a5f771b6fcc6c6f4a0b2ff6d40e4eb6ccb2`. Retrieved 2026-09-28.

Method: files were read directly (not only the README); XML/YAML were parsed, Xacro files
expanded, STL meshes parsed, and Python files syntax-checked. The Section 4 packages were
additionally **built and run** in an Ubuntu 22.04 / ROS 2 Humble container (see
`VERIFICATION.md`). Everything in Sections 5–9 was inspected **statically only**: nothing
from those sections was built or run, no Gazebo was started and no hardware was touched.
Paths below are relative to the repository root. "Analysis" marks conclusions drawn from
file contents rather than from a measurement.

## 1. Repository layout

The repository holds seven **cumulative snapshots** of one colcon workspace,
`SectionN_*/arduinobot_ws/src`. Package names repeat in every section, so only one snapshot
can be built at a time.

| Section directory | Packages (new ones in bold) | Content added |
|---|---|---|
| `Section3_Introduction_to_ROS_2` | **arduinobot_py_examples**, **arduinobot_cpp_examples** | publisher and subscriber (Python/C++) |
| `Section4_Digital_Twin` | + **arduinobot_description** | parameter nodes (Py/C++); URDF/Xacro, 13 STL meshes, `display.launch.py`, `gazebo.launch.py` (ros_gz), `display.rviz`, `arduinobot.pdf` |
| `Section5_Control` | + **arduinobot_controller** | ros2_control configuration (`arduinobot_controllers.yaml`, update rate 10 Hz; `arm_controller` = JointTrajectoryController on joint_1–3, `gripper_controller` = JointTrajectoryController on joint_4, `joint_state_broadcaster`), slider bridge node; Xacro gains `arduinobot_gazebo.xacro` and `arduinobot_ros2_control.xacro` |
| `Section6_Kinematics` | + **arduinobot_moveit**, **arduinobot_msgs**, **arduinobot_utils** | MoveIt 2 configuration (SRDF groups `arm`, `gripper`; KDL solver, position-only IK), services `AddTwoInts`, `EulerToQuaternion`, `QuaternionToEuler`; service examples |
| `Section7_Application` | + **arduinobot_remote** | `ArduinobotTask` action server (`task_server`), action/MoveIt examples |
| `Section8_Alexa_Integration` | + **arduinobot_bringup** | Alexa/Flask webhook `alexa_interface.py`, `simulated_robot.launch.py` |
| `Section9_Build` | + **arduinobot_firmware** | Arduino sketches, serial demo nodes, `ArduinobotInterface` ros2_control hardware plugin, `real_robot.launch.py`, C++ lifecycle example |

Sections 5–9 are **future work** relative to the student's documented progress
(`COURSE_PROGRESS_EVIDENCE.md`).

## 2. Branches and Gazebo generations

| Aspect | `main` (selected) | `gz-classic` |
|---|---|---|
| Simulator integration | `ros_gz_sim` (`gz_sim.launch.py`, `create`), `ros_gz_bridge` `/clock` bridge; on Humble the Xacro selects `ign_ros2_control/IgnitionSystem` (Sections 5–9, `is_ignition` derived from `ROS_DISTRO`) | Gazebo Classic: `gazebo_ros` (`gzserver`, `gzclient`, `spawn_entity.py`), `gazebo_ros2_control/GazeboSystem`, `libgazebo_ros2_control.so`, transmissions |
| Section 4 `package.xml` of the examples | declares `rcl_interfaces` | missing `rcl_interfaces` |
| Section 4 robot model and meshes | identical on both branches | identical |
| Resource path set by `gazebo.launch.py` | `GZ_SIM_RESOURCE_PATH` only | `GAZEBO_MODEL_PATH` |

Mixing the two generations is not possible by swapping a single launch action: plugin
names, hardware-interface names, launch files and resource variables all differ.

## 3. Findings relevant to the delivered workspace (Section 4)

| # | Finding | Evidence | Handling |
|---|---|---|---|
| A1 | Python and C++ `simple_parameter` callbacks start from `SetParametersResult()` (`successful = false`) and set `true` only for their own parameters: an update of `use_sim_time` alone is rejected, but accepted inside a batch with a valid parameter (OR semantics). | `Section4_Digital_Twin/.../simple_parameter.py:16-29`, `simple_parameter.cpp:24-42`; runtime: `verification/logs/baseline_instructor/05_baseline_instructor.log` | corrected (C4, C5) |
| A2 | `simple_publisher.py` passes `frequency_ = 1.0` to `create_timer()`, which expects a period in seconds, and logs it with `%d`. | `simple_publisher.py:12-15` | corrected (C1) |
| A3 | Ctrl+C in the Python nodes ends with a traceback (`KeyboardInterrupt`/`ExternalShutdownException`) and `ros2run` reports failure. | baseline log | corrected (C2) |
| A4 | The package's own flake8 test fails (8 findings) in `arduinobot_py_examples`; flake8 fails on the description launch files; the description's copyright linter fails (no headers). | `colcon test` on the untouched snapshot | corrected (C7, C11, C12) |
| A5 | `display.rviz` lists `tool_link` three times; the link was removed from the URDF in May 2023 (commits `718b6d9`, `5fb33f3`). `arduinobot.pdf` (2021) still shows `tool_link` and joint `gripper_right_to_tool`. | `display.rviz:56-57, 74-76, 132-135`; `pdftotext arduinobot.pdf` | RViz entries removed (C9); `arduinobot.pdf` kept unchanged as instructor material but **not used** in the report — the link/joint figure is regenerated from the current model |
| A6 | RobotModel "Description Topic" is configured `Volatile` while `robot_state_publisher` publishes `/robot_description` transient-local. An auditor flagged a possible late-join failure; a second, adversarial check refuted it at source level, and the runtime test showed RViz 11.2.28 subscribing TRANSIENT_LOCAL and displaying the model when started 8 s after the publisher. | `display.rviz:83-89`; `verification/logs/run_2026-09-28/50_rviz.log` | value changed to `Transient Local` for consistency (C9) |
| A7 | Launch files import `ament_index_python`, `launch`, `launch_ros` without declaring them (they arrived transitively via `ros2launch`). | `launch/*.launch.py` imports vs `package.xml` | declared (C10) |
| A8 | `gazebo.launch.py` reads `os.environ["ROS_DISTRO"]` into an unused variable; it starts no joint-state source, so in Gazebo only fixed-joint TF would be published (spawn-only demonstration). | `gazebo.launch.py:30`, `:67-74` | unused line removed (C12); Gazebo launch otherwise unchanged and **not run** |
| A9 | On Humble, `ros_gz` targets Gazebo Fortress. The launch file sets only `GZ_SIM_RESOURCE_PATH`; Fortress historically reads `IGN_GAZEBO_RESOURCE_PATH` (the verifier found that newer Fortress releases, from 6.16.0, also accept the `GZ_` name). Mesh resolution in Gazebo therefore depends on the installed Fortress version. | `gazebo.launch.py:23-28`; no `IGN_GAZEBO_RESOURCE_PATH` in the repository | recorded; to be checked on the target machine if Gazebo is used |
| A10 | `package.xml` of the description depends on `ros_gz_sim`/`ros_gz_bridge` although only the optional Gazebo launch file needs them. | `package.xml` | kept, commented; `rosdep` can skip them with `--skip-keys` |
| A11 | Inertials are placeholders: every link has `ixx = iyy = izz = 1.0` for masses 0.01–1.0 kg; effort 30 and velocity 10 are Xacro properties with no stated physical source. | `arduinobot.urdf.xacro:5-18` | kept; described in the report as supplied model parameters, not measured data |
| A12 | 6 of the 13 STL meshes are never referenced (`link`, `plate`, `round_plate`, `servo_plate`, `triangular_link`, `vertical_drive_arm`). The URDF models the arm as a serial chain; the physical parallelogram linkage parts are not modelled. | mesh references vs `meshes/` | all meshes preserved (instructor assets); limitation stated |

### 3.1 Model scale (analysis)

The STL files carry no unit. Their coordinates are consistent with millimetres (pivot bores
80.0 units apart, bores 3.2–4.2 units across, part numbers `EBA_01.00.0xx` in the headers).
The Xacro scales every mesh by `0.01`, so one file unit becomes 1 cm, and all joint origins
were written for that scale (e.g. `joint_3` z = 0.8 = 80 units × 0.01). The resulting model is
about 1.69 m tall in RViz. The student's notes contain course diagrams giving the same
offsets in centimetres (e.g. 3.07 cm between `base_link` and `base_plate` where the URDF uses
0.307 m; `1.4.docx`, lesson 32, p84–p89). Together this indicates that the software model is
**ten times** the size of the physical parts. The model was **not** rescaled: a correct
rescale would need scale 0.001 *and* every joint and visual origin divided by ten, and no
measured dimensions of a built robot are available. The report quotes model values as model
values.

### 3.2 Other observations (analysis)

* Several joint axes lie 1–3 cm (model scale) away from the corresponding bores in the meshes,
  so parts visibly shift slightly around their pivots when joints move.
* Collision geometry reuses the full-resolution visual meshes (167 532 triangles for the
  seven used meshes) — adequate for visualisation, heavy for physics or planning.

## 4. Later sections (not part of the delivered workspace; static inspection only)

| Topic | Finding (file) |
|---|---|
| Hidden dependency | From Section 5 on, `arduinobot_gazebo.xacro:9,16` calls `$(find arduinobot_controller)`, which `arduinobot_description/package.xml` does not declare (and `arduinobot_controller` depends back on the description). Expanding the model — even for RViz — fails unless the controller package is built. This is why Section 4 was chosen. |
| Controllers | `arduinobot_controllers.yaml`: controller manager 10 Hz; the mimic joint `joint_5` appears in no controller; `slider_control` maps `JointState` positions by index, not by name. |
| MoveIt 2 | `arduinobot_moveit`: groups `arm` (joint_1–3 plus fixed joints) and `gripper` (joint_4, joint_5); KDL with `position_only_ik`; no planning-pipeline YAML (OMPL/CHOMP/Pilz come from `moveit_configs_utils` defaults); several runtime dependencies not declared in `package.xml`. |
| Application | `ArduinobotTask.action` (`int32 task_number` / `bool success` / `int32 percentage`); the C++ task server returns without aborting the goal on failure; the Python task server uses an Iron-style `moveit_py` API and is not Humble-compatible as written. |
| Alexa | `alexa_interface.py` (Flask + ask-sdk) is started unconditionally by the Section 8/9 bringup; its pip dependencies are not declared or documented; no skill interaction model is in the repository; `skill_id` is the placeholder `"SKILL-ID"`. |
| Examples | Section 3 `arduinobot_py_examples/package.xml` declares an unused `arduinobot_msgs` dependency that the Section 3 workspace does not contain. The Python MoveIt example (Sections 7–9) targets Iron or later. |

## 5. Hardware material (Section 9) — facts stated in files only

| Fact | Source (main @ 4936385) |
|---|---|
| Servo pins: base 8, shoulder 9, elbow 10, gripper 11 | `Section9_Build/arduinobot_ws/src/arduinobot_firmware/firmware/robot_control/robot_control.ino:4-7` |
| Start angles base/shoulder/elbow 90°, gripper 0° | same file `:10-13`, written at `:56-59` |
| Serial 115200 baud, 1 ms timeout | same file `:62-63` |
| Frame format `b%03d,s%03d,e%03d,g%03d,` (zero-padded, trailing comma) | `Section9_Build/arduinobot_ws/src/arduinobot_controller/src/arduinobot_interface.cpp:9-20, 166-191` |
| Radian → servo-degree mapping, shoulder inverted | same file `:167-182` |
| Serial port `/dev/ttyACM0` hard-coded in the Xacro | `Section9_Build/arduinobot_ws/src/arduinobot_description/urdf/arduinobot_ros2_control.xacro:31-36` |
| Serial demo nodes default to `/dev/ttyUSB0` | `arduinobot_firmware/src/simple_serial_*.cpp`, `*.py` |
| `motor_calibration.ino` attaches pin 9 and writes 90 | `.../firmware/motor_calibration/motor_calibration.ino:6,10` (main only) |

No repository file names an Arduino board model, a servo model, wiring, supply voltage or
power requirements. The student's notes (`1.1 Course Notes.doc`, lesson 5 "Project
Architecture", *Electronics Architecture*, p7, P0114–P0128) record, as course description,
that an Arduino board controls four servo motors, "typically 4 × SG90 servo motors" or
equivalents; neither source provides electrical ratings, a power arrangement or a wiring
diagram. None of this hardware was used or
actuated during the preparation, and no firmware was compiled or flashed.

## 6. README inconsistencies (main @ 4936385)

| README text | Actual state |
|---|---|
| `cd ~/Robotics-and-ROS-2-Learn-by-Doing-Manipulators/Section9-Build/arduinobot_ws` (line 175) | directory is `Section9_Build` |
| Firmware link `…/blob/humble/Section9_Build/…/robot_control.inol` (line 193) | branch `humble` does not exist; file is `robot_control.ino` |
| Dependency list | no `rosdep` step; omits `tf_transformations`, `python3-transforms3d` and the Alexa SDK packages |

## 7. Licence and attribution

The repository root contains an Apache License 2.0 (`LICENSE`), and the package manifests
state "Apache 2.0". The README acknowledges the EEZYbotARM (Thingiverse thing 1015238) and an
Arduino Project Hub "Arduino 3D-Printed Robotic Arm"; the STL headers carry `EBA_` part
numbers. The licences of those upstream designs were not inspected, so no statement is made
about the meshes beyond the repository's own licence file.
