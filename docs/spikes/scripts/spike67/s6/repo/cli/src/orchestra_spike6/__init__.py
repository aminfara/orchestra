import os, sys, time
from importlib.metadata import version
from pathlib import Path

def main():
    d = Path.home() / ".orchestra-spike6"
    v = version("orchestra-spike6")
    try:
        d.mkdir(exist_ok=True)
        f = d / f"marker-{os.getpid()}"
        f.write_text(f"{time.time()} {sys.argv}\n")
        wrote = f"wrote {f}"
    except OSError as e:
        wrote = f"WRITE FAILED: {e}"
    print(f"orchestra-spike6 {v} argv={sys.argv} exe={sys.executable} {wrote}")
