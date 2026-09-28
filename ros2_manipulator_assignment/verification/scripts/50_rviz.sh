#!/bin/bash
# Stage 50: display.launch.py with RViz (needs a display; Xvfb is started if none is set)
source "$(dirname "$0")/common.sh"
export ROS_DOMAIN_ID=51 QT_X11_NO_MITSHM=1
if [ -z "$DISPLAY" ]; then export DISPLAY=:77 LIBGL_ALWAYS_SOFTWARE=1; Xvfb :77 -screen 0 1920x1080x24 >/dev/null 2>&1 & sleep 2; fi
shot() { local name=$1 wid; wid=$(xdotool search --name "$2" 2>/dev/null | tail -1)
         if [ -n "$wid" ]; then import -window "$wid" "$OUT/$name"; else import -window root "$OUT/$name"; fi; echo "screenshot: $name (window '$2' id ${wid:-root})"; }
echo "================ A: ros2 launch arduinobot_description display.launch.py (default gui:=true)"
L=$(start_bg "$OUT/50_display_launch.log" ros2 launch arduinobot_description display.launch.py)
sleep 25
run ros2 node list --no-daemon --spin-time 5
run ros2 topic info /joint_states --no-daemon --spin-time 5
run ros2 topic info -v /robot_description --no-daemon --spin-time 5
run bash -c "xdotool search --name '.' getwindowname %@ 2>/dev/null | sort -u | grep -v '^$'"
# place the two windows side by side so that neither hides the other in the screenshots
xdotool search --name "RViz" windowmove 0 0 2>/dev/null; xdotool search --name "Joint State Publisher" windowmove 1600 0 2>/dev/null; sleep 2
import -window root "$OUT/50_display_launch_screen.png"; echo "screenshot: 50_display_launch_screen.png (whole virtual screen)"
shot 50_display_launch_rviz.png "RViz"
shot 50_display_launch_jsp_gui.png "Joint State Publisher"
stop_bg "$L"
echo "--- launch log"; cat "$OUT/50_display_launch.log"
sleep 2
echo; echo "================ B: RViz started 8 s AFTER robot_state_publisher (late join), non-zero joint values"
SHARE=$(ros2 pkg prefix arduinobot_description)/share/arduinobot_description
RSP=$(start_bg "$OUT/50_late_rsp.log" ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro $SHARE/urdf/arduinobot.urdf.xacro)")
JSP=$(start_bg "$OUT/50_late_jsp.log" ros2 run joint_state_publisher joint_state_publisher --ros-args \
      -p zeros.joint_1:=-0.5 -p zeros.joint_2:=0.3 -p zeros.joint_3:=-0.4 -p zeros.joint_4:=-0.6)
sleep 8
RV=$(start_bg "$OUT/50_late_rviz.log" rviz2 -d "$SHARE/rviz/display.rviz")
sleep 25
run ros2 topic info -v /robot_description --no-daemon --spin-time 5
shot 50_late_join_posed_rviz.png "RViz"
stop_bg "$RV"; stop_bg "$JSP"; stop_bg "$RSP"
echo "--- rviz log"; cat "$OUT/50_late_rviz.log"
