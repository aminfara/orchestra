"""Start behave in its own process group (as the CLI would), interrupt it, then check whether the service survived."""
import os, signal, subprocess, sys, time
from pathlib import Path

acc, out = sys.argv[1], Path(sys.argv[2])
def alive(pid):
    try: os.kill(pid, 0); return True
    except ProcessLookupError: return False

for case, sig in [("normal", None), ("sigint", signal.SIGINT), ("sigterm", signal.SIGTERM), ("sigkill", signal.SIGKILL)]:
    pidfile = out / f"{case}.pid"; pidfile.unlink(missing_ok=True)
    env = {**os.environ, "ORCH_SERVICE_PIDFILE": str(pidfile), "SLOW_SCENARIO": "0" if sig is None else "1"}
    p = subprocess.Popen(["uv", "run", "--project", acc, "behave", "features", "-f", "progress",
                          "--junit", "--junit-directory", str(out / case)],
                         cwd=acc, env=env, start_new_session=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if sig:
        while not pidfile.exists(): time.sleep(0.05)
        time.sleep(1.5)
        os.killpg(p.pid, sig)
    tail = p.communicate(timeout=60)[0].strip().splitlines()[-2:]
    time.sleep(0.5)
    spid = int(pidfile.read_text())
    survived = alive(spid)
    if survived:
        os.killpg(spid, signal.SIGKILL)  # the supervisor's reap via the recorded pgid
        time.sleep(0.2)
    print(f"{case}: behave exit={p.returncode} service_survived={survived} reaped={survived and not alive(spid)} junit_files={len(list((out/case).glob('*.xml'))) if (out/case).exists() else 0} tail={tail}")
