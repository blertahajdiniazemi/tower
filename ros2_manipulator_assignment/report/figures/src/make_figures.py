#!/usr/bin/env python3
"""Build the report figures from their editable sources.

Usage: make_figures.py <model_report.json> <expanded.urdf>
  model_report.json and expanded.urdf are produced by verification stage 40
  (verification/scripts/40_model_tf.sh). Outputs go to report/figures/.
Requires graphviz (dot) and matplotlib.
"""
import json
import os
import subprocess
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(SRC)
NAVY = '#1f3b5a'
plt.rcParams['font.family'] = 'Liberation Sans'


def dot(name):
    for fmt, extra in (('png', ['-Gdpi=250']), ('svg', [])):
        subprocess.run(['dot', '-T' + fmt, *extra, os.path.join(SRC, name + '.dot'),
                        '-o', os.path.join(OUT, name + '.' + fmt)], check=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + '.png'), dpi=250, bbox_inches='tight', pad_inches=0.08)
    fig.savefig(os.path.join(OUT, name + '.svg'), bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, ec=NAVY, fs=10, bold_first=True, ls='-'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.008,rounding_size=0.012',
                                fc=fc, ec=ec, lw=1.2, ls=ls))
    lines = text.split('\n')
    ax.text(x + w / 2, y + h / 2 + (0.012 * (len(lines) - 1)), lines[0], ha='center',
            va='center', fontsize=fs, weight='bold' if bold_first else 'normal', color='#10202f')
    for i, line in enumerate(lines[1:]):
        ax.text(x + w / 2, y + h / 2 + 0.012 * (len(lines) - 1) - 0.028 * (i + 1), line,
                ha='center', va='center', fontsize=fs - 1.5, color='#27394b')


def fig01_architecture():
    fig, ax = plt.subplots(figsize=(10, 6.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    left, width = 0.03, 0.70
    # application layer
    box(ax, left, 0.80, 0.225, 0.15, 'arduinobot_py_examples\nsimple_publisher\nsimple_subscriber\n'
        'simple_parameter', '#dbe7f3')
    box(ax, left + 0.2375, 0.80, 0.225, 0.15, 'arduinobot_cpp_examples\nsimple_publisher\n'
        'simple_subscriber\nsimple_parameter', '#e3efe0')
    box(ax, left + 0.475, 0.80, 0.225, 0.15, 'Humble packages used\nrobot_state_publisher (C++)\n'
        'joint_state_publisher(_gui) (Py)\nrviz2 (C++)', '#f2f2f2')
    ax.text(left - 0.012, 0.875, 'Nodes', rotation=90, va='center', ha='right', fontsize=10,
            color=NAVY, weight='bold')
    box(ax, left, 0.665, 0.34, 0.10, 'rclpy\nPython client library', '#dbe7f3')
    box(ax, left + 0.36, 0.665, 0.34, 0.10, 'rclcpp\nC++ client library', '#e3efe0')
    box(ax, left, 0.54, width, 0.09, 'rcl  (ROS client support library, C)\nnodes, publishers, '
        'subscriptions, timers, parameters, graph queries', '#eef2f6')
    box(ax, left, 0.415, width, 0.09, 'rmw  (ROS middleware interface)\nvendor-neutral API; '
        'implementation chosen with RMW_IMPLEMENTATION', '#eef2f6')
    box(ax, left, 0.29, width, 0.09, 'rmw_fastrtps_cpp  →  eProsima Fast DDS\nHumble default '
        '(verified in the test container); other DDS vendors possible', '#f6e3cf', ec='#b5651d')
    box(ax, left, 0.165, width, 0.09, 'DDS / RTPS wire protocol\ndiscovery, serialisation, '
        'QoS, transport over UDP/IP or shared memory', '#f6e3cf', ec='#b5651d')
    box(ax, left, 0.04, width, 0.09, 'Ubuntu 22.04 LTS (Linux kernel)\nprocesses, threads, '
        'sockets, file system: ROS 2 runs on top of the OS, it does not replace it', '#e6e6e6')
    for y in (0.765, 0.63, 0.505, 0.38, 0.255, 0.13):
        ax.annotate('', xy=(left + width / 2, y), xytext=(left + width / 2, y + 0.035),
                    arrowprops=dict(arrowstyle='<->', color='#6b7c8d', lw=1))
    # side panel
    sx = 0.77
    box(ax, sx, 0.54, 0.21, 0.41, 'Interfaces\nstd_msgs/msg/String\nsensor_msgs/msg/JointState\n'
        'tf2_msgs/msg/TFMessage\nrcl_interfaces (parameters)\n\nGraph concepts\nnodes · topics\n'
        'services · actions\nparameters', '#fbfbfb', fs=10)
    box(ax, sx, 0.165, 0.21, 0.34, 'Tools\nros2 CLI (run, launch,\ntopic, param, node)\n'
        'colcon (build, test)\nrosdep (dependencies)\nxacro · tf2_tools', '#fbfbfb', fs=10)
    ax.set_title('ROS 2 Humble software stack as used by the arduinobot workspace', fontsize=12,
                 color=NAVY, loc='left')
    save(fig, 'fig01_ros2_architecture')


def fig03_workspace():
    entries = [
        (0, 'arduinobot_ws/', 'colcon workspace (overlay)', 'b'),
        (1, 'src/', 'the only delivered sub-directory', 'b'),
        (2, 'arduinobot_py_examples/', 'ament_python', 'p'),
        (3, 'package.xml', 'rclpy, std_msgs, rcl_interfaces', ''),
        (3, 'setup.py, setup.cfg', 'console_scripts entry points', ''),
        (3, 'arduinobot_py_examples/*.py', 'simple_publisher / _subscriber / _parameter', ''),
        (3, 'test/', 'flake8, pep257, parameter tests', ''),
        (2, 'arduinobot_cpp_examples/', 'ament_cmake', 'c'),
        (3, 'package.xml, CMakeLists.txt', 'add_executable + install(TARGETS)', ''),
        (3, 'src/*.cpp', 'simple_publisher / _subscriber / _parameter', ''),
        (2, 'arduinobot_description/', 'ament_cmake (resources only)', 'd'),
        (3, 'urdf/arduinobot.urdf.xacro', 'robot model', ''),
        (3, 'meshes/*.STL', '13 instructor meshes (7 referenced)', ''),
        (3, 'launch/display.launch.py', 'RSP + joint states + RViz', ''),
        (3, 'launch/gazebo.launch.py', 'optional, ros_gz (not run here)', ''),
        (3, 'rviz/display.rviz', 'RViz configuration', ''),
        (1, 'build/  install/  log/', 'generated by colcon, not delivered', 'g'),
    ]
    colours = {'b': NAVY, 'p': '#2f6ea5', 'c': '#3d7a3a', 'd': '#8a5a1f', 'g': '#8a8a8a', '': '#10202f'}
    fig, ax = plt.subplots(figsize=(10, 6.2))
    ax.axis('off')
    n = len(entries)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, n)
    for i, (lvl, name, note, kind) in enumerate(entries):
        y = n - 1 - i
        x = 0.02 + lvl * 0.045
        if lvl:
            ax.plot([x - 0.03, x - 0.008], [y, y], color='#9aa9b8', lw=1)
            # vertical connector to the parent row
            parent = max(j for j in range(i) if entries[j][0] == lvl - 1)
            ax.plot([x - 0.03, x - 0.03], [n - 1 - parent - 0.35, y], color='#9aa9b8', lw=1)
        ax.text(x, y, name, va='center', fontsize=10.5, family='DejaVu Sans Mono',
                color=colours[kind], weight='bold' if kind else 'normal',
                style='italic' if kind == 'g' else 'normal')
        ax.text(0.60, y, note, va='center', fontsize=10, color='#8a8a8a' if kind == 'g' else '#27394b')
    ax.set_title('Delivered workspace layout (source tree only)', fontsize=12, color=NAVY, loc='left')
    fig.tight_layout()
    save(fig, 'fig03_workspace')


def fig05_urdf(model_json):
    m = json.load(open(model_json))
    lines = ['// Generated by make_figures.py from verification output model_report.json',
             'digraph urdf {',
             '  graph [rankdir=TB, fontname="Liberation Sans", nodesep=0.9, ranksep=0.32, pad=0.15];',
             '  node [fontname="Liberation Sans", fontsize=12, shape=box, style="rounded,filled", '
             'fillcolor="#dbe7f3", color="#1f3b5a", penwidth=1.2, width=2.0];',
             '  edge [fontname="Liberation Sans", fontsize=10, color="#1f3b5a", penwidth=1.3, '
             'arrowsize=0.7];']
    for link in m['links']:
        lines.append('  "%s" [label=<<b>%s</b>>];' % (link, link))

    def fmt(v):
        return ' '.join(('%g' % round(x, 3)) for x in v)
    for j in m['joints']:
        if j['type'] == 'fixed':
            label = ('<font color="#555555"><b>%s</b> (fixed)<br/>xyz %s</font>'
                     % (j['name'], fmt(j['xyz'])))
            attrs = 'style=dashed, color="#7a7a7a"'
        else:
            lim = j['limit']
            label = ('<b>%s</b> (%s)<br/>axis %s · xyz %s<br/>limits [%.2f, %.2f] rad'
                     % (j['name'], j['type'], fmt(j['axis']), fmt(j['xyz']),
                        lim['lower'], lim['upper']))
            if j['mimic']:
                label += ('<br/><font color="#9b3d2b"><b>mimic: %s × %g</b></font>'
                          % (j['mimic']['joint'], j['mimic']['multiplier']))
            attrs = 'color="#b5651d", penwidth=2.0'
        lines.append('  "%s" -> "%s" [%s, label=<%s>];' % (j['parent'], j['child'], attrs, label))
    lines.append('}')
    open(os.path.join(SRC, 'fig05_urdf_tree.dot'), 'w').write('\n'.join(lines) + '\n')
    dot('fig05_urdf_tree')


def fig06_workflow():
    steps = [
        ('1  Inspect sources', 'notes, instructor repo\n@4936385, Humble docs'),
        ('2  Prepare packages', 'copy Section 4 snapshot,\nminimal corrections'),
        ('3  Dependencies', 'package.xml declarations,\nrosdep check / install'),
        ('4  Build', 'colcon build\n--symlink-install'),
        ('5  Source', 'source install/setup.bash\n(overlay on /opt/ros/humble)'),
        ('6  Run / launch', 'ros2 run ...\nros2 launch ...'),
        ('7  Inspect / verify', 'ros2 topic, param, tf2_echo,\nRViz, colcon test'),
        ('8  Document', 'evidence, provenance,\nverification, report'),
    ]
    fig, ax = plt.subplots(figsize=(10, 3.9))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    w, h, gap = 0.215, 0.30, 0.03
    xs = [0.01 + i * (w + gap) for i in range(4)]
    ys = [0.62, 0.10]
    centres = []
    for i, (title, body) in enumerate(steps):
        x, y = xs[i % 4], ys[i // 4]
        fc = '#e3efe0' if i in (3, 4, 5) else '#dbe7f3'
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.006,rounding_size=0.02',
                                    fc=fc, ec=NAVY, lw=1.2))
        ax.text(x + w / 2, y + h * 0.70, title, ha='center', va='center', fontsize=11.5,
                weight='bold', color='#10202f')
        ax.text(x + w / 2, y + h * 0.33, body, ha='center', va='center', fontsize=9.5,
                color='#27394b', linespacing=1.3)
        centres.append((x, y))
    arrow = dict(arrowstyle='-|>', color=NAVY, lw=1.4, mutation_scale=14)
    for i in range(7):
        if i == 3:
            continue
        (x0, y0), (x1, y1) = centres[i], centres[i + 1]
        ax.annotate('', xy=(x1 - 0.004, y1 + h / 2), xytext=(x0 + w + 0.004, y0 + h / 2),
                    arrowprops=arrow)
    # wrap from step 4 (end of first row) to step 5 (start of second row)
    x4, y4 = centres[3]
    x5, y5 = centres[4]
    ax.plot([x4 + w / 2, x4 + w / 2, x5 + w / 2], [y4 - 0.01, 0.51, 0.51], color=NAVY, lw=1.4)
    ax.annotate('', xy=(x5 + w / 2, y5 + h + 0.008), xytext=(x5 + w / 2, 0.515), arrowprops=arrow)
    # feedback loop from step 7 back to step 2
    x7, y7 = centres[6]
    x2, y2 = centres[1]
    ax.annotate('', xy=(x2 + w * 0.8, y2 - 0.008), xytext=(x7 + w * 0.2, y7 + h + 0.008),
                arrowprops=dict(arrowstyle='-|>', color='#b5651d', lw=1.3, ls='--',
                                mutation_scale=14, connectionstyle='arc3,rad=-0.25'))
    ax.text(0.515, 0.455, 'defect found: fix, rebuild, re-test', ha='left', va='center',
            fontsize=9.5, color='#b5651d', style='italic')
    save(fig, 'fig06_workflow')


def main():
    model_json, urdf = sys.argv[1:3]
    fig01_architecture()
    dot('fig02_pubsub')
    fig03_workspace()
    dot('fig04_software_architecture')
    fig05_urdf(model_json)
    fig06_workflow()
    meshes = os.path.join(OUT, '..', '..', 'arduinobot_ws', 'src', 'arduinobot_description', 'meshes')
    subprocess.run([sys.executable, os.path.join(SRC, 'render_model.py'), urdf, meshes,
                    os.path.join(OUT, 'fig08_offline_render.png')], check=True)
    print('figures written to', OUT)


if __name__ == '__main__':
    main()
