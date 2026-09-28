#!/usr/bin/env python3
"""Offline render of the arduinobot model (not an RViz screenshot).

Places the instructor's STL meshes with the kinematics of the expanded URDF
(joint origins, axes, visual origins and mesh scale) and draws them with
matplotlib, one colour per link.

Usage: render_model.py <expanded.urdf> <meshes_dir> <out.png> [joint=value ...]
"""
import os
import struct
import sys
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402
import numpy as np  # noqa: E402

COLOURS = {
    'base_link': '#4c6a92', 'base_plate': '#6f8fb8', 'forward_drive_arm': '#c9793b',
    'horizontal_arm': '#d9a441', 'claw_support': '#5b8c5a', 'gripper_right': '#9b5d8c',
    'gripper_left': '#b77fa9',
}


def rpy_matrix(r, p, y):
    cr, sr, cp, sp, cy, sy = np.cos(r), np.sin(r), np.cos(p), np.sin(p), np.cos(y), np.sin(y)
    rx = np.array([[1, 0, 0], [0, cr, -sr], [0, sr, cr]])
    ry = np.array([[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]])
    rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]])
    return rz @ ry @ rx


def axis_angle(axis, q):
    a = np.asarray(axis, float) / np.linalg.norm(axis)
    k = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(q) * k + (1 - np.cos(q)) * k @ k


def homog(rot, xyz):
    t = np.eye(4)
    t[:3, :3] = rot
    t[:3, 3] = xyz
    return t


def vec(text, default='0 0 0'):
    return np.array([float(v) for v in (text if text else default).split()])


def read_stl(path):
    data = open(path, 'rb').read()
    n = struct.unpack('<I', data[80:84])[0]
    rec = np.frombuffer(data[84:84 + 50 * n], dtype=np.dtype([
        ('n', '<f4', 3), ('v', '<f4', (3, 3)), ('attr', '<u2')]))
    return rec['v'].astype(float)


def main():
    urdf, mesh_dir, out = sys.argv[1:4]
    q = {k: float(v) for k, v in (a.split('=') for a in sys.argv[4:])}
    root = ET.parse(urdf).getroot()
    joints = {}
    for j in root.findall('joint'):
        joints[j.find('child').get('link')] = j
    by_name = {j.get('name'): j for j in root.findall('joint')}

    def position(jname):
        j = by_name[jname]
        m = j.find('mimic')
        if m is not None:
            return float(m.get('multiplier', 1)) * position(m.get('joint')) + float(m.get('offset', 0))
        return q.get(jname, 0.0)

    def link_pose(link):
        if link not in joints:
            return np.eye(4)
        j = joints[link]
        o = j.find('origin')
        t = homog(rpy_matrix(*vec(o.get('rpy') if o is not None else None)),
                  vec(o.get('xyz') if o is not None else None))
        if j.get('type') in ('revolute', 'continuous'):
            t = t @ homog(axis_angle(vec(j.find('axis').get('xyz')), position(j.get('name'))), [0, 0, 0])
        return link_pose(j.find('parent').get('link')) @ t

    fig = plt.figure(figsize=(4.4, 5.0), dpi=250)
    ax = fig.add_subplot(111, projection='3d')
    allpts = []
    handles = []
    for link in root.findall('link'):
        vis = link.find('visual')
        if vis is None:
            continue
        mesh = vis.find('geometry/mesh')
        name = link.get('name')
        tris = read_stl(os.path.join(mesh_dir, os.path.basename(mesh.get('filename'))))
        tris = tris * vec(mesh.get('scale'), '1 1 1')
        o = vis.find('origin')
        tv = link_pose(name) @ homog(rpy_matrix(*vec(o.get('rpy') if o is not None else None)),
                                     vec(o.get('xyz') if o is not None else None))
        pts = tris.reshape(-1, 3) @ tv[:3, :3].T + tv[:3, 3]
        tris_w = pts.reshape(-1, 3, 3)
        # light shading from the triangle normals
        nrm = np.cross(tris_w[:, 1] - tris_w[:, 0], tris_w[:, 2] - tris_w[:, 0])
        nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-12
        shade = 0.55 + 0.45 * np.abs(nrm @ np.array([0.4, -0.5, 0.75]) / 1.03)
        base = np.array(matplotlib.colors.to_rgb(COLOURS.get(name, '#888888')))
        cols = np.clip(base[None, :] * shade[:, None], 0, 1)
        pc = Poly3DCollection(tris_w, facecolors=cols, edgecolors='none', linewidths=0)
        ax.add_collection3d(pc)
        allpts.append(pts)
        handles.append(plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=base,
                                  markersize=9, label=name))
    pts = np.vstack(allpts)
    centre = (pts.max(0) + pts.min(0)) / 2
    half = (pts.max(0) - pts.min(0)).max() / 2
    ax.set_xlim(centre[0] - half, centre[0] + half)
    ax.set_ylim(centre[1] - half, centre[1] + half)
    ax.set_zlim(max(0, centre[2] - half), centre[2] + half)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=22, azim=-35)
    ax.set_axis_off()
    ax.legend(handles=handles, loc='upper left', fontsize=10, frameon=False,
              handletextpad=0.2, borderaxespad=0.0, bbox_to_anchor=(0.0, 1.02))
    height = pts[:, 2].max() - pts[:, 2].min()
    ax.text2D(0.98, 0.02, 'height %.2f model m' % height, transform=ax.transAxes, ha='right',
              fontsize=10, color='#333333')
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.savefig(out, dpi=250, bbox_inches='tight', pad_inches=0.02)
    print('wrote', out, 'extent', pts.min(0).round(3), pts.max(0).round(3))


if __name__ == '__main__':
    main()
