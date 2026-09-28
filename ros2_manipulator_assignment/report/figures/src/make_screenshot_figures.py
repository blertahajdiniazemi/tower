#!/usr/bin/env python3
"""Figures made from genuine artefacts (no drawing, only cropping/composition).

Usage: make_screenshot_figures.py <verification run dir>
  fig07_tf_frames.png            TF tree from the view_frames .gv of the run, edge labels reduced
                                 to the recorded rate (fig07_tf_frames_raw.png: unmodified PDF)
  fig09_rviz_display_launch.png  RViz window + joint_state_publisher_gui window of the same
                                 display.launch.py session, placed side by side
  fig10_rviz_late_join.png       RViz window of the late-join / posed run
  fig11_notes_rviz_historical.png  image IMG055 extracted unchanged from the student's notes
                                   (1.4.docx, lesson 32, p79)
"""
import glob
import os
import shutil
import subprocess
import sys

from PIL import Image

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(SRC)
run = sys.argv[1]

pdf = sorted(glob.glob(os.path.join(run, 'frames_*.pdf')))[-1]
# unmodified rasterisation of the view_frames PDF (kept for reference)
subprocess.run(['pdftoppm', '-r', '160', '-png', '-singlefile', pdf,
                os.path.join(OUT, 'fig07_tf_frames_raw')], check=True)
# readable version used in the report: same frames and edges, labels reduced to the rate
subprocess.run([sys.executable, os.path.join(SRC, 'frames_figure.py'), pdf[:-4] + '.gv',
                os.path.join(OUT, 'fig07_tf_frames.png')], check=True)
os.replace(os.path.join(OUT, 'fig07_tf_frames.dot'), os.path.join(SRC, 'fig07_tf_frames.dot'))

rviz = Image.open(os.path.join(run, '50_display_launch_rviz.png')).convert('RGB')
jsp = Image.open(os.path.join(run, '50_display_launch_jsp_gui.png')).convert('RGB')
gap = 24
canvas = Image.new('RGB', (rviz.width + gap + jsp.width, max(rviz.height, jsp.height)), 'white')
canvas.paste(rviz, (0, 0))
canvas.paste(jsp, (rviz.width + gap, 0))
canvas.save(os.path.join(OUT, 'fig09_rviz_display_launch.png'))

Image.open(os.path.join(run, '50_late_join_posed_rviz.png')).convert('RGB').save(
    os.path.join(OUT, 'fig10_rviz_late_join.png'))

shutil.copyfile(os.path.join(SRC, 'notes_1.4_lesson32_p79_IMG055.png'),
                os.path.join(OUT, 'fig11_notes_rviz_historical.png'))
print('done')
