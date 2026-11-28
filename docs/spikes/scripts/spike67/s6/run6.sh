#!/bin/bash
# spike 6: uv tool install forms. Leaves the git-form install in place for the sandboxed probe.
cd ${SPIKE_DIR:?set SPIKE_DIR to this folder}/s6/repo
exec > >(tee ${SPIKE_DIR:?set SPIKE_DIR to this folder}/s6/terminal.log) 2>&1
set -x
time uv tool install ./cli
command -v orchestra; ls -l "$(command -v orchestra)"
orchestra probe local-path
uv tool uninstall orchestra-spike6
time uv tool install --editable ./cli
orchestra probe editable-before
sed -i '' 's/orchestra-spike6 {v}/EDITED orchestra-spike6 {v}/' cli/src/orchestra_spike6/__init__.py
orchestra probe editable-after-edit
git checkout -q -- cli
uv tool uninstall orchestra-spike6
time uv tool install "git+file://${SPIKE_DIR:?set SPIKE_DIR to this folder}/s6/repo@v0.0.1#subdirectory=cli"
uv tool list --show-paths
orchestra probe git-subdir
uv tool install "git+file://${SPIKE_DIR:?set SPIKE_DIR to this folder}/s6/repo@v0.0.1#subdirectory=cli"; echo "reinstall-exit=$?"
cat ~/.orchestra-spike6/* 
echo SPIKE6-DONE
