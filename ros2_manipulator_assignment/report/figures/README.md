# Report figures

PNG files are the versions embedded in the Word report; SVG files are vector exports of the
generated diagrams. Editable sources are in `src/`.

| File | Content | Kind | Source / how to regenerate |
|---|---|---|---|
| `fig01_ros2_architecture.png/.svg` | ROS 2 Humble stack with the project's nodes | new diagram (C) | `src/make_figures.py` (matplotlib) |
| `fig02_pubsub.png/.svg` | publisher → `/chatter` → subscriber, both language directions | new diagram (C) | `src/fig02_pubsub.dot` (Graphviz) |
| `fig03_workspace.png/.svg` | delivered workspace layout | new figure (C) | `src/make_figures.py` |
| `fig04_software_architecture.png/.svg` | description → robot_state_publisher → TF → RViz; optional parts dashed | new diagram (C) | `src/fig04_software_architecture.dot` |
| `fig05_urdf_tree.png/.svg` | link–joint tree generated from the verified model | generated (C) | `src/make_figures.py` writes `src/fig05_urdf_tree.dot` from `model_report.json` |
| `fig06_workflow.png/.svg` | development and verification workflow | new diagram (C) | `src/make_figures.py` |
| `fig07_tf_frames.png` | TF tree recorded by `ros2 run tf2_tools view_frames` | genuine runtime output (C) | `src/make_screenshot_figures.py` from `verification/logs/run_2026-09-28/frames_*.pdf` |
| `fig08_offline_render.png` | instructor meshes placed with the URDF kinematics | offline render (C), not an RViz test | `src/render_model.py` |
| `fig09_rviz_display_launch.png` | RViz + joint_state_publisher_gui windows of `display.launch.py` | genuine screenshots (C), composed side by side | `src/make_screenshot_figures.py` |
| `fig10_rviz_late_join.png` | RViz started 8 s after robot_state_publisher, posed model | genuine screenshot (C) | `src/make_screenshot_figures.py` |
| `fig11_notes_rviz_historical.png` | the student's model in RViz (urdf_tutorial) | historical evidence from the notes (A) – `1.4.docx`, lesson 32, p79, IMG055, unchanged | `src/notes_1.4_lesson32_p79_IMG055.png` |

Regenerate everything after a verification run:

```bash
cd report/figures
python3 src/make_figures.py ../../verification/logs/run_2026-09-28/model_report.json \
                            ../../verification/logs/run_2026-09-28/arduinobot_expanded.urdf
python3 src/make_screenshot_figures.py ../../verification/logs/run_2026-09-28
```

Requirements: Python 3 with matplotlib, numpy and Pillow; Graphviz (`dot`); Poppler (`pdftoppm`).
