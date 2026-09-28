"""Reference list (IEEE style). Numbers are assigned in order of first citation."""

DOCS = 'https://docs.ros.org/en/humble/'
DOCNOTE = ''  # the note on how the pages were inspected is printed once above the list


def doc(title, path):
    return '"%s," *ROS 2 Documentation: Humble*. [Online]. Available: %s%s' % (title, DOCS, path)


REFS = {
    # --- student's notes (evidence of documented progress)
    'n11': '[Student Name], "1.1 Course Notes," personal course notes for *Robotics and ROS 2 – '
           'Learn by Doing! Manipulators*, lessons 1, 4–6, Microsoft Word 97-2003 document, '
           'last saved 4 Jun. 2026 (file metadata), unpublished.',
    'n12': '[Student Name], "1.2 Course Notes," personal course notes, lessons 11, 14, 16–24, '
           'Microsoft Word 97-2003 document, last saved 6 Jun. 2026 (file metadata), unpublished.',
    'n13': '[Student Name], "1.3 Course Notes," personal course notes, lessons 25–27, Microsoft '
           'Word 97-2003 document, last saved 25 Jun. 2026 (file metadata), unpublished.',
    'n14': '[Student Name], "1.4," personal course notes, lessons 28–32, Microsoft Word (OOXML) '
           'document, last modified 9 Jul. 2026 (file metadata), unpublished.',
    'n15': '[Student Name], "1.5," personal course notes, lessons 34–36, Microsoft Word 97-2003 '
           'document, last saved 3 Aug. 2026 (file metadata), unpublished.',
    # --- instructor material
    'repo': 'A. Brandi, "Robotics-and-ROS-2-Learn-by-Doing-Manipulators," GitHub repository, '
            'branch main, commit 4936385347e477c59927382c904883c432c9b33d, retrieved 28 Sep. 2026. '
            '[Online]. Available: https://github.com/AntoBrandi/Robotics-and-ROS-2-Learn-by-Doing-Manipulators',
    'repo_gzc': 'A. Brandi, "Robotics-and-ROS-2-Learn-by-Doing-Manipulators," GitHub repository, '
                'branch gz-classic, commit 07440a5f771b6fcc6c6f4a0b2ff6d40e4eb6ccb2, retrieved '
                '28 Sep. 2026 (used for comparison only).',
    # --- assignment preparation material
    'prep': 'Assignment preparation material: workspace `arduinobot_ws`, `docs/` (provenance, '
            'course-progress evidence, repository audit, verification) and '
            '`verification/logs/run_2026-09-28`, delivered with this report.',
    # --- official documentation (inspected from the documentation source)
    'd_index': doc('ROS 2 Documentation', 'index.html'),
    'd_about': doc('About ROS', 'About-ROS.html'),
    'd_nodes': doc('Nodes', 'Concepts/Basic/About-Nodes.html'),
    'd_unodes': doc('Understanding nodes', 'Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html'),
    'd_clientlib': doc('Client libraries', 'Concepts/Basic/About-Client-Libraries.html'),
    'd_internal': doc('Internal ROS 2 interfaces', 'Concepts/Advanced/About-Internal-Interfaces.html'),
    'd_vendors': doc('Different ROS 2 middleware vendors', 'Concepts/Intermediate/About-Different-Middleware-Vendors.html'),
    'd_discovery': doc('Discovery', 'Concepts/Basic/About-Discovery.html'),
    'd_domain': doc('The ROS_DOMAIN_ID', 'Concepts/Intermediate/About-Domain-ID.html'),
    'd_interfaces': doc('Interfaces', 'Concepts/Basic/About-Interfaces.html'),
    'd_topics': doc('Topics', 'Concepts/Basic/About-Topics.html'),
    'd_utopics': doc('Understanding topics', 'Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html'),
    'd_services': doc('Services', 'Concepts/Basic/About-Services.html'),
    'd_actions': doc('Actions', 'Concepts/Basic/About-Actions.html'),
    'd_qos': doc('Quality of Service settings', 'Concepts/Intermediate/About-Quality-of-Service-Settings.html'),
    'd_executors': doc('Executors', 'Concepts/Intermediate/About-Executors.html'),
    'd_params': doc('Parameters', 'Concepts/Basic/About-Parameters.html'),
    'd_uparams': doc('Understanding parameters', 'Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html'),
    'd_pyparams': doc('Using parameters in a class (Python)', 'Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html'),
    'd_pypubsub': doc('Writing a simple publisher and subscriber (Python)', 'Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html'),
    'd_cpppubsub': doc('Writing a simple publisher and subscriber (C++)', 'Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html'),
    'd_workspace': doc('Creating a workspace', 'Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html'),
    'd_colcon': doc('Using colcon to build packages', 'Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html'),
    'd_package': doc('Creating a package', 'Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html'),
    'd_build': doc('The build system', 'Concepts/Advanced/About-Build-System.html'),
    'd_env': doc('Configuring environment', 'Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html'),
    'd_rosdep': doc('Managing dependencies with rosdep', 'Tutorials/Intermediate/Rosdep.html'),
    'd_launch': doc('Launch', 'Concepts/Basic/About-Launch.html'),
    'd_urdf': doc('URDF', 'Tutorials/Intermediate/URDF/URDF-Main.html'),
    'd_urdf_visual': doc('Building a visual robot model from scratch', 'Tutorials/Intermediate/URDF/Building-a-Visual-Robot-Model-with-URDF-from-Scratch.html'),
    'd_urdf_move': doc('Building a movable robot model', 'Tutorials/Intermediate/URDF/Building-a-Movable-Robot-Model-with-URDF.html'),
    'd_urdf_phys': doc('Adding physical and collision properties', 'Tutorials/Intermediate/URDF/Adding-Physical-and-Collision-Properties-to-a-URDF-Model.html'),
    'd_xacro': doc('Using Xacro to clean up your code', 'Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html'),
    'd_rsp': doc('Using URDF with robot_state_publisher (Python)', 'Tutorials/Intermediate/URDF/Using-URDF-with-Robot-State-Publisher-py.html'),
    'd_tf2': doc('Tf2', 'Concepts/Intermediate/About-Tf2.html'),
    'd_tf2intro': doc('Introducing tf2', 'Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html'),
    'd_rviz': doc('RViz User Guide', 'Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html'),
    'd_security': doc('ROS 2 Security', 'Concepts/Intermediate/About-Security.html'),
    'd_realtime': doc('Understanding real-time programming', 'Tutorials/Demos/Real-Time-Programming.html'),
    'd_install': doc('Ubuntu (deb packages)', 'Installation/Ubuntu-Install-Debs.html'),
    'd_humble': doc('Humble Hawksbill (humble)', 'Releases/Release-Humble-Hawksbill.html'),
    'd_distros': doc('Distributions', 'Releases.html'),
}
