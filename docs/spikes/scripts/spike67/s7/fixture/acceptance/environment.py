import os, signal, subprocess, sys, time
from pathlib import Path

SERVICE = Path(__file__).resolve().parent.parent / "service" / "server.js"


def before_all(context):
    # Treat SIGTERM like Ctrl-C so after_all still stops the service.
    signal.signal(signal.SIGTERM, signal.default_int_handler)
    # start_new_session: the service gets its own process group, so cleanup can kill it and anything it spawns.
    proc = subprocess.Popen(
        ["node", str(SERVICE)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, start_new_session=True, env={**os.environ, "PORT": "0"},
    )
    context.service = proc
    # Record the pgid so a supervisor (the CLI) can reap it if behave itself is SIGKILLed.
    pidfile = os.environ.get("ORCH_SERVICE_PIDFILE")
    if pidfile:
        Path(pidfile).write_text(str(proc.pid))
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        line = proc.stdout.readline()
        if line.startswith("LISTENING "):
            context.base_url = f"http://127.0.0.1:{int(line.split()[1])}"
            print(f"service up at {context.base_url} pid={proc.pid}", file=sys.stderr)
            return
        if not line and proc.poll() is not None:
            break
    stop(context)
    raise RuntimeError(f"service failed to start (exit {proc.returncode})")


def stop(context):
    proc = getattr(context, "service", None)
    if proc and proc.poll() is None:
        os.killpg(proc.pid, signal.SIGTERM)
        try:
            proc.wait(5)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)


def after_all(context):
    stop(context)


def before_scenario(context, scenario):
    # Fixture knob for the interrupt tests only.
    time.sleep(float(os.environ.get("SLOW_SCENARIO", 0)))
