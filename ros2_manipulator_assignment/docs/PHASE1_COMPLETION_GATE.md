# Phase 1 completion gate

Checked on 28 Sep 2026 before the final report was produced.

| Gate condition | Status | Where |
|---|---|---|
| Notes inspected and progress evidence recorded | Done – all five files converted without altering the originals, 483 rendered pages and 164 images inspected; 29 evidence rows with locators; boundaries independently re-checked and every row adversarially verified | `COURSE_PROGRESS_EVIDENCE.md` |
| Instructor source revision and baseline identified | Done – `main` @ `4936385347e477c59927382c904883c432c9b33d`, `Section4_Digital_Twin/arduinobot_ws/src`; `gz-classic` @ `07440a5` compared | `PROVENANCE.md` §1 |
| Active workspace coherent and organised | Done – `arduinobot_ws/src` with three uniquely named packages; reference snapshots kept outside | `PROVENANCE.md` §2, `VERIFICATION.md` V1 |
| Core examples and robot visualisation prepared | Done – publishers, subscribers, parameter nodes, description, `display.launch.py` (`gui` argument), RViz configuration | `arduinobot_ws/src` |
| Corrections documented as category C | Done – C1–C12 with reasons and evidence; unified diff | `PROVENANCE.md` §3, `patches/` |
| Robot model preserved and structure checked | Done – Xacro and meshes byte-identical to the instructor's; topology, types, axes, limits, mimic and mesh URIs checked; scale discrepancy recorded, not "fixed" | `VERIFICATION.md` V13–V14, audit §3.1 |
| Verification as far as the environment permits | Done – build, tests, both cross-language runs, parameters, joint states, TF, RViz (software rendering, `gui:=true` and `gui:=false`), late join, clean shutdown, archive build, in an Ubuntu 22.04 / Humble container | `VERIFICATION.md` §2 |
| Remaining tests and limitations explicit | Done – target-machine checks, xmllint (network), interactive sliders, Gazebo, control, MoveIt, hardware | `VERIFICATION.md` §3–4 |
| Figures and code excerpts correspond to the final project | Done – figures regenerated from the final verification run; report listings are extracted from the delivered files at build time (`report/tools/content.py:excerpt`) | `report/figures/README.md` |
| Fixable source errors resolved before the report | Done – no known open defect in the delivered core; the optional Gazebo launch file is untested and marked as such | – |

**Phase 1 conclusion:** project prepared, built and runtime-verified in an Ubuntu 22.04 /
ROS 2 Humble container; checks on the student's own machine, with a hardware-accelerated
display, and of the optional Gazebo launch remain pending. This limitation is carried into
the report (abstract, sections 13, 15 and 16).
