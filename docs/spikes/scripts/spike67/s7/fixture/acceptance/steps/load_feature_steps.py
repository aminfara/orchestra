# Behave loads only top-level steps/*.py; this pulls in steps/<feature-id>/*.py.
# ORCHESTRA_STEPS_REVERSE=1 loads them in reverse order, so a dry run in both orders catches overlaps either way round.
import os
from pathlib import Path
from behave.runner_util import exec_file

_files = sorted(Path(__file__).parent.glob("*/*.py"), reverse=bool(os.environ.get("ORCHESTRA_STEPS_REVERSE")))
for _f in _files:
    exec_file(str(_f), {})
