# Spikes 6 and 7: plugin packaging and the acceptance harness

Run on 2026-11-28 on macOS against Claude Code 2.1.332, uv 0.13.10, Behave 1.3.3 and Node v26.13.1. The acceptance environment used uv's managed CPython 3.13.12. Spike 6 ran its installs from one script in a Terminal panel tab, then probed from sandboxed Bash. Spike 7 ran entirely in sandboxed Bash. Fixtures are in `spike67/` in the session scratchpad.

## Recommendation

**Ship the CLI as `cli/` in this repo and install it with `uv tool install`.** A user on a fresh machine runs three commands after installing uv:

```bash
/plugin marketplace add aminfara/orchestra        # then /plugin install orchestra@orchestra
uv tool install "git+https://github.com/aminfara/orchestra@v<version>#subdirectory=cli"
orchestra setup
```

For development, Ali uses `uv tool install --editable ./cli`, and edits take effect without a reinstall.

**Skills call bare `orchestra`, never an absolute path.** A bare `orchestra probe` from sandboxed Bash matched `excludedCommands: ["orchestra *"]` and wrote under `~`. The same binary called by its full path was sandboxed, and so was the call chained after `echo`. uv puts the binary in `~/.local/bin`, which must be on `PATH` (`uv tool update-shell` adds it). Hooks are different: Claude Code runs them directly, so they reference scripts as `"${CLAUDE_PLUGIN_ROOT}"/hooks/guard.py`. The decision hook never calls the CLI.

**Do not use the plugin `bin/` directory for the CLI.** The plugins reference says files in `bin/` are on the Bash tool's `PATH` while the plugin is enabled. They are not on the Terminal tab's `PATH`, where `orchestra run` lives, and claude.ai and Cowork refuse to install a plugin that has `bin/`. A shim there would also need its own virtual environment.

**Keep the plugin and CLI versions equal and let `orchestra setup` check them.** `cli/pyproject.toml` carries the same version as `.claude-plugin/plugin.json`, and both are bumped together. Claude Code substitutes `${CLAUDE_PLUGIN_ROOT}` into skill text, so the skill runs `orchestra setup --plugin-root ${CLAUDE_PLUGIN_ROOT}`, which is still one bare command. The CLI reads `plugin.json`, compares it with its own installed version, and on a mismatch prints the exact `uv tool install` line for the plugin's tag.

**The acceptance harness works as planned, with four additions.** `environment.py` starts the service on port 0 in its own process group and maps SIGTERM to Ctrl-C. A six-line loader pulls in `steps/<feature-id>/`. The duplicate-step check is `behave --dry-run` run twice, in normal and reversed load order. The red check reads the JUnit XML by a strict rule (below), because a service that fails to start shows up as skipped tests with no error.

## Spike 6 results

| Install form | Time | Result |
|---|---|---|
| `uv tool install ./cli` | 3.6 s | `~/.local/bin/orchestra` symlinks to `~/.local/share/uv/tools/orchestra-spike6/bin/orchestra` |
| `uv tool install --editable ./cli` | 1.7 s | An edit to the source showed on the next call with no reinstall |
| `uv tool install "git+file://<repo>@v0.0.1#subdirectory=cli"` | 1.9 s | Resolved the tag to its commit and built from `cli/` |
| The same command again | under 1 s | "Checked 1 package", exit 0, no change |

The uv pages I fetched (concepts and guides for tools, and pip packages) show `git+https://` and `@tag` but do not mention `#subdirectory`. The local `git+file` test confirms that uv accepts the form, and `uv tool install --help` lists `--editable`. I did not fetch the real GitHub repo.

From sandboxed Bash, with the git-form install on `PATH`:

| Call | Write to `~/.orchestra-spike6/` |
|---|---|
| `orchestra probe sandboxed-bare` | written |
| `~/.local/bin/orchestra probe ...` | Operation not permitted |
| `echo control && orchestra probe ...` | Operation not permitted |

`uv tool install` writes to `~/.local/share/uv/tools` and `~/.local/bin`, which the sandbox denies. Installing is therefore a Terminal step, done once per machine.

## Spike 7 results

The fixture is a 15-line Node HTTP service with `GET /hello` and `POST /count`. It listens on `PORT` (0 picks a free port), prints `LISTENING <port>`, and exits 3 when `FAIL_START=1`. `acceptance/` holds a `pyproject.toml` with `behave` as the only dependency, two features (`greeting`, `counter`) with five scenarios, and steps in `steps/greeting/` and `steps/counter/`.

**a. Start, stop and concurrency.** `before_all` starts `node` with `start_new_session=True` and reads stdout until the `LISTENING` line, with a 10-second limit. `after_all` sends SIGTERM to the process group, then SIGKILL after 5 seconds. A driver started Behave in its own group, as the CLI would, and checked the service afterwards:

| Ending | Behave exit | Service left running | JUnit files |
|---|---|---|---|
| Normal, with failing scenarios | 1 | no | 2 |
| SIGINT (Ctrl-C) | 1 | no | 2, rest marked untested |
| SIGTERM, before the fix | 143 | **yes** | 0 |
| SIGTERM, with `signal.signal(SIGTERM, signal.default_int_handler)` in `before_all` | 1 | no | 2 |
| SIGKILL | -9 | **yes** | 0 |

After SIGKILL nothing in Behave runs, so the CLI must reap the service. `environment.py` writes the service's PID, which is also its process group ID, to the file named by an environment variable, and the driver's `killpg` on it stopped the service. Two copies of the fixture, each with its own `UV_PROJECT_ENVIRONMENT`, ran at the same time in three rounds. Each round got two distinct ports and the same results, and no `.venv` appeared in either copy. Two concurrent `uv sync` runs into fresh environments sharing one cache both succeeded.

**b. Step folders.** Behave 1.3.3 does not load subfolders. Its `load_step_modules` lists only `steps/*.py`. This file in `steps/` is the smallest loader that works:

```python
# Behave loads only top-level steps/*.py; this pulls in steps/<feature-id>/*.py.
import os
from pathlib import Path
from behave.runner_util import exec_file

_files = sorted(Path(__file__).parent.glob("*/*.py"), reverse=bool(os.environ.get("ORCHESTRA_STEPS_REVERSE")))
for _f in _files:
    exec_file(str(_f), {})
```

A shared helper at `steps/http_helper.py` was importable from the feature folders, because Behave puts `steps/` on `sys.path` while it loads them.

**c. Duplicate steps.** Behave raised `AmbiguousStep`, exited 1 and wrote no JUnit when two features defined the same text. It did the same when a literal step (`the count is 1`) loaded after a matching pattern (`the count is {n:d}`). In the reverse order it said nothing: the literal registered first and silently took the step. Behave checks only whether an existing step matches the new step's text, so the check depends on load order. Running `behave --dry-run -f null` twice, once with `ORCHESTRA_STEPS_REVERSE=1`, caught the silent case on the reversed pass. A dry run takes 0.17 s, skips the hooks (with `FAIL_START=1` it reported no hook error), and also counts undefined steps. The CLI needs no scan of its own.

**d. JUnit XML and exit codes.**

| Case | `testcase status` | Child element | Exit |
|---|---|---|---|
| Passes | `passed` | none | 0 if all pass |
| Assertion fails | `failed` | `<failure type="AssertionError" message="got 'hello alice'">` | 1 |
| Undefined step | `error` | `<error type="NoneType" message="None">`, body says "undefined" | 1 |
| Exception in a step | `error` | `<error type="KeyError" message="'total'">` | 1 |
| Service fails to start | `untested`, every case | `<skipped />`; suite shows `errors="0" failures="0"` | 1 |
| Ctrl-C mid-run | `untested` for the rest | `<skipped />` | 1 |

The exit code is 1 for every case that does not pass, so it cannot tell red from broken. A startup failure looks like skipped tests, and only stdout's `HOOK-ERROR in before_all` names it. The red check therefore classifies the XML, with no stdout parsing:

- **Broken harness** if the exit code is not 0 or 1, the dry run fails, there are fewer XML files than feature files, or any testcase is `error`, `untested` or `skipped`.
- **Red as expected** otherwise, when every failing testcase is a `failure` of type `AssertionError` and the new scenarios are among them.

One gap remains for the test author: a feature that is not built may surface as an exception rather than an assertion. Python's `urllib` raises `HTTPError` on a 404, and a missing server refuses the connection. The step helpers must therefore return status codes and turn transport errors into assertions.

**e. Timings.** A fresh environment with an empty cache took 1.54 s for `behave` alone and 6.07 s for the first sync, which also had `httpx` and wrote `uv.lock`. A fresh environment with a warm cache took 0.02 to 0.03 s, and a no-op sync took 0.05 s. A full run of five scenarios took 0.24 to 1.03 s, including service start. Each environment is 1.6 MB.

**Sandbox quirks.** Four things failed only because of this session's sandbox, and they matter if agents run the harness from sandboxed Bash. `~/.cache/uv` is not writable, so I set `UV_CACHE_DIR` to the scratchpad. Node needed `OPENSSL_CONF=/dev/null`, because `/System` is read-denied. The sandbox denies reading `**/*.pem`, which broke `httpx` through `certifi`, so the steps use `urllib`. `uv sync` also could not remove `certifi`'s `cacert.pem`.

## Verified and inferred

**Verified:** every table above, each observed once except the concurrent runs, which ran three rounds. Also verified: the loader, the shared-helper import, dry runs skipping hooks, and a re-run install being a no-op.

**Inferred and not tested:** that `#subdirectory` works the same against GitHub over HTTPS, and that a skill's `${CLAUDE_PLUGIN_ROOT}` substitution reaches a Bash command intact. That moving to a new tag needs only a re-run of `uv tool install`; the uv docs say upgrades respect the original constraint, so `uv tool upgrade` will not move a pinned tag. That a 404 in a step shows as an `error` (from `urllib`'s documented behaviour).

## Implications for the plan

- **Section 2, the table.** The CLI row gains the install command and the rule that callers use bare `orchestra` on `PATH`. The Hooks row says scripts are referenced through `"${CLAUDE_PLUGIN_ROOT}"`.
- **Section 2.1.** The harness row lists `acceptance/environment.py`, `acceptance/steps/load_feature_steps.py` and `acceptance/uv.lock`, which the test author commits.
- **Section 2.6.** Replace "JUnit XML separates assertion failures from errors" with the classification rule in 7d. The duplicate check becomes the two-order dry run. Add that `environment.py` starts the service on a free port in its own process group, handles SIGTERM, and writes its process group ID for the CLI.
- **Section 4 and section 14, step 4 (the red check).** Use the rule in 7d. A startup failure counts as a broken harness, not as red.
- **Section 5.** Onboarding checks that `orchestra` is on `PATH` and that its version matches the plugin.
- **Section 10.** Add `features/<feature-id>/acceptance.pid` for the service's process group ID, which the CLI reaps after a killed run.
- **Section 13.** Entry 1's open item on uv-installed CLIs closes: the exclusion matches a bare call and not a full path. Entries 6 and 7 are done.
- **This repo's `CLAUDE.md`.** The version-bump rule should cover `cli/` as well as `skills/`. Ali decides this; I did not edit it.

## Open

- How `ORCHESTRA_PROXY_HUMAN` reaches the CLI's environment, still open from spike 1.
- Whether `excludedCommands` matches a command from a plugin's `bin/`. It does not affect the recommendation.
- Whether headless roles inherit the `*.pem` read deny and the `/System` deny, which would break common HTTP clients in a test author's sandboxed runs.
- An `AssertionError` raised in a `Given` step reads as red even when it is a setup failure. The test-author skill could reserve assertions for `Then` steps.
- Two overlapping patterns, such as `{n:d}` and `{word}`, are not caught by `AmbiguousStep` in either order.

## Leftovers

The throwaway tool is uninstalled and `~/.orchestra-spike6` is deleted. All virtual environments and uv caches for spike 7 are in the scratchpad, not under `~`. uv's own cache in `~/.cache/uv` probably holds the throwaway package's build and git checkout. Terminal tab `spike6 uv tool` is still open.
