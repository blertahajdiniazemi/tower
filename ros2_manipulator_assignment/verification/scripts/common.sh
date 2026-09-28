# Shared setup for the verification stages (sourced by each stage script).
# WS  : colcon workspace root containing src/ (default /ws)
# OUT : directory for logs and artefacts      (default /out)
set -o pipefail
source /opt/ros/humble/setup.bash
# In the container, xacro and joint_state_publisher(_gui) come from a source underlay
[ -f /opt/underlay/install/setup.bash ] && source /opt/underlay/install/setup.bash
WS=${WS:-/ws}
OUT=${OUT:-/out}
mkdir -p "$OUT"
[ -f "$WS/install/setup.bash" ] && source "$WS/install/setup.bash"
export RCUTILS_COLORIZED_OUTPUT=0
# print a command, then run it
run() { echo; echo "\$ $*"; "$@"; echo "[exit code: $?]"; }
# start a command in its own process group (so Ctrl+C can be emulated for the whole group)
start_bg() { local log=$1; shift; setsid "$@" > "$log" 2>&1 & echo $!; }
# emulate Ctrl+C: SIGINT to the process group, then wait for it
stop_bg() { kill -INT -- -"$1" 2>/dev/null; for i in $(seq 1 50); do kill -0 "$1" 2>/dev/null || break; sleep 0.2; done
            if kill -0 "$1" 2>/dev/null; then echo "[process group $1 still running after 10 s -> SIGKILL]"; kill -KILL -- -"$1"; fi; }
