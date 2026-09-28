# Course-progress evidence record (student notes)

This record states what the five supplied note files establish about the student's own
study and practical work in *Robotics and ROS 2 – Learn by Doing! Manipulators*. It is
the basis for every "documented student work" (category A) statement in the report.

**Reading rules applied**

* Conceptual discussion does not establish practical implementation.
* A code listing does not establish that the code was saved, built or run.
* Installing a dependency does not establish completion of a lesson that uses it.
* A course roadmap or contents list does not establish completion.
* Terminal output and screenshots in the notes are **historical** evidence of what happened
  on the student's virtual machine at that time; they are not evidence that the
  reconstructed project of this assignment runs (that is covered by `VERIFICATION.md`).
* Missing evidence is reported as "not documented in the supplied notes", not as proof that
  the student did not study or do something.
* The terminal prompt `blerta@ROS2VM` identifies a VM user name and host name only; it is
  not used as the student's name. Dates quoted below come from the VM clock and are only as
  reliable as that clock. ROS log epoch time stamps are converted to UTC; log folder names and
  the desktop clock show VM local time (UTC+2).

## 1. Inventory of the supplied notes

| Supplied file (upload name) | Actual format (detected) | Size | SHA-256 (first 16) | Working copy | Rendering used for locators | Readability |
|---|---|---|---|---|---|---|
| `1.1 Course Notes.doc` (`bf835656-1.1_Course_Notes.doc`) | Word 97-2003 binary (OLE compound document) | 7.0 MB | `889c4bced719eeb3` | LibreOffice 24.2 → .docx | 13 pages, 229 paragraphs, 7 images | fully legible; text cross-checked with `catdoc` (2 252 vs 2 251 words) |
| `1.2 Course Notes.doc` (`0d9cdeeb-1.2_Course_Notes.doc`) | Word 97-2003 binary | 20.1 MB | `6f1768d5c995fbe1` | LibreOffice → .docx | 266 pages, 10 160 paragraphs, 2 tables, 40 images | legible; the `ros-humble-ros-gz*` install log was deliberately shortened by the student (three "." lines) |
| `1.3 Course Notes.doc` (`12dd52e0-1.3__Course_Notes.doc`) | Word 97-2003 binary | 9.8 MB | `1fdac666a23c96c0` | LibreOffice → .docx | 105 pages, 2 360 paragraphs, 54 images | legible; lesson 26 heading begins with a line break (title recovered from XML and rendering) |
| `1.4.docx` (`aee0311c-1.4.docx`) | Office Open XML (genuine .docx) | 11.6 MB | `d8ac58451eba39e5` | used directly | 89 pages, 1 840 paragraphs, 60 images | legible |
| `1.5.doc` (`2202e8fd-1.5.doc`) | Word 97-2003 binary | 0.4 MB | `b5a69bf0364326cd` | LibreOffice → .docx | 10 pages, 192 paragraphs, 3 images | legible; the code listing has no indentation in the original file (checked with `catdoc` and `antiword`) |

The originals were preserved unchanged; conversions were made on copies (no binary .doc
was renamed to .docx). All 164 embedded images were extracted in document order and
inspected visually; OCR was not needed for any critical value because every screenshot was
legible, and critical identifiers were checked on enlarged crops. Every row of the table
below was re-checked against the notes by an independent pass; image page numbers are the
pages on which the image is rendered. Three illustrations (1.1 IMG005, IMG006; 1.4 IMG056)
carry C2PA metadata identifying them as AI-generated and are not used as technical evidence.

**Locator format:** `file | lesson | pN | Pnnnn / IMGnnn`, where `pN` is the page of the
LibreOffice PDF rendering of the working copy, `Pnnnn` the paragraph number in document
order, and `IMGnnn` the n-th embedded image of that file.

## 2. Lessons present in the notes

| File | Lessons (course numbering as written in the notes) |
|---|---|
| 1.1 | 1 Course Motivation; 4 Get the Most Out of the Course; 5 Project Architecture; 6 Course Presentation |
| 1.2 | 11 Install ROS 2 Humble on Ubuntu 22.04; 14 Configure the Development Environment (lab); 16 Why a Robot Operating System?; 17 What is ROS 2; 18 Why a New Robot Operating System?; 19 ROS 2 Architecture; 20 Hardware Abstraction; 21 Low-Level Device Control; 22 Messaging Between Processes; 23 Package Management; 24 Architecture of a ROS 2 Application |
| 1.3 | 25 Create and Activate a Workspace; 26 Python: Simple Publisher; 27 C++: Simple Publisher |
| 1.4 | 28 Python: Simple Subscriber; 29 C++: Simple Subscriber; 30 Robot Description; 31 URDF; 32 URDF Model |
| 1.5 | 34 RViz 2; 35 Parameters; 36 Parameters (Python) lab (incomplete, see below) |

Not present in any note: lessons 2, 3, 7–10, 12, 13, 15, 33 and everything after 36
(including any C++ parameter lesson). This means only that they are not documented in the
supplied notes.

## 3. Evidence table

Type abbreviations: **C** conceptual discussion, **CL** code listing, **CMD** command listing,
**IO** installation output, **BO** build output, **RO** runtime output (terminal text),
**SS** screenshot, **D** diagram/illustration (course material).

| # | File · lesson | Topic | Locator | Type | What the evidence supports | Limitation | Related project files |
|---|---|---|---|---|---|---|---|
| 1 | 1.1 · 5 | Intended robot: 3-DOF manipulator (base, shoulder, elbow) + gripper; gripper not counted as a DOF | p5–p6, P0079–P0099, IMG003 | C, D | Student recorded the course's robot concept and DOF reasoning | Description of the intended robot, not of a built one | `urdf/arduinobot.urdf.xacro` |
| 2 | 1.1 · 5 | Electronics: Arduino board, 4 servo motors ("typically 4 × SG90") | p7, P0109–P0128, IMG004 | C, D | Course hardware concept | No wiring, ratings, purchase, assembly or firmware upload documented | Section 9 firmware (not in workspace) |
| 3 | 1.1 · 6 | Course roadmap (IMG005: Introduction, Setup, ROS 2, Digital Twin, Control, Kinematics, Application, Alexa, Build, Conclusions); simulation, voice control, physical build and outcomes described in the text | p8–p13, P0141–P0223, IMG005 (renders p9), IMG006–IMG007 | C, D | Awareness of the course plan | Roadmap only; no completion evidence. IMG005 and IMG006 carry C2PA metadata identifying them as AI-generated illustrations | repository `Section3`–`Section9` |
| 4 | 1.2 · 11 | ROS 2 Humble installation on Ubuntu 22.04 "jammy" (locale, sources, `ros-humble-desktop`: 1 018 packages newly installed; `ros-dev-tools`: 70 packages) | p3–p125, P0085–P6474 | CMD, IO | ROS 2 Humble Desktop and dev tools installed on the student's VM without visible errors | Point release appears only in the lesson title ("Ubuntu 22.04.05", P0003/P0070), not in command output; talker/listener check not documented | environment |
| 5 | 1.2 · 11 | `source /opt/ros/humble/setup.bash` appended to `~/.bashrc`; `ros2 --help` works in a new terminal | p126–p130, P6496–P6686, IMG001 (renders p129) | CL, RO, SS | Underlay sourcing configured; ros2 CLI available | Only functional check of the lesson is `ros2 --help`; IMG001 shows only the new, empty terminal tab – the `.bashrc` content and the `ros2 --help` output are pasted text | README §2 |
| 6 | 1.2 · 14 | VS Code + extensions (C/C++, C/C++ Extension Pack with CMake Tools, XML, Robotics Developer Environment), Terminator | p130–p143, IMG002–IMG023 | SS, IO | Development environment prepared | The Python extension is never shown installed (IMG012–IMG013 still show "Install"); XML Tools shown only "Installing" (IMG018) | – |
| 7 | 1.2 · 14 | Installed `ros-humble-joint-state-publisher-gui` 2.4.0, `ros-humble-xacro` 2.1.1 | p143–p145, P6806–P6874 | IO | Packages needed by the description launch were installed | Installation is not use | `arduinobot_description/package.xml` |
| 8 | 1.2 · 14 | Installed `ros-humble-ros-gz*`, `ros2-control`, `ros2-controllers`, `ign-ros2-control*`, `moveit*`, `libserial-dev`, `python3-pip`; pip `pyserial`, `flask`, `flask-ask-sdk`, `ask-sdk` | p145–p208, P6875–P8655 | IO | Dependencies for later course sections were installed (modern-Gazebo stack, matching branch `main`) | **Not evidence of** Gazebo, control, MoveIt, serial or Alexa work; ros-gz log truncated by the student | Sections 5–9 (not in workspace) |
| 9 | 1.2 · 16–20 | Why ROS, what ROS 2 is, ROS 1 limitations, layered architecture (application / rclcpp·rclpy / rcl / rmw / DDS), hardware abstraction | p208–p235, P8658–P9362, IMG024–IMG028 (text layer diagram P9093–P9113, p225) | C, D | Conceptual study of ROS 2 motivation and architecture | Theory only | report §2–§4 |
| 10 | 1.2 · 21–24 | Device drivers; topics, **services and actions**; packages; underlay/overlay | p235–p266, IMG029–IMG040 | C, D | Conceptual study | **Services and actions appear only as theory**; no `.srv`/`.action`, no service/action code or commands | — |
| 11 | 1.3 · 25 | Workspace `~/arduinobot_ws/src`; `colcon build` (0, then 2 packages); `ros2 pkg create` for `arduinobot_py_examples` (ament_python) and `arduinobot_cpp_examples` (ament_cmake); `install/` layout; sourcing; `ros2 pkg list` shows both packages | p1–p24, P0009–P0828 | RO, BO | Workspace and both example packages created and built on the VM | Pasted text only, no screenshots in this lesson; the paste contains editing artefacts (e.g. P0284, P0359–P0367); both packages are corroborated by later screenshots (1.3 IMG005 p30, IMG011 p44) | `arduinobot_ws/`, both example packages |
| 12 | 1.3 · 26 | Python publisher code; `setup.py` entry point `simple_publisher = arduinobot_py_examples.simple_publisher:main`; `package.xml` `rclpy`, `std_msgs` | p28–p40, P0906–P1235, IMG005–IMG009 (render p30–p39) | CL, SS | Code written in the editor; entry point and dependencies added | Editor tabs show unsaved changes in IMG005–IMG009; saving of the code and `setup.py` follows from the later build and run, saving of `package.xml` is not shown; the text listing is unindented, the indented code is in IMG005 | `arduinobot_py_examples/…/simple_publisher.py`, `setup.py`, `package.xml` |
| 13 | 1.3 · 26 | Build, sourcing, `ros2 run arduinobot_py_examples simple_publisher` → "Publishing at 1 Hz"; `ros2 topic list` shows `/chatter` | p43–p58, IMG011–IMG022 (runs dated 2026-02-26 and 2026-04-03) | BO, RO, SS | The Python publisher ran on the VM | — | same |
| 14 | 1.3 · 26 | `ros2 topic echo /chatter` ("Hello ROS 2 - counter: 897" …), `ros2 topic info /chatter [--verbose]` (std_msgs/msg/String, RELIABLE, VOLATILE), `ros2 topic hz /chatter` (average rate 1.000) | p59–p67, IMG023–IMG026 | RO, SS | Topic inspection with the CLI was performed | — | README §3.1 |
| 15 | 1.3 · 27 | C++ publisher code, `CMakeLists.txt` (`add_executable`, `ament_target_dependencies`, `install(TARGETS …)`), `package.xml` `<depend>` rclcpp, std_msgs | p70–p87, P1713–P2093, IMG030–IMG039 (IMG030 renders p71) | CL, SS | C++ node and build rules written | The student's string reads "counter: " (with a space), the instructor's "counter:" | `arduinobot_cpp_examples/…` |
| 16 | 1.3 · 27 | Build (cpp 3.53 s), `ros2 run arduinobot_cpp_examples simple_publisher`, `topic list/echo/info --verbose/hz` (1.000 Hz) | p88–p105, IMG040–IMG054 (runs dated 2026-06-19/20) | BO, RO, SS | The C++ publisher ran and was inspected | — | same |
| 17 | 1.4 · 28 | Python subscriber code and entry point; build; `ros2 topic pub /chatter …` → "I heard: Hello ROS 2" | p3–p21, IMG001–IMG019 | CL, BO, RO, SS | Python subscriber written, built and receiving | Listing differs slightly from the saved file (names) | `…/simple_subscriber.py`, `setup.py` |
| 18 | 1.4 · 28 | **C++ publisher → Python subscriber**: "I heard: Hello ROS 2 - counter: 0 … 2" | p21–p23 (output on p22), IMG020, P0372–P0393 (epoch 1782388747 = 2026-06-25 11:59 UTC) | RO, SS | Cross-language communication demonstrated historically | Only three messages shown | both example packages |
| 19 | 1.4 · 29 | C++ subscriber code, `CMakeLists.txt` change, build (cpp 5.79 s); `ros2 topic pub` → "I heard: Hello ROS 2" | p24–p41, IMG021–IMG031 | CL, BO, RO, SS | C++ subscriber built and receiving | The C++ source is recorded only as a text listing (P0472–P0508); its only screenshot (IMG022) shows the new, empty file, so the saved content is inferred from the successful build and output | `…/simple_subscriber.cpp`, `CMakeLists.txt` |
| 20 | 1.4 · 29 | **Python publisher → C++ subscriber**: "I heard: Hello ROS 2 - counter: 0 … 3" | p41–p42, IMG031–IMG032, P0750–P0765 (epoch 1782430999 = 2026-06-25 23:43 UTC, 2026-06-26 01:43 VM local time) | RO, SS | Cross-language communication demonstrated historically in the other direction | Subscriber output only in the screenshot | both example packages |
| 21 | 1.4 · 30–31 | Why robot models; URDF elements (robot, link, visual, collision, inertial, joint), tree rules, joint types | p44–p50 | C | Conceptual study of robot description | Theory only; `collision`/`inertial` described imprecisely | report §8 |
| 22 | 1.4 · 32 | `ros2 pkg create --build-type ament_cmake arduinobot_description`; `colcon build` (3 packages); `urdf/`, `meshes/` folders; `CMakeLists.txt` `install(DIRECTORY meshes urdf …)` | p51–p73, IMG033–IMG036, IMG051–IMG052 | RO, BO, SS, CL | Description package created | `package.xml` never edited or shown; the `install(DIRECTORY …)` edit exists only as a text listing (P1483–P1498) – IMG051/IMG052 show the unmodified and comment-stripped file; copying of the STL files is not shown (IMG034 shows only the folder path) | `arduinobot_description/` |
| 23 | 1.4 · 32 | Complete Xacro model written: 8 links, 7 joints, mimic `joint_5` ← `joint_4` × −1, mesh scale 0.01; names, origins, axes, limits and meshes match the instructor file (only the `PI` property differs: 3.14159 vs 3.14159265359) | p65–p70, P1231–P1425, IMG046–IMG050 | CL, SS | The student wrote the full kinematic/visual model | No `<collision>`/`<inertial>` blocks (the instructor file has them); explanation section stops after `forward_drive_arm` | `urdf/arduinobot.urdf.xacro` |
| 24 | 1.4 · 32 | `ros2 launch urdf_tutorial display.launch.py model:=…/arduinobot.urdf.xacro`; RViz shows the **complete red arduinobot model** (Global Status: Ok, RobotModel, TF) | p76–p79, P1563–P1582, IMG054 (p76), IMG055 (p79) (VM clock 2026-07-03); base-only stage earlier in the notes, p59–p64, IMG040–IMG045 (VM clock 2026-07-07) | RO, SS | Historical RViz visualisation of the student's model | Used `urdf_tutorial`, **not** the instructor `display.launch.py`/`display.rviz`; no slider movement shown; fixed frame not visible | `display.launch.py`, `display.rviz` (instructor equivalents) |
| 25 | 1.4 · 32 | Dimension diagrams of the course robot (3.5 cm, 8 cm, 8.2 cm, 2.2 cm …) | p84–p89, IMG056–IMG060 | D | IMG057–IMG060 are Udemy-watermarked course frames whose offsets equal the URDF values ÷ 10 (3.5 cm ↔ `joint_2` z 0.35, 8 cm ↔ `joint_3` z 0.8, 8.2 cm ↔ 0.82) | Not student work. IMG056 (p84, the only source of "3.07 cm") has no watermark and embeds C2PA metadata of an AI image generator, so it is not treated as course evidence | audit §3.1 (model scale) |
| 26 | 1.5 · 34 | RViz 2 purpose, displays, why graphical visualisation | p1–p5, P0001–P0117 (text flow diagram P0012–P0025; no images) | C | Conceptual study | No RViz run in this note; RViz described as a pure subscriber (see §6) | report §10 |
| 27 | 1.5 · 35 | Parameters concept (per node, reuse across robots) | p5–p6 | C | Conceptual study | Theory only | report §11 |
| 28 | 1.5 · 36 | Python parameter lab: empty `simple_parameter.py` created in `arduinobot_py_examples/arduinobot_py_examples` | p6–p9, P0148–P0153, IMG001–IMG003 (render p7, p8, p9) | SS | File created in the workspace | The file is empty in the last screenshot | `…/simple_parameter.py` |
| 29 | 1.5 · 36 | Full listing of `simple_parameter.py` (same names and defaults as the instructor file) | p9–p10, P0155–P0190 | CL | The student recorded the parameter node | Listing unindented (not valid Python as recorded) and logs the string parameter with `%d`; **no** entry point, `package.xml` change, build, run or `ros2 param` output documented | `…/simple_parameter.py`, `setup.py`, `package.xml` |

## 4. Summary by category

| Category | Content |
|---|---|
| **A – Documented student work** (rows 4–7, 11–20, 22–24, 28–29; row 8 as installation only) | ROS 2 Humble installation and environment set-up; workspace and package creation; Python and C++ publishers and subscribers built and run; topic inspection with `ros2 topic list/echo/info/hz`; **both** cross-language directions (C++→Python and Python→C++); `arduinobot_description` package with a complete URDF/Xacro model visualised in RViz via `urdf_tutorial`; start of the Python parameter lab (file creation and code listing only). Conceptual study (rows 1–3, 9, 10, 21, 26, 27) is also category A as *study*, not as implementation. |
| **B – Instructor material** | Course material reproduced in the notes (e.g. row 25) and the whole repository, including the Section 4 packages that form the delivered workspace, the meshes, `display.launch.py`, `display.rviz`, `gazebo.launch.py`, the C++ parameter example, and all later sections. |
| **C – Assignment preparation** | Corrections C1–C12 (`PROVENANCE.md`), the parameter tests, verification scripts and runs, figures, documentation and the report. The runnable, verified parameter example and the instructor `display.launch.py` path were exercised during preparation, not by the student's notes. |
| **D – Future work / not documented** | Python parameter lab completion (entry point, build, run, `ros2 param`); C++ parameters; services and actions in practice; the instructor's `display.launch.py`/`display.rviz` path (lesson 33 absent); Gazebo simulation; ros2_control; MoveIt 2; application/task server; Alexa; firmware and physical robot. |

## 5. Relationships between notes, instructor code and delivered code

* **Python publisher (row 12):** the notes' code is identical to the instructor's, including
  `frequency_ = 1.0` passed as the timer *period*; the delivered code keeps the 1 Hz
  behaviour but computes the period as `1.0 / frequency_` (C1). The notes' own Ctrl+C
  traceback (1.3, p52–p54, IMG019) is the same shutdown behaviour corrected by C2.
* **C++ publisher (row 15):** the student's string has a space after "counter:"; the
  delivered code keeps the instructor's string. Both are historical facts.
* **Parameter node (row 29):** the notes' listing has the instructor's callback design and,
  in addition, `%d` for the string parameter, which – once the unindented listing is
  re-indented – would raise a `TypeError` when that parameter is set. The delivered code
  uses `%s` (as the instructor does) and a corrected callback (C4). Completion of the lab is **not** documented; the runnable parameter
  demonstration is category C.
* **Robot model (rows 23–24):** the student's model matches the instructor's kinematics;
  the delivered workspace uses the instructor's file (which adds collision and inertial
  elements). The student's historical RViz screenshot (1.4, p79, IMG055) and the
  preparation's RViz screenshots (`verification/logs/run_2026-09-28/`) are kept separate.

## 6. Technical points in the notes corrected in the report (record unchanged)

| Locator | Point in the notes | Correct statement |
|---|---|---|
| 1.4, p83/p85, P1734, P1782–P1789 | joint_1 limits explained as −π…π (±180°) | the code uses −π/2…π/2 (±90°) |
| 1.4, p81/p85, P1651, P1769–P1773 | scale 0.01 "reduces the mesh to the correct dimensions"; 0.307 m quoted as a CAD value | the meshes are consistent with millimetres; 0.01 yields a model 10× the real size (course frames IMG057–IMG059 give 3.5 cm, 8 cm, 8.2 cm for the URDF's 0.35, 0.8, 0.82 m) |
| 1.4, p63, P1170–P1171 | −X called "left", −Y "back" | in ROS base frames +X is forward and +Y left; −X is backward, −Y right |
| 1.4, p64, P1204–P1215 | rebuild required after editing the Xacro | not when `model:=` points to the source file; relaunching re-reads it |
| 1.4, p48, P0905–P0911 | `<collision>`/`<inertial>` "assign volume/inertia" | collision = contact geometry; inertial = mass, centre of mass and inertia tensor |
| 1.5, p10, P0177 | string parameter logged with `%d` (once the listing is re-indented, setting the parameter would raise `TypeError`) | use `%s` |
| 1.5, p1/p5, P0010, P0113 | RViz only subscribes | RViz mainly consumes topics and TF but its tools can also publish (e.g. `/initialpose`, `/goal_pose`, `/clicked_point`) |
| 1.5, p2, P0045 | `ros2 topic echo` without a topic | `ros2 topic echo /chatter` |
