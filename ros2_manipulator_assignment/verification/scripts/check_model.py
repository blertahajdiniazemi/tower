#!/usr/bin/env python3
"""Static checks of the expanded arduinobot URDF.

Usage: check_model.py <expanded.urdf> [<report.json>]

Run after sourcing the workspace so that package:// URIs can be resolved
through the ament index. Prints a human-readable report and exits non-zero
if a check fails.
"""
import json
import math
import os
import struct
import sys
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory

# Topology checklist taken from the assignment brief; it is compared with the
# model, never used to modify it.
EXPECTED_JOINTS = {
    'virtual_joint': ('fixed', 'world', 'base_link'),
    'joint_1': ('revolute', 'base_link', 'base_plate'),
    'joint_2': ('revolute', 'base_plate', 'forward_drive_arm'),
    'joint_3': ('revolute', 'forward_drive_arm', 'horizontal_arm'),
    'horizontal_arm_to_claw_support': ('fixed', 'horizontal_arm', 'claw_support'),
    'joint_4': ('revolute', 'claw_support', 'gripper_right'),
    'joint_5': ('revolute', 'claw_support', 'gripper_left'),
}

failures = []


def check(condition, message):
    print(('  PASS  ' if condition else '  FAIL  ') + message)
    if not condition:
        failures.append(message)


def vec(text, default='0 0 0'):
    return [float(v) for v in (text if text is not None else default).split()]


def stl_info(path):
    with open(path, 'rb') as f:
        data = f.read()
    count = struct.unpack('<I', data[80:84])[0]
    if len(data) == 84 + 50 * count:
        mins = [math.inf] * 3
        maxs = [-math.inf] * 3
        for i in range(count):
            off = 84 + 50 * i + 12
            for k in range(3):
                x, y, z = struct.unpack('<3f', data[off + 12 * k: off + 12 * k + 12])
                for axis, value in enumerate((x, y, z)):
                    mins[axis] = min(mins[axis], value)
                    maxs[axis] = max(maxs[axis], value)
        return {'format': 'binary', 'triangles': count, 'min': mins, 'max': maxs}
    return {'format': 'ascii-or-unknown', 'triangles': None, 'min': None, 'max': None}


def main():
    urdf_path = sys.argv[1]
    root = ET.parse(urdf_path).getroot()
    report = {'robot': root.get('name'), 'links': [], 'joints': [], 'meshes': []}

    links = [link.get('name') for link in root.findall('link')]
    joints = root.findall('joint')
    print('Robot name: %s' % root.get('name'))
    print('Links (%d): %s' % (len(links), ', '.join(links)))

    print('\nJoints:')
    children = {}
    parents = {}
    for j in joints:
        name, jtype = j.get('name'), j.get('type')
        parent, child = j.find('parent').get('link'), j.find('child').get('link')
        origin = j.find('origin')
        xyz = vec(origin.get('xyz') if origin is not None else None)
        rpy = vec(origin.get('rpy') if origin is not None else None)
        axis_el = j.find('axis')
        axis = vec(axis_el.get('xyz')) if axis_el is not None else None
        limit = j.find('limit')
        lim = None
        if limit is not None:
            lim = {k: float(limit.get(k)) for k in ('lower', 'upper', 'effort', 'velocity')
                   if limit.get(k) is not None}
        mimic = j.find('mimic')
        mim = None
        if mimic is not None:
            mim = {'joint': mimic.get('joint'),
                   'multiplier': float(mimic.get('multiplier', '1')),
                   'offset': float(mimic.get('offset', '0'))}
        report['joints'].append({'name': name, 'type': jtype, 'parent': parent, 'child': child,
                                 'xyz': xyz, 'rpy': rpy, 'axis': axis, 'limit': lim,
                                 'mimic': mim})
        print('  %-31s %-9s %-18s -> %-18s xyz=%s axis=%s limit=%s mimic=%s' % (
            name, jtype, parent, child, xyz, axis, lim, mim))
        children.setdefault(parent, []).append(child)
        parents.setdefault(child, []).append(parent)

    print('\nTree checks:')
    roots = [link for link in links if link not in parents]
    check(len(roots) == 1, 'single root link (found %s)' % roots)
    check(all(len(p) == 1 for p in parents.values()), 'every non-root link has exactly one parent')
    reached = set()
    stack = list(roots)
    while stack:
        link = stack.pop()
        reached.add(link)
        stack.extend(children.get(link, []))
    check(reached == set(links), 'all %d links reachable from the root' % len(links))

    print('\nChecklist comparison:')
    by_name = {j['name']: j for j in report['joints']}
    for name, (jtype, parent, child) in EXPECTED_JOINTS.items():
        j = by_name.get(name)
        check(j is not None and (j['type'], j['parent'], j['child']) == (jtype, parent, child),
              '%s is %s %s -> %s' % (name, jtype, parent, child))
    check(set(by_name) == set(EXPECTED_JOINTS), 'no joints beyond the checklist')
    for j in report['joints']:
        if j['type'] in ('revolute', 'prismatic'):
            check(j['limit'] is not None and j['axis'] is not None,
                  '%s has an axis and limits' % j['name'])
        if j['mimic']:
            check(j['mimic']['joint'] in by_name,
                  '%s mimics existing joint %s' % (j['name'], j['mimic']['joint']))
    movable = [j['name'] for j in report['joints'] if j['type'] != 'fixed']
    independent = [j['name'] for j in report['joints'] if j['type'] != 'fixed' and not j['mimic']]
    print('  INFO  non-fixed joints in URDF: %d %s' % (len(movable), movable))
    print('  INFO  independently commanded joints (non-mimic): %d %s' % (
        len(independent), independent))

    print('\nMesh resolution:')
    for link in root.findall('link'):
        for kind in ('visual', 'collision'):
            for el in link.findall(kind):
                mesh = el.find('geometry/mesh')
                if mesh is None:
                    continue
                uri = mesh.get('filename')
                scale = vec(mesh.get('scale'), '1 1 1')
                origin = el.find('origin')
                entry = {'link': link.get('name'), 'element': kind, 'uri': uri, 'scale': scale,
                         'origin_xyz': vec(origin.get('xyz') if origin is not None else None),
                         'origin_rpy': vec(origin.get('rpy') if origin is not None else None)}
                ok = uri.startswith('package://')
                if ok:
                    pkg, rel = uri[len('package://'):].split('/', 1)
                    path = os.path.join(get_package_share_directory(pkg), rel)
                    directory, base = os.path.split(path)
                    # exact-case check, independent of the file system
                    ok = os.path.isdir(directory) and base in os.listdir(directory)
                    entry['resolved'] = path
                    if ok and kind == 'visual':
                        info = stl_info(path)
                        entry['stl'] = info
                        if info['min'] is not None:
                            size = [(hi - lo) * s for lo, hi, s in
                                    zip(info['min'], info['max'], scale)]
                            entry['scaled_size_m'] = size
                check(ok, '%s %s -> %s' % (link.get('name'), kind, uri))
                report['meshes'].append(entry)

    print('\nVisual mesh sizes (file units x scale):')
    for m in report['meshes']:
        if m['element'] == 'visual' and 'stl' in m:
            s = m['stl']
            raw = [hi - lo for lo, hi in zip(s['min'], s['max'])]
            print('  %-18s %-24s %6d triangles, raw extent %s, scaled extent %s m' % (
                m['link'], os.path.basename(m['uri']), s['triangles'],
                ['%.1f' % v for v in raw], ['%.3f' % v for v in m['scaled_size_m']]))

    report['links'] = links
    report['failures'] = failures
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'w') as f:
            json.dump(report, f, indent=1)
    print('\nRESULT: %s (%d failure(s))' % ('PASS' if not failures else 'FAIL', len(failures)))
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
