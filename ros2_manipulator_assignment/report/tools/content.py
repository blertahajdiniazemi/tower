"""Text of the report. Every technical statement is tied to the delivered code, the
verification logs, the student's notes or an inspected documentation page."""
import os

A = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FIG = os.path.join(A, 'report', 'figures')
SRC = os.path.join(A, 'arduinobot_ws', 'src')
TITLE = 'Robot Operating System 2: Architecture, Communication and Application in a Manipulator Robot'


def excerpt(rel, start, end, include_end=True):
    """Lines of a delivered source file from the first line containing `start` up to the
    first following line containing `end`; fails loudly if the file changed."""
    lines = open(os.path.join(SRC, rel)).read().split('\n')
    i = next(k for k, l in enumerate(lines) if start in l)
    j = next(k for k in range(i + 1, len(lines)) if end in lines[k])
    chunk = lines[i:j + 1] if include_end else lines[i:j]
    indent = min(len(l) - len(l.lstrip()) for l in chunk if l.strip())
    return '\n'.join(l[indent:] for l in chunk)


def title_page(r):
    r.para('[University Name]', align='center', size=14, space_after=2)
    r.para('[Faculty / Department] · [Degree Programme]', align='center', size=12, space_after=60)
    p = r.para('**' + TITLE + '**', align='center', size=21, space_after=14)
    p.paragraph_format.line_spacing = 1.15
    r.para('Assignment report', align='center', size=13, space_after=70)
    rows = [
        ('Student', '[Student Name] ([Student ID])'),
        ('Module', '[Module Name and Code]'),
        ('Instructor / supervisor', '[Supervisor Name]'),
        ('Course studied', '*Robotics and ROS 2 – Learn by Doing! Manipulators* '
                           '(course material and repository by Antonio Brandi)'),
        ('Target environment', 'Ubuntu 22.04 LTS, ROS 2 Humble Hawksbill'),
        ('Submission date', '[Submission Date]'),
    ]
    for k, v in rows:
        p = r.para('**%s:** %s' % (k, v), align='center', size=12, space_after=4)
    r.para('', space_after=60)
    r.para('*Placeholders in square brackets are to be completed by the student.*',
           align='center', size=10)
    r.page_break()


def abstract(r):
    r.heading('Abstract', 1, numbered=False)
    r.body(
        'This report explains the Robot Operating System 2 (ROS 2) through one concrete project: the '
        'three-degree-of-freedom manipulator with gripper ("arduinobot") of the course *Robotics and '
        'ROS 2 – Learn by Doing! Manipulators*. Three kinds of source were used and kept apart: the '
        'student\'s own course notes, which establish what was studied and practised; the instructor\'s '
        'public repository, whose Section 4 workspace at commit 4936385 was taken as the software '
        'baseline; and the official ROS 2 Humble documentation, which supports the technical explanations.')
    r.body(
        'A clean workspace with three packages was prepared and twelve small, documented corrections were '
        'made, concerning the timer period, clean shutdown, parameter validation, dependency declarations '
        'and a stale RViz configuration. The unchanged robot model and the corrected examples were built '
        'and exercised in an Ubuntu 22.04 / ROS 2 Humble container: Python-to-C++ and C++-to-Python '
        'publisher–subscriber communication, parameter inspection and updates including the rejection of '
        'invalid updates, URDF processing, joint states, TF and an RViz display rendered on a virtual '
        'screen. The notes document the installation, workspace creation, publishers and subscribers in '
        'both languages and a complete URDF model visualised in RViz; the parameter laboratory is '
        'documented only as a code listing.')
    r.body(
        'The main limitations are that verification ran in a container rather than on the student\'s own '
        'machine, that RViz used software rendering, that simulation, ros2_control, MoveIt 2 and the '
        'physical robot were not exercised, and that the robot description is a kinematic model at ten '
        'times the physical size with placeholder dynamic parameters.')
    r.page_break()


def introduction(r, c):
    r.heading('Introduction', 1, page_break=True)
    r.heading('Purpose and context', 2)
    r.body(
        'The purpose of this report is to explain what ROS 2 is, why it is used and how its main '
        'mechanisms work, using a manipulator project that was studied in a practical online course. '
        'Rather than describing ROS 2 in the abstract, each concept is connected to a file, a command '
        'or a measured result of the prepared project. The course builds a small 3D-printable arm '
        'driven by four servo motors and an Arduino board, first as a "digital twin" in software and '
        'later as physical hardware %s.' % c('n11', 'repo'))
    r.heading('Target environment and scope', 2)
    r.body(
        'The target platform is Ubuntu 22.04 LTS with ROS 2 Humble Hawksbill, a combination for which '
        'Humble is released as Debian packages and which is a Tier 1 platform of that distribution '
        '%s. The scope follows the chain Ubuntu 22.04 → ROS 2 Humble → workspace → packages → nodes → '
        'publisher/subscriber communication → robot description → TF → RViz → parameters → manipulator '
        'case study. Simulation, motion control, motion planning, voice control and hardware belong to '
        'later parts of the course; they are described as context and future work only.'
        % c('d_install', 'd_humble'))
    r.heading('Sources and how claims are classified', 2)
    r.body(
        'Four categories are used consistently. **Category A – documented student work** is work or study '
        'supported by a located piece of evidence in the student\'s notes %s. **Category B – instructor '
        'material** is code, models and configuration supplied by the course author %s. **Category C – '
        'assignment preparation** covers the changes, verification, figures and documentation produced '
        'for this assignment %s. **Category D – future work** covers activities whose completion is not '
        'documented in the supplied notes. Historical screenshots from the notes and new verification '
        'results are always identified separately.' % (c('n11', 'n12', 'n13', 'n14', 'n15'), c('repo'), c('prep')))


def what_is_ros2(r, c):
    r.heading('What is ROS 2?', 1)
    r.body(
        'The official documentation describes the Robot Operating System as "a set of software libraries '
        'and tools for building robot applications" %s and states that, despite its name, it is "not an '
        'operating system in the traditional sense" %s. ROS 2 runs as ordinary user-space software on top '
        'of an operating system – here Ubuntu 22.04 – and relies on it for processes, threads, networking '
        'and files. What ROS 2 adds is a common way for independent pieces of robot software to find each '
        'other, exchange typed data and be configured, together with tools for building, launching and '
        'inspecting them.' % (c('d_index'), c('d_about')))
    r.body(
        'A running ROS 2 system is described as a *graph*: nodes connected by topics, services, actions '
        'and parameters %s. Nodes "can communicate with other nodes within the same process, in a '
        'different process, or on a different machine" %s, and they find each other automatically through '
        'the middleware\'s discovery mechanism %s. This is what makes ROS 2 suitable for distributed '
        'applications: a driver, an algorithm and a visualisation tool can be developed separately and '
        'combined at run time, on one computer or several.' % (c('d_unodes'), c('d_nodes'), c('d_discovery')))
    r.body(
        'ROS 2 is released in *distributions*, versioned sets of packages kept stable after release %s. '
        'Humble Hawksbill, the eighth ROS 2 release, was published on 23 May 2022 and reaches end of life '
        'in May 2027 %s. The notes record these ideas as conceptual study, including that ROS is a '
        'framework on top of an operating system (1.2 Course Notes, lessons 16, 17 and 20) %s.'
        % (c('d_distros'), c('d_humble', 'd_distros'), c('n12')))


def why_ros2(r, c):
    r.heading('Why ROS 2?', 1)
    r.body(
        'The engineering motivation recorded in the notes is reuse: without a common framework, '
        'application code is tied to one robot\'s hardware and must be rewritten for each new platform, '
        'whereas a framework with standard interfaces lets the same application logic run on different '
        'robots behind hardware abstractions (1.2 Course Notes, lessons 17, 20 and 21) %s. The project in '
        'this report illustrates this on a small scale. The robot-specific part is a model file and a '
        'few configuration files; the programs that turn the model into coordinate frames and a 3D view '
        '– robot_state_publisher, joint_state_publisher and RViz – are generic Humble packages used '
        'unchanged.' % c('n12'))
    r.body(
        'ROS 2 was also designed to address limitations of ROS 1 that the notes list for lesson 18: '
        'changing network conditions, multi-robot systems, embedded platforms, security and real-time '
        'behaviour %s. {ref:tab-ros1} relates these motivations to what the Humble documentation actually '
        'provides and qualifies each point, because several of them are capabilities that must be '
        'configured rather than guarantees.' % c('n12'))
    r.table(
        ['Motivation (notes, lesson 18)', 'What ROS 2 provides (documentation)', 'Qualification'],
        [
            ['Unreliable or changing networks', 'DDS/RTPS middleware with configurable Quality of Service '
             '(history, reliability, durability) %s' % c('d_vendors', 'd_qos'),
             'QoS must be chosen and must be compatible between endpoints; it does not guarantee timing.'],
            ['Many robots and computers', 'Distributed discovery ("not centralized like in ROS 1") and '
             'domain IDs that separate logical networks %s' % c('d_vendors', 'd_domain'),
             'All participants must use a compatible middleware and the same domain.'],
            ['Security', 'Secured communication between nodes through the middleware\'s DDS security '
             'plug-ins %s' % c('d_security'), 'Security is "turned off by default" and needs '
             'security files for each participant.'],
            ['Real-time behaviour', 'Designed "with real-time performance constraints in mind" %s'
             % c('d_realtime'), 'Requires a real-time kernel and deterministic code; the standard '
             'executors are not suited to hard real-time use %s.' % c('d_executors')],
            ['Several programming languages', 'Client libraries rclcpp and rclpy share one C core, rcl %s'
             % c('d_clientlib'), 'Demonstrated in this project for C++ and Python.'],
        ],
        'tab-ros1', 'Motivations for ROS 2 recorded in the notes and what the Humble documentation '
        'provides.', [4.0, 6.3, 5.7])


def architecture(r, c):
    r.heading('ROS 2 Architecture', 1)
    r.heading('Layers', 2)
    r.body(
        'ROS 2 is organised in layers ({ref:fig-arch}). User code is written against a *client library*: '
        'rclcpp for C++ or rclpy for Python. Both are built on rcl, a common library written in C, so '
        'behaviour that is not language-specific is implemented once %s. Below rcl, the ROS middleware '
        'interface (rmw) is "the interface between the ROS 2 software stack and the underlying middleware '
        'implementation"; the middleware, a DDS or RTPS implementation, is responsible for discovery, '
        'publish/subscribe and request/reply mechanics and serialisation %s. In Humble the default '
        'implementation is rmw_fastrtps_cpp with eProsima Fast DDS %s; the test container reported '
        'exactly this implementation %s. The notes contain the same layered view as a text diagram '
        '(1.2 Course Notes, lesson 19) %s.' % (c('d_clientlib'), c('d_internal'), c('d_humble', 'd_vendors'),
                                            c('prep'), c('n12')))
    r.figure(os.path.join(FIG, 'fig01_ros2_architecture.png'), 'fig-arch',
             'ROS 2 Humble software stack with the nodes of this project.', width_cm=14.0,
             attribution='New diagram (category C) based on the documentation cited in Section 4.1; the '
                         'default RMW was confirmed in the test container.')
    r.heading('Graph, interfaces and execution', 2)
    r.body(
        'Nodes interact through three interface styles: topics for continuous data streams, services for '
        'short request/response calls and actions for long-running goals with feedback %s. Their data '
        'types are defined in an interface definition language (.msg, .srv and .action files) from which '
        'code is generated for each language %s; this is why a C++ node and a Python node can exchange a '
        '`std_msgs/msg/String` without any conversion code. Parameters are a fourth, node-local mechanism '
        'for configuration (Section 11).' % (c('d_topics', 'd_services', 'd_actions'), c('d_interfaces')))
    r.body(
        'Callbacks are executed by an *executor*: calling `spin()` runs a single-threaded executor that '
        'waits for timers, messages and other events and invokes the matching callbacks %s. Discovery is '
        'automatic: a node advertises itself on its ROS domain and connections are made only between '
        'endpoints with compatible QoS settings %s. The project stays within this basic model: every '
        'example node is spun by one executor, uses the default domain and communicates over topics and '
        'the built-in parameter services.' % (c('d_executors'), c('d_discovery')))


def nodes(r, c):
    r.heading('Nodes', 1)
    r.body(
        'A node is "a participant in the ROS 2 graph" and typically performs one logical task %s. A node '
        'is not the same thing as its communication endpoints: publishers, subscriptions, timers and '
        'parameters are entities *owned* by a node, and one node may own many of them. Nor is a node the '
        'same as an operating-system process: an executable "can contain one or more nodes" %s. The '
        'verification illustrates this: while RViz was running, `ros2 node list` showed `/rviz2` and an '
        'additional `/transform_listener_impl_…` node created inside the same RViz process %s.'
        % (c('d_nodes'), c('d_unodes'), c('prep')))
    r.body('{ref:tab-nodes} lists the nodes that were inspected in the delivered workspace, together with '
           'the generic Humble nodes started by the description package.')
    r.table(
        ['Executable (package)', 'Node name', 'Language', 'Entities and responsibility'],
        [
            ['simple_publisher (arduinobot_py_examples)', '/simple_publisher', 'Python',
             'publisher on `/chatter`, 1 s timer; publishes "Hello ROS 2 - counter: N"'],
            ['simple_subscriber (arduinobot_py_examples)', '/simple_subscriber', 'Python',
             'subscription on `/chatter`; logs "I heard: …"'],
            ['simple_parameter (arduinobot_py_examples)', '/simple_parameter', 'Python',
             'parameters `simple_int_param` (28), `simple_string_param` ("Antonio"); set-parameter callback'],
            ['simple_publisher (arduinobot_cpp_examples)', '/simple_publisher', 'C++',
             'publisher on `/chatter`, 1 s wall timer; publishes "Hello ROS 2 - counter:N"'],
            ['simple_subscriber (arduinobot_cpp_examples)', '/simple_subscriber', 'C++',
             'subscription on `/chatter`; logs "I heard: …"'],
            ['simple_parameter (arduinobot_cpp_examples)', '/simple_parameter', 'C++',
             'same parameters and callback contract as the Python node (instructor example)'],
            ['robot_state_publisher', '/robot_state_publisher', 'C++ (Humble)',
             'reads `robot_description`, subscribes to `/joint_states`, publishes `/tf`, `/tf_static`, '
             '`/robot_description`'],
            ['joint_state_publisher(_gui)', '/joint_state_publisher', 'Python (Humble)',
             'publishes `/joint_states` for all non-fixed joints, from sliders or fixed values'],
            ['rviz2', '/rviz2', 'C++ (Humble)', '3D visualisation of the model and TF'],
        ],
        'tab-nodes', 'Nodes of the delivered workspace and the Humble nodes it uses.',
        [4.6, 3.4, 2.1, 5.9], font_size=9)
    r.body(
        'The Python and C++ versions share node names, so each demonstration runs one publisher and one '
        'subscriber; to run all nodes together a node can be renamed at start-up, e.g. '
        '`--ros-args -r __node:=py_simple_publisher` %s. The notes document writing, building and '
        'running both publishers and both subscribers (1.3, lessons 26–27; 1.4, lessons 28–29) %s.'
        % (c('d_unodes'), c('n13', 'n14')))


def pubsub(r, c):
    r.heading('Publisher–Subscriber Communication', 1)
    r.heading('Topic, message type and QoS', 2)
    r.body(
        'Topics implement "a strongly-typed, anonymous publish/subscribe system": publishers and '
        'subscribers do not address each other, they only agree on a topic name and a message type %s. '
        'The two must be distinguished. In this project the topic *name* is `/chatter` (created as the '
        'relative name `chatter` in the root namespace) and its *type* is `std_msgs/msg/String`, a '
        'message with one string field `data`. Publishers and subscribers must use the same type to '
        'communicate %s. {ref:fig-pubsub} shows the two cross-language combinations that were exercised.'
        % (c('d_topics'), c('d_utopics')))
    r.figure(os.path.join(FIG, 'fig02_pubsub.png'), 'fig-pubsub',
             'Publisher → topic → subscriber in both cross-language directions.', width_cm=14,
             attribution='New diagram (category C); names taken from the delivered code. It shows the '
                         'configuration, not a measured trace.')
    r.body(
        'Both publishers and subscribers pass the integer 10 as their QoS argument. In rclpy and rclcpp '
        'this selects a profile with history "keep last" and depth 10; the remaining policies take the '
        'defaults, which are "reliable" and "volatile" %s. `ros2 topic info -v /chatter` in the test '
        'container reported RELIABLE and VOLATILE for both endpoints %s. These are configured policies, '
        'not promises: "reliable" makes the middleware retransmit lost samples, but the queue depth still '
        'bounds how many samples can wait, and no policy guarantees a delivery time.'
        % (c('d_qos', 'd_pypubsub'), c('prep')))
    r.heading('Timer, callbacks and the frequency correction', 2)
    r.body(
        'The publishers are driven by timers. `create_timer()` in rclpy takes a period in seconds; the '
        'official tutorial writes `timer_period = 0.5  # seconds` %s. The instructor\'s Python publisher '
        'stored the value 1.0 in a variable called `frequency_` and passed it directly as the period. At '
        '1.0 the result is the same, but any other "frequency" would have produced the inverse rate. The '
        'delivered code keeps `frequency_` as a rate in hertz and passes `1.0 / self.frequency_` '
        '({ref:lst-pub}); this correction is category C. The same code appears unchanged in the student\'s '
        'notes (1.3 Course Notes, lesson 26, p28–p29) %s.' % (c('d_pypubsub'), c('n13')))
    r.code(excerpt('arduinobot_py_examples/arduinobot_py_examples/simple_publisher.py',
                   'class SimplePublisher', 'self.counter_ += 1'),
           'lst-pub', 'Python publisher: publisher creation, timer and timer callback '
           '(`arduinobot_py_examples/simple_publisher.py`, delivered version).')
    r.body(
        'On the receiving side ({ref:lst-sub}) the C++ subscriber registers `msgCallback` with '
        '`create_subscription`. The callback is not called directly by user code; the executor invokes '
        'it when `rclcpp::spin()` finds a new message %s.' % c('d_executors'))
    r.code(excerpt('arduinobot_cpp_examples/src/simple_subscriber.cpp',
                   'SimpleSubscriber() : Node', 'RCLCPP_INFO_STREAM', include_end=True) + '\n  }',
           'lst-sub', 'C++ subscriber: subscription creation and callback '
           '(`arduinobot_cpp_examples/src/simple_subscriber.cpp`, instructor code, unchanged).')
    r.heading('Command-line inspection and cross-language results', 2)
    r.body(
        'The ROS 2 command-line tools inspect the running graph: `ros2 topic list -t` lists topics with '
        'their types, `ros2 topic info -v` shows the endpoints and their QoS, `ros2 topic echo` prints '
        'messages and `ros2 topic hz` measures the receive rate %s. The documentation notes that the rate '
        'reported by `ros2 topic hz` is measured on its own subscription and "may not exactly match the '
        'publisher rate" %s; the measured values below are therefore observations, while the 1 s timer '
        'period is the configured value.' % (c('d_utopics'), c('d_utopics')))
    r.table(
        ['Direction', 'Publisher → subscriber (package / executable)', 'Result in the test container'],
        [
            ['(a) Python → C++', 'arduinobot_py_examples / simple_publisher → '
             'arduinobot_cpp_examples / simple_subscriber',
             '33 consecutive messages received (counter 0–32, "I heard: Hello ROS 2 - counter: 0" …); '
             'average rate 1.000 Hz; no traceback on Ctrl+C'],
            ['(b) C++ → Python', 'arduinobot_cpp_examples / simple_publisher → '
             'arduinobot_py_examples / simple_subscriber',
             '33 consecutive messages received (counter 0–32, "I heard: Hello ROS 2 - counter:0" …); '
             'average rate 1.000 Hz; no traceback on Ctrl+C'],
        ],
        'tab-pubsub', 'Publisher–subscriber runs in the preparation environment (log '
        '`verification/logs/run_2026-09-28/20_pubsub.log`).', [2.7, 5.6, 7.7], font_size=9)
    r.body(
        'The student\'s notes contain historical evidence of the same two directions on the student\'s '
        'virtual machine, dated 25 June 2026 by the VM clock: a C++ publisher feeding the Python '
        'subscriber (1.4, lesson 28, p22, screenshot IMG020) and the Python publisher feeding the C++ '
        'subscriber (1.4, lesson 29, p41–p42, IMG031–IMG032). The notes also show `ros2 topic echo`, '
        '`ros2 topic info --verbose` and `ros2 topic hz` measuring 1.000 Hz for both publishers '
        '(1.3, lessons 26–27) %s. These historical runs are category A; the runs in {ref:tab-pubsub} are '
        'category C. The C++ publisher prints no space after "counter:", while the student\'s own C++ '
        'version and the Python publisher do; the instructor\'s string was kept unchanged. This messaging '
        'example exchanges text only and does not move the robot model.' % c('n13', 'n14'))


def workspaces(r, c):
    r.heading('Workspaces and Packages', 1)
    r.heading('Underlay, overlay and colcon', 2)
    r.body(
        'A workspace is "a directory containing ROS 2 packages" %s. The ROS 2 installation in '
        '`/opt/ros/humble` acts as the *underlay*; a local workspace sourced on top of it is an '
        '*overlay*, whose packages take precedence over those of the underlay %s. Sourcing '
        '`install/setup.bash` adds the overlay and the underlay it was built against to the current '
        'shell only, so it must be repeated in each new terminal %s. The notes document this sequence on '
        'the student\'s machine: `~/arduinobot_ws/src`, a first `colcon build`, creation of both example '
        'packages, a rebuild, sourcing and `ros2 pkg list` showing the new packages (1.3 Course Notes, '
        'lesson 25) %s.' % (c('d_workspace'), c('d_env', 'd_workspace'), c('d_workspace'), c('n13')))
    r.body(
        'colcon builds the packages in dependency order %s; with `--symlink-install`, Python modules and '
        'launch files are installed as links to the source tree and can be edited without reinstalling '
        '%s. The instructor\'s repository holds seven snapshots of the same workspace, one per course '
        'section, with identical package names; only the Section 4 snapshot was placed in `src` %s.'
        % (c('d_build'), c('d_colcon'), c('repo', 'prep')))
    r.figure(os.path.join(FIG, 'fig03_workspace.png'), 'fig-ws',
             'Delivered workspace (source tree). `build/`, `install/` and `log/` are generated by colcon.',
             width_cm=12.5, attribution='New figure (category C).')
    r.heading('Package types and dependency declarations', 2)
    r.body(
        'Every package has a `package.xml` manifest that declares its dependencies %s. Two build types '
        'are used ({ref:tab-pkgs}). In the ament_python package, `setup.py` registers console-script '
        'entry points such as `simple_publisher = arduinobot_py_examples.simple_publisher:main`, and '
        '`setup.cfg` installs them where `ros2 run` looks for executables %s. In the ament_cmake packages, '
        '`add_executable`, `ament_target_dependencies` and `install(TARGETS …)` build and install the C++ '
        'programs %s, and `install(DIRECTORY launch meshes urdf rviz …)` copies the description\'s '
        'resources into the package\'s share directory, where `package://` URIs and '
        '`get_package_share_directory()` find them.' % (c('d_build'), c('d_pypubsub', 'd_package'), c('d_cpppubsub')))
    r.table(
        ['Package', 'Build type', 'Declared dependencies (delivered)', 'Installs'],
        [
            ['arduinobot_py_examples', 'ament_python', 'exec: rclpy, std_msgs, rcl_interfaces; test: '
             'ament_copyright, ament_flake8, ament_pep257, python3-pytest', '3 console scripts'],
            ['arduinobot_cpp_examples', 'ament_cmake', 'depend: rclcpp, std_msgs, rcl_interfaces',
             '3 executables (`lib/`)'],
            ['arduinobot_description', 'ament_cmake', 'exec: ament_index_python, launch, launch_ros, '
             'robot_state_publisher, urdf, joint_state_publisher, joint_state_publisher_gui, rviz2, xacro, '
             'ros2launch; ros_gz_sim, ros_gz_bridge (optional Gazebo launch only)',
             '`launch/`, `meshes/`, `urdf/`, `rviz/`'],
        ],
        'tab-pkgs', 'Packages of the delivered workspace.', [3.8, 2.4, 6.9, 2.9], font_size=9)
    r.body(
        'Direct dependencies should be declared even when they arrive transitively; the launch files\' '
        'imports `ament_index_python`, `launch` and `launch_ros` were therefore added to the manifest '
        '(category C). `rosdep` resolves declared keys to system packages %s; in the test container it '
        'reported only `ros_gz_sim` and `ros_gz_bridge` missing, which only the optional Gazebo launch '
        'file needs %s.'
        % (c('d_rosdep'), c('prep')))


def urdf(r, c):
    r.heading('Robot Description and URDF', 1)
    r.heading('Links, joints and origins', 2)
    r.body(
        'The Unified Robot Description Format (URDF) is an XML format "for specifying the geometry and '
        'organization of robots" %s. A model is a tree of *links* (rigid bodies) connected by *joints*; '
        'each joint names one parent and one child link, so the tree has exactly one root %s. The '
        'arduinobot model has eight links and seven joints ({ref:fig-urdf}, {ref:tab-joints}), all read '
        'from the expanded file of the delivered package %s.' % (c('d_urdf'), c('d_urdf_visual'), c('prep')))
    r.figure_pair(
        (os.path.join(FIG, 'fig05_urdf_tree.png'), 'fig-urdf',
         'Link–joint tree of `arduinobot.urdf.xacro`. Dashed edges: fixed joints; `joint_5` mimics '
         '`joint_4` (×−1).', 7.4,
         'Generated from the verified model (category C); replaces the instructor\'s 2021 '
         '`arduinobot.pdf`, which still shows a removed `tool_link`.'),
        (os.path.join(FIG, 'fig08_offline_render.png'), 'fig-render',
         'Offline render of the instructor\'s meshes placed with the URDF kinematics (all joints 0).', 7.6,
         'Rendered with matplotlib from the expanded URDF (category C); not an RViz test. Axes in model '
         'metres.'))
    r.table(
        ['Joint', 'Type', 'Parent → child', 'Origin xyz (m)', 'Axis', 'Limits (rad)'],
        [
            ['virtual_joint', 'fixed', 'world → base_link', '0 0 0', '–', '–'],
            ['joint_1', 'revolute', 'base_link → base_plate', '0 0 0.307', 'z', '−π/2 … π/2'],
            ['joint_2', 'revolute', 'base_plate → forward_drive_arm', '−0.02 0 0.35', 'x', '−π/2 … π/2'],
            ['joint_3', 'revolute', 'forward_drive_arm → horizontal_arm', '0 0 0.8', 'x', '−π/2 … π/2'],
            ['horizontal_arm_to_claw_support', 'fixed', 'horizontal_arm → claw_support', '0 0.82 0', '–', '–'],
            ['joint_4', 'revolute', 'claw_support → gripper_right', '−0.04 0.13 −0.1', 'z', '−π/2 … 0'],
            ['joint_5', 'revolute (mimic)', 'claw_support → gripper_left', '−0.22 0.13 −0.1', 'z',
             '0 … π/2; = −1 × joint_4'],
        ],
        'tab-joints', 'Joints of the model (all revolute joints: effort 30, velocity 10 as supplied '
        'Xacro properties).', [4.3, 1.9, 4.3, 2.3, 0.9, 2.3], font_size=8.5)
    r.body(
        'Two kinds of origin must be distinguished. A joint `<origin>` places the child link\'s frame '
        'relative to the parent link\'s frame %s; it defines the kinematics. The `<origin>` inside a '
        'link\'s `<visual>` or `<collision>` element only places the geometry relative to the link\'s own '
        'frame %s. {ref:lst-urdf} shows both for `forward_drive_arm`: `joint_2` puts the shoulder frame '
        '0.35 m above the base plate and rotates it about the x axis, while the visual origin rotates and '
        'shifts the STL mesh so that it lines up with that frame. The notes record exactly this '
        'distinction when the student corrected the base mesh offset with a visual origin of '
        '(−0.5, −0.5, 0) (1.4, lesson 32, p62–p64) %s.' % (c('d_urdf_visual'), c('d_urdf_visual'), c('n14')))
    r.code(excerpt('arduinobot_description/urdf/arduinobot.urdf.xacro',
                   '<link name="forward_drive_arm">', '</visual>') + '\n    <!-- collision element identical to the visual -->\n</link>\n\n'
           + excerpt('arduinobot_description/urdf/arduinobot.urdf.xacro', '<joint name ="joint_2"', '</joint>'),
           'lst-urdf', 'A link with its visual element and the joint that moves it '
           '(`arduinobot_description/urdf/arduinobot.urdf.xacro`, instructor file, unchanged; the '
           'repeated collision element is abbreviated).')
    r.heading('Xacro, meshes and physical properties', 2)
    r.body(
        'The file is a Xacro document: properties such as `PI`, `effort` and `velocity`, expressions like '
        '`${PI / 2}` and a macro `default_inertial` are expanded by the `xacro` program into plain URDF %s. '
        'The launch file runs xacro through a `Command` substitution and passes the result to '
        'robot_state_publisher as the `robot_description` parameter, the pattern shown in the documentation '
        '%s. Seven STL meshes are referenced with `package://arduinobot_description/meshes/<name>.STL` '
        'URIs; the verification resolved all fourteen visual and collision references with exact '
        'upper-case extensions %s.' % (c('d_xacro'), c('d_xacro'), c('prep')))
    r.body(
        '`<collision>` elements define geometry for collision checking and `<inertial>` elements define '
        'mass, centre of mass and inertia for physics simulation %s. In this model the collision geometry '
        'reuses the detailed visual meshes, and every link has the placeholder inertia '
        '`ixx = iyy = izz = 1.0` whatever its mass; effort 30 and velocity 10 are uniform Xacro '
        'properties. These are supplied model parameters, not measured properties of the robot, and '
        'the model is therefore a kinematic and visual description rather than a validated dynamic '
        'model. The documentation itself notes that velocity and effort values in its example "don\'t '
        'matter" for visualisation %s.' % (c('d_urdf_phys'), c('d_urdf_move')))
    r.body(
        'The mesh files carry no unit. Their coordinates are consistent with millimetres (for example, '
        'pivot bores 80.0 units apart), but the model scales them by 0.01, so one unit becomes one '
        'centimetre and the rendered arm is about 1.69 m tall ({ref:fig-render}). All joint origins were '
        'written for that scale: `joint_3` at 0.8 m equals the 80-unit bore spacing. Course video frames '
        'reproduced in the notes give the corresponding real offsets in centimetres – 3.5 cm, 8 cm and '
        '8.2 cm where the URDF uses 0.35 m, 0.8 m and 0.82 m (1.4, lesson 32, p86–p88) %s. The software model is therefore about ten '
        'times the physical size. It was deliberately not rescaled, because a correct rescale would '
        'require changing every origin and no measured dimensions of a built robot are available; model '
        'values in this report are quoted as model values.' % c('n14', 'repo'))
    r.heading('Degrees of freedom, gripper and mimic joint', 2)
    r.body(
        'The URDF contains five revolute joints, but the robot is not a five-degree-of-freedom arm. The '
        'arm has three independent degrees of freedom – base rotation (`joint_1`), shoulder (`joint_2`) '
        'and elbow (`joint_3`) – which position the gripper, as the notes explain for the course robot '
        '(1.1 Course Notes, lesson 5, p6) %s. `joint_4` opens and closes the right finger; it is a '
        'gripper actuation, not an additional arm DOF. `joint_5` moves the left finger but carries '
        '`<mimic joint="joint_4" multiplier="-1"/>`, so its position is always derived from `joint_4` and '
        'it adds no command variable. Consequently only four joints are commanded independently: '
        'joint_state_publisher_gui shows four sliders, and in the verification `joint_4 = −0.6` produced '
        '`joint_5 = 0.6` in `/joint_states` %s. The physical robot of the course uses a parallelogram '
        'linkage to keep the gripper orientation (notes, lesson 5) %s; the URDF does not model that '
        'linkage and treats the arm as a serial chain, and six supplied meshes of linkage parts are '
        'unused.' % (c('n11'), c('prep'), c('n11')))


def tf(r, c):
    r.heading('TF and Coordinate Frames', 1)
    r.body(
        'tf2 "lets the user keep track of multiple coordinate frames over time" and maintains them as a '
        'tree %s. Each URDF link becomes a frame. robot_state_publisher reads the model and publishes the '
        'transforms: those of fixed joints once on `/tf_static` with transient-local durability %s, and '
        'those of movable joints on `/tf` whenever new joint positions arrive on `/joint_states` %s. '
        'Joint positions come from joint_state_publisher or its GUI, which parse the model, publish '
        'values for all non-fixed joints and let robot_state_publisher "calculate all of the transforms" '
        '%s. {ref:fig-arch2} shows these relationships for the delivered launch file.'
        % (c('d_tf2'), c('d_humble'), c('d_rsp'), c('d_urdf_move')))
    r.figure(os.path.join(FIG, 'fig04_software_architecture.png'), 'fig-arch2',
             'Software architecture of the manipulator visualisation (`display.launch.py`). Dashed grey '
             'elements are optional or outside the verified core.', width_cm=16,
             attribution='New diagram (category C) derived from the delivered launch file and the '
                         'topics observed in the verification.')
    r.body(
        'In the verification, joint_state_publisher was started with fixed values (`joint_1 = 0.5`, '
        '`joint_2 = 0.3`, `joint_3 = −0.4`, `joint_4 = −0.6`) and published at a measured 9.99 Hz, '
        'while `ros2 run tf2_tools view_frames` recorded the tree in {ref:fig-frames}: the two fixed '
        'joints appear as static transforms and the five movable joints at about 10 Hz %s. '
        '`ros2 run tf2_ros tf2_echo world claw_support` returned the translation (−0.295, 0.499, 1.339) m '
        'and roll–pitch–yaw (−0.100, 0.000, 0.500) rad %s. An independent forward-kinematics '
        'calculation from the joint origins and axes of {ref:tab-joints} gives the same values, which '
        'confirms that the published TF tree matches the model: yaw equals `joint_1` and roll equals '
        '`joint_2 + joint_3`, because both pitch joints rotate about x.' % (c('d_tf2intro', 'prep'), c('prep')))
    r.figure(os.path.join(FIG, 'fig07_tf_frames.png'), 'fig-frames',
             'TF tree recorded by `view_frames` during the verification.', width_cm=7.0,
             attribution='Genuine output of `ros2 run tf2_tools view_frames` (category C, '
                         '`verification/logs/run_2026-09-28`), converted from PDF.')


def rviz(r, c):
    r.heading('RViz 2', 1)
    r.body(
        'RViz is "a 3D visualizer for the Robot Operating System" %s. It shows *displays*: the RobotModel '
        'display draws the robot "in the correct pose (as defined by the current TF transforms)" and the '
        'TF display draws the frame hierarchy %s. All data are transformed into the *fixed frame*, which '
        '"should not be moving relative to the world" %s. The delivered configuration `display.rviz` uses '
        'the fixed frame `base_link`; because `virtual_joint` fixes `base_link` to `world` with a zero '
        'offset, this is equivalent to the tree\'s root frame.' % (c('d_rviz'), c('d_rviz'), c('d_rviz')))
    r.figure(os.path.join(FIG, 'fig09_rviz_display_launch.png'), 'fig-rviz',
             '`ros2 launch arduinobot_description display.launch.py` in the preparation environment: '
             'RViz with RobotModel and TF displays, and the joint_state_publisher_gui window with four '
             'sliders.', width_cm=13.5,
             attribution='Genuine screenshot of the delivered workspace (category C), Ubuntu 22.04 / Humble '
                         'container, virtual X server with software OpenGL; 28 Sep. 2026.')
    r.body(
        'The RobotModel display obtains the model from the `/robot_description` topic, which '
        'robot_state_publisher publishes with transient-local durability, so that a subscriber started '
        'later still receives it – provided both sides use transient local %s. The instructor\'s '
        'configuration requested "Volatile". With the unmodified configuration and RViz 11.2.28, RViz '
        'started eight seconds after robot_state_publisher still displayed the model, and `ros2 topic '
        'info -v` showed that it had in fact subscribed with TRANSIENT_LOCAL (baseline log); the value '
        'was changed to "Transient Local" so that the file states the QoS actually used, and the late '
        'start was repeated with the delivered file ({ref:fig-latejoin}). Three stale entries for a '
        'link `tool_link`, which the model no longer contains, were removed from the same file %s. '
        'The URDF defines no `<material>` elements, and RViz drew the meshes in red, as in the '
        'student\'s own screenshot.' % (c('d_qos'), c('prep')))
    r.body(
        'RViz is a visualisation tool and not a simulator. It draws the pose implied by TF; it computes '
        'no forces, gravity, contacts or motor dynamics, and a slider moves the drawn model instantly '
        'whether or not a real arm could follow. Physical simulation is the task of Gazebo, which the '
        'course introduces with the optional `gazebo.launch.py`; its Time panel is mainly useful "when '
        'running in a simulator" %s. The notes contain a historical RViz screenshot of the complete '
        'model, produced with `ros2 launch urdf_tutorial display.launch.py model:=…/arduinobot.urdf.xacro` '
        'on 3 July 2026 by the VM clock ({ref:fig-hist}) %s. It shows that the student\'s own model loaded '
        'with all meshes; it used the urdf_tutorial launch file rather than the instructor\'s '
        '`display.launch.py`, and joint movement is not documented. The conceptual RViz lesson in 1.5 '
        'contains no practical run %s.' % (c('d_rviz'), c('n14'), c('n15')))
    r.figure_pair(
        (os.path.join(FIG, 'fig10_rviz_late_join.png'), 'fig-latejoin',
         'Preparation run: RViz started 8 s after robot_state_publisher; joint_1 = −0.5, joint_2 = 0.3, '
         'joint_3 = −0.4, joint_4 = −0.6 (gripper open).', 7.6,
         'Genuine screenshot of the delivered workspace (category C), 28 Sep. 2026.'),
        (os.path.join(FIG, 'fig11_notes_rviz_historical.png'), 'fig-hist',
         'Historical screenshot from the student\'s notes: the student\'s model in RViz '
         '(urdf_tutorial configuration).', 7.6,
         'Extracted from 1.4.docx, lesson 32, p79, IMG055 (category A, historical evidence; not a test '
         'of the delivered workspace).'))


def parameters(r, c):
    r.heading('ROS 2 Parameters', 1)
    r.heading('Concept', 2)
    r.body(
        'Parameters "are associated with individual nodes" and configure them "at startup (and during '
        'runtime), without changing the code"; each consists of a key, a typed value and a descriptor %s. '
        'There is no global parameter server: each node maintains its own parameters %s and exposes '
        'parameter services through which `ros2 param` lists, reads and sets them %s. A node must '
        'normally declare the parameters it accepts, and by default "attempts to change the type of a '
        'declared parameter at runtime will fail" %s. A node can also register a "set parameter" callback '
        'whose purpose is "to inspect the upcoming change … and explicitly reject the change"; such '
        'callbacks should have no side effects %s. The notes record the concept, including the per-node '
        'nature of parameters (1.5, lesson 35) %s.' % (c('d_params'), c('d_uparams'), c('d_params'),
                                                      c('d_params'), c('d_params'), c('n15')))
    r.heading('The example and its correction', 2)
    r.body(
        'The `simple_parameter` node declares `simple_int_param` (default 28) and `simple_string_param` '
        '(default "Antonio") and registers `paramChangeCallback` ({ref:lst-param}). The instructor\'s '
        'callback started from a default `SetParametersResult`, whose `successful` field is false, and '
        'set it to true only when one of its own parameters appeared. Two consequences were reproduced '
        'on the unmodified code: `ros2 param set /simple_parameter use_sim_time true` was rejected, although '
        '`use_sim_time` is a standard parameter of every node %s; and the same change was accepted when '
        'sent together with a valid `simple_int_param` in one atomic request %s. The delivered callback '
        'first validates the whole request, rejects it with a reason if one of the node\'s parameters '
        'has the wrong type, accepts parameters it does not manage and only then logs the changes. In '
        'Humble, rclpy enforces the declared type before calling the callback, so the callback\'s own type '
        'check is a second line of defence; this is stated in the code and exercised by a unit test. '
        'The same correction was applied to the C++ node.' % (c('d_uparams'), c('prep')))
    r.code(excerpt('arduinobot_py_examples/arduinobot_py_examples/simple_parameter.py',
                   'def __init__(self):', 'return SetParametersResult(successful=True)'),
           'lst-param', 'Parameter declaration and set-parameter callback '
           '(`arduinobot_py_examples/simple_parameter.py`, delivered version; category C correction of '
           'instructor code).')
    r.table(
        ['Request (Python node, test container)', 'Result'],
        [
            ['`ros2 param get … simple_int_param` / `simple_string_param`', '28 / "Antonio" (defaults)'],
            ['`ros2 param set … simple_int_param 30`, `… simple_string_param "ROS 2"`',
             'successful; node logs both changes'],
            ['`ros2 param set … simple_int_param hello`',
             'rejected: "Wrong parameter type, expected \'Type.INTEGER\' got \'Type.STRING\'"'],
            ['`ros2 param set … use_sim_time true`', 'successful (rejected by the original callback)'],
            ['atomic request: `simple_int_param = 5` with an integer for `simple_string_param`',
             'rejected as a whole; values stay 30 and "ROS 2"'],
            ['start-up override `--ros-args -p simple_int_param:=42`', 'value 42'],
            ['`colcon test` (6 parameter unit tests, flake8, pep257)', 'passed'],
        ],
        'tab-params', 'Parameter behaviour of the delivered Python node '
        '(`verification/logs/run_2026-09-28/30_parameters.log`, `10_build.log`).', [8.6, 7.4], font_size=9)
    r.heading('Boundary between the notes and this preparation', 2)
    r.body(
        'The Python parameter laboratory is only partly documented. The notes show the creation of an '
        'empty `simple_parameter.py` in the student\'s workspace and a full listing of the node with the '
        'instructor\'s names and defaults (1.5, lesson 36, p7–p10) %s. The listing is unindented as '
        'stored in the document and logs the string parameter with `%%d`, which – once re-indented – '
        'would raise a `TypeError` when that parameter is set; the delivered code uses `%%s`, as the instructor\'s file does. No '
        'entry-point registration, rebuild, run or `ros2 param` output is documented, and no C++ parameter '
        'lesson appears in the notes. The runnable parameter demonstration and its results therefore '
        'belong to category C, and completing the laboratory on the student\'s machine is future work.'
        % c('n15'))


def case_study(r, c):
    r.heading('3-DOF Manipulator Case Study', 1)
    r.heading('Robot and package responsibilities', 2)
    r.body(
        'The course robot is a 3D-printable desktop arm with three joints – base, shoulder and elbow – '
        'plus a gripper, driven by four hobby servo motors ("typically 4 × SG90") through an Arduino '
        'board (1.1 Course Notes, lesson 5, p5–p7) %s. In software the robot is represented by the '
        'arduinobot_description package; the two example packages teach the communication and '
        'configuration mechanisms that later course sections use to control it. Responsibilities are '
        'deliberately separated: the description package contains no program code, only the model, '
        'its meshes, a launch file and an RViz configuration, while all running programs in the '
        'visualisation are generic Humble nodes.' % c('n11'))
    r.heading('Implementation choices', 2)
    r.bullets([
        '**Baseline.** Section 4 on `main` (commit 4936385) is the smallest snapshot with all three '
        'packages, and its model does not depend on the control package, unlike Sections 5–9 %s. Branch '
        '`gz-classic` targets Gazebo Classic, whereas the notes record the installation of the '
        'modern-Gazebo packages `ros-humble-ros-gz*` (1.2, lesson 14) %s.' % (c('repo', 'prep'), c('repo_gzc', 'n12')),
        '**Minimal corrections.** Twelve changes (C1–C12) were made; the robot model, meshes, topic, message '
        'type, node names and defaults are unchanged. {ref:tab-changes} summarises them; the full diff is '
        'delivered in `patches/`.',
        '**Joint-state source.** A `gui` launch argument selects exactly one of joint_state_publisher_gui '
        '(default) and joint_state_publisher, so the pipeline can run without a slider window and two '
        'conflicting `/joint_states` publishers cannot be started together.',
        '**No combined launch file.** Messaging and visualisation are independent; combining them would '
        'couple the example and description packages without demonstrating anything new.',
        '**Simulation kept optional.** `gazebo.launch.py` was kept as instructor material with formatting '
        'fixes only. It was not executed, and on Humble its use of `GZ_SIM_RESOURCE_PATH` must be '
        'checked against the installed Gazebo Fortress version %s.' % c('prep'),
    ])
    r.table(
        ['ID', 'Change (category C)', 'Reason'],
        [
            ['C1', 'timer period `1.0 / frequency_`; log "%.1f Hz"', 'create_timer expects a period in seconds'],
            ['C2', 'clean Ctrl+C handling in the three Python nodes', 'tracebacks and "exited with failure" on shutdown'],
            ['C3', 'subscriber variable name, no-op statement removed', 'readability'],
            ['C4–C5', 'parameter callback validates the whole request; unmanaged parameters accepted (Python, C++)',
             '`use_sim_time` rejected; inconsistent batch results'],
            ['C6', 'six pytest cases for the parameter contract', 'guard the corrected behaviour'],
            ['C7', 'flake8 style fixes in the Python package', 'package\'s own linter test failed'],
            ['C8', '`gui` launch argument (default unchanged)', 'headless runs; single joint-state source'],
            ['C9', '`display.rviz`: stale `tool_link` removed, description QoS "Transient Local"',
             'link absent from model; configuration states the QoS used'],
            ['C10', 'direct exec dependencies declared (launch, launch_ros, ament_index_python, joint_state_publisher)',
             'imports and C8'],
            ['C11–C12', 'copyright linter skipped (no per-file headers); lint-only fixes in `gazebo.launch.py`',
             'linter failures; launch logic unchanged'],
        ],
        'tab-changes', 'Changes made to the instructor snapshot (details in `docs/PROVENANCE.md`).',
        [1.4, 8.4, 6.2], font_size=9)
    r.heading('Demonstration workflow', 2)
    r.body(
        'After building and sourcing the workspace, the demonstration consists of four independent '
        'steps, each documented with exact commands in the README: (1) Python publisher with C++ '
        'subscriber, (2) C++ publisher with Python subscriber, (3) the parameter node inspected and '
        'updated with `ros2 param`, and (4) `ros2 launch arduinobot_description display.launch.py`, '
        'moving the sliders and inspecting `/joint_states` and TF. {ref:lst-launch} shows the part of '
        'the launch file that loads the model and selects the joint-state source.')
    r.code(excerpt('arduinobot_description/launch/display.launch.py',
                   'robot_description = ParameterValue', 'condition=UnlessCondition'),
           'lst-launch', 'Model loading and joint-state source selection '
           '(`arduinobot_description/launch/display.launch.py`; the `gui` condition is a category C addition).')
    r.heading('Hardware context', 2)
    r.body(
        'The physical robot was not built or used in this preparation, and the notes contain no '
        'evidence of assembly, wiring or firmware upload. The repository\'s later sections state the '
        'following facts, which are reported only as file contents: the Arduino sketch attaches the base, '
        'shoulder, elbow and gripper servos to pins 8, 9, 10 and 11 and opens the serial port at 115 200 '
        'baud (`Section9_Build/…/robot_control.ino`); the ros2_control hardware interface sends frames '
        'of the form `b%%03d,s%%03d,e%%03d,g%%03d,` to `/dev/ttyACM0` %s. No file specifies the board '
        'model, wiring, supply voltage or power arrangement, so none is stated here.' % c('repo'))


def workflow(r, c):
    r.heading('Development Workflow', 1)
    r.body(
        'The work followed the cycle in {ref:fig-flow}: inspect the sources, prepare the packages, '
        'resolve dependencies, build, source, run, inspect and document, returning to preparation when '
        'a check revealed a defect. Every check was scripted (`verification/scripts/`), so that it can '
        'be repeated on the target machine and its output kept as evidence.')
    r.figure(os.path.join(FIG, 'fig06_workflow.png'), 'fig-flow',
             'Development and verification workflow.', width_cm=13.5,
             attribution='New diagram (category C).')
    r.body(
        'The preparation environment was a cloud container running Ubuntu 24.04, not the target system. '
        'The ROS 2 checks were therefore run inside the official `osrf/ros:humble-desktop` Docker image '
        '(Ubuntu 22.04.5, rclcpp 16.0.19, rclpy 3.3.21, rviz2 11.2.28). Because the network policy blocked '
        '`packages.ros.org`, xacro 2.1.1 and joint_state_publisher 2.4.0 – the versions the notes show '
        'being installed with apt – were built from their upstream release tags in a separate underlay. '
        'RViz ran on a virtual X server with software OpenGL %s.' % c('prep'))
    r.table(
        ['Check', 'Method', 'Status'],
        [
            ['Layout, manifests, launch/Xacro syntax, portable paths', 'static inspection, xacro, check_urdf', 'passed (static)'],
            ['package.xml schema (format 3)', 'xmllint with the REP 149 schema', 'passed (static)'],
            ['Build of all three packages', '`colcon build --symlink-install`', 'passed (build)'],
            ['Package tests (linters, 6 parameter tests)', '`colcon test`; xmllint could not download its schema',
             'passed except xmllint (blocked by environment)'],
            ['Python → C++ and C++ → Python on `/chatter`', '`ros2 run`, `ros2 topic list/info/echo/hz`', 'passed (runtime)'],
            ['Parameters (Python and C++)', '`ros2 param`, atomic service call', 'passed (runtime)'],
            ['Model tree, joints, mimic, 14 mesh URIs', '`check_model.py`, `check_urdf`', 'passed (static)'],
            ['Joint states, TF, static TF', '`ros2 topic echo/hz`, `tf2_echo`, `view_frames`', 'passed (runtime)'],
            ['RViz display, late join, clean shutdown', '`display.launch.py` under Xvfb, screenshots', 'passed (runtime, software rendering)'],
            ['Gazebo launch, ros2_control, MoveIt, hardware', '–', 'not tested'],
        ],
        'tab-verif', 'Verification summary (details and logs in `docs/VERIFICATION.md`).',
        [6.0, 6.5, 3.5], font_size=9)
    r.body(
        'Typical problems met during the work: a terminal without `source install/setup.bash` does not '
        'find the packages; CLI tools started with `--no-daemon` sometimes listed no nodes before '
        'discovery finished (`--spin-time 5` fixed this); `ros2 topic echo /tf_static` waited until its '
        'QoS was set to reliable and transient local like the publisher; and on Ctrl+C launch reports '
        'joint_state_publisher_gui as "died" (exit code −2), an upstream behaviour, while '
        'robot_state_publisher and RViz finish cleanly %s.' % c('prep'))


def advantages(r, c):
    r.heading('Advantages of ROS 2', 1)
    r.body('The project demonstrates several advantages directly:')
    r.bullets([
        '**Language interoperability.** Python and C++ nodes exchanged messages in both directions without '
        'conversion code, because both client libraries use generated interface code and a common core %s.'
        % c('d_clientlib'),
        '**Reuse of generic components.** robot_state_publisher, joint_state_publisher and RViz visualised '
        'a robot they know nothing about, driven only by its URDF %s.' % c('d_urdf_move'),
        '**Introspection.** The running graph, topic types, QoS, parameters and transforms could be '
        'inspected with standard tools, which made every verification step observable.',
        '**Configuration without recompilation.** Parameters changed node behaviour at start-up and at run '
        'time, and launch arguments selected the joint-state source.',
        '**Reproducible builds.** Declared dependencies, colcon and rosdep allowed the same workspace to be '
        'built from source in a clean container %s.' % c('d_rosdep'),
    ])
    r.body(
        'The same project also shows practical limitations. The environment must be sourced correctly in '
        'every terminal; discovery and QoS compatibility introduce timing effects that beginners do not '
        'expect; and the ecosystem moves quickly – the course repository already contains two Gazebo '
        'generations, renamed plug-ins and environment variables, and Humble reaches end of life in '
        'May 2027 %s. ROS 2 does not by itself make an application real-time, secure or compatible with '
        'arbitrary hardware: real-time behaviour needs a suitable kernel and deterministic code %s, '
        'security must be enabled and configured %s, and hardware support requires a driver or '
        'ros2_control interface such as the one the course writes for its Arduino.'
        % (c('d_distros'), c('d_realtime'), c('d_security')))


def status(r, c):
    r.heading('Current Project Status and Future Work', 1)
    r.heading('Status by category', 2)
    r.table(
        ['Category', 'Status'],
        [
            ['A – Documented student work',
             'ROS 2 Humble and tools installed; development environment configured; workspace and both '
             'example packages created; Python and C++ publishers and subscribers built and run; topic '
             'inspection; both cross-language directions; description package and complete URDF/Xacro '
             'model visualised in RViz with urdf_tutorial; conceptual study of ROS 2 architecture, '
             'communication, packages, RViz and parameters; Python parameter lab started (code listing '
             'only). Sources: notes 1.1–1.5 %s.' % c('n11', 'n12', 'n13', 'n14', 'n15')],
            ['B – Instructor material',
             'Section 4 packages (examples, parameter nodes, model, meshes, launch and RViz files), later '
             'sections with ros2_control, MoveIt 2, application, Alexa and firmware %s.' % c('repo')],
            ['C – Assignment preparation',
             'Clean workspace with corrections C1–C12; build, tests and runtime checks in an Ubuntu 22.04 / '
             'Humble container; parameter demonstration; TF and RViz verification; figures, documentation '
             'and this report %s.' % c('prep')],
            ['D – Future work (not documented in the notes)',
             'Completing the Python parameter lab; C++ parameters; practical services and actions; the '
             'instructor\'s display launch on the student\'s machine; Gazebo simulation; ros2_control; '
             'MoveIt 2; the application and Alexa integration; building and wiring the physical robot.'],
        ],
        'tab-status', 'Project status by category.', [3.6, 12.4], font_size=9)
    r.heading('Checks outstanding on the target machine', 2)
    r.body(
        'The preparation verified the project in a container that uses the target distribution but not the '
        'student\'s machine. The following remain to be run on Ubuntu 22.04 with Humble installed from apt, '
        'using the commands in the README and `verification/scripts/`:')
    r.bullets([
        '`rosdep install` and `colcon build --symlink-install` in `~/arduinobot_ws`, and `colcon test` '
        'with network access (so that the xmllint test can download its schema);',
        'the two cross-language runs and the parameter commands in separate terminals;',
        '`display.launch.py` with a real display and hardware-accelerated graphics, including moving the '
        'sliders and observing the mimic finger;',
        'optionally `gazebo.launch.py`, checking whether the meshes resolve with the installed Gazebo '
        'Fortress version.',
    ])
    r.heading('Future work', 2)
    r.body(
        'The natural continuation follows the course: completing and running the parameter laboratory, '
        'then services and actions, simulation in Gazebo, ros2_control controllers, MoveIt 2 motion '
        'planning, the task server and voice interface, and finally the physical robot. Two technical '
        'extensions follow from this report: a real-scale model (mesh scale 0.001 with all origins '
        'divided by ten) together with inertial values computed from the meshes, and a migration plan to '
        'a supported distribution before Humble\'s end of life in May 2027 %s.' % c('d_distros'))


def conclusion(r, c):
    r.heading('Conclusion', 1)
    r.body(
        'ROS 2 is a framework of libraries and tools that runs on top of an operating system and organises '
        'robot software as a graph of nodes communicating through typed topics, services and actions over '
        'a DDS-based middleware, configured through parameters and launch files. The arduinobot project '
        'made each of these concepts concrete: two small programs in different languages communicating '
        'over `/chatter`, a parameter node whose update rules had to be corrected, a workspace with three '
        'packages, and a URDF model that generic Humble nodes turn into coordinate frames and a 3D view.')
    r.body(
        'The notes document the work up to a complete robot model visualised in RViz; the parameter '
        'laboratory and later course stages are not documented as completed. The prepared workspace keeps '
        'the instructor\'s robot model, adds twelve documented corrections and was built and exercised in '
        'an Ubuntu 22.04 / ROS 2 Humble container; the student\'s own machine, simulation, control, motion '
        'planning and hardware remain to be verified, and the model is a ten-times-scaled kinematic '
        'description with placeholder dynamics. Within these limits, the project shows that ROS 2\'s value lies less in any single '
        'feature than in the combination of standard interfaces, reusable components and inspection tools '
        'that allowed every step to be checked.')


def references(r, cite_order, refs):
    r.heading('References', 1, numbered=False)
    r.para('Pages of the ROS 2 Humble documentation were read from the documentation source repository '
           '(ros2/ros2_documentation, branch humble, commit 35b00f1f3c1ab7c14bf85e35fa895f9f580ea279, '
           'inspected 28 Sep. 2026) because docs.ros.org was not reachable from the preparation '
           'environment; the URLs are those at which the same pages are published. References [1]–[5] '
           'are evidence of the student\'s course progress; the others support the technical content.',
           size=9, align='justify')
    for n, key in enumerate(cite_order, 1):
        p = r.para('[%d]\t%s' % (n, refs[key]), size=9, space_after=0)
        pf = p.paragraph_format
        from docx.shared import Cm
        pf.left_indent = Cm(1.0)
        pf.first_line_indent = Cm(-1.0)
        pf.line_spacing = 1.0
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT


SECTIONS = [introduction, what_is_ros2, why_ros2, architecture, nodes, pubsub, workspaces, urdf, tf,
            rviz, parameters, case_study, workflow, advantages, status, conclusion]
