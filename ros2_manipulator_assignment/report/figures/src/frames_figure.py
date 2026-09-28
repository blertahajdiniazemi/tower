#!/usr/bin/env python3
"""Readable version of the TF tree recorded by `ros2 run tf2_tools view_frames`.

Reads the .gv file written by view_frames, keeps its frames and parent/child edges and
replaces each verbose edge label by the recorded average rate ("static" when view_frames
reports its placeholder rate 10000 with an empty buffer). No frame or edge is added or removed.
Usage: frames_figure.py <frames_*.gv> <out.png>
"""
import re
import subprocess
import sys

gv = open(sys.argv[1]).read()
edges = re.findall(r'"([^"]+)"\s*->\s*"([^"]+)"\[label="([^"]*)"\]', gv)
if not edges:
    sys.exit('no edges found in ' + sys.argv[1])
out = ['digraph frames {',
       '  graph [rankdir=TB, nodesep=0.3, ranksep=0.12, pad=0.1];',
       '  node [shape=ellipse, height=0.36, margin="0.12,0.02", fontname="Liberation Sans", fontsize=15, style=filled, '
       'fillcolor="#dbe7f3", color="#1f3b5a"];',
       '  edge [fontname="Liberation Sans", fontsize=13, color="#1f3b5a"];']
for parent, child, label in edges:
    rate = float(re.search(r'Average rate: ([0-9.]+)', label).group(1))
    buf = float(re.search(r'Buffer length: ([0-9.]+)', label).group(1))
    text = 'static (/tf_static)' if rate >= 10000 and buf == 0 else '%.1f Hz (/tf)' % rate
    style = 'style=dashed, color="#7a7a7a"' if text.startswith('static') else ''
    out.append('  "%s" -> "%s" [label=" %s", %s];' % (parent, child, text, style))
out.append('}')
dot = '\n'.join(out)
open(sys.argv[2].rsplit('.', 1)[0] + '.dot', 'w').write(dot + '\n')
subprocess.run(['dot', '-Tpng', '-Gdpi=250', '-o', sys.argv[2]], input=dot.encode(), check=True)
print('edges', len(edges))
