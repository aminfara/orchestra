# Spike 1: who launches what

Run on 2026-11-27 against Claude Code 2.1.319 in the desktop app's Code tab on macOS.

## Recommendation

Run every `orchestra` command outside the Bash sandbox. Interactive calls (`submit`, `decide`, `status`) should go through one narrow `sandbox.excludedCommands` entry for `orchestra *`. `orchestra run` should go in a tab of the user's Terminal panel. A background Bash command is not an option: it escapes the 10-minute limit but not the sandbox, and inside the sandbox `claude -p` cannot authenticate. In dry runs, mode A should be driven by a subagent that returns at each checkpoint and is continued with SendMessage, while the main session plays Ali.

| Job | Host |
|---|---|
| State writes under `~/.orchestra` | The `orchestra` CLI, unsandboxed through `excludedCommands` (interactive) or in a Terminal tab (`run`) |
| Worktree creation | The same CLI, because `.git/worktrees` of a project repo is read-only in the sandbox |
| `orchestra run` and its `claude -p` children | A Terminal panel tab opened with `run_in_terminal`, read back with `read_terminal` |
| Mode A in dry runs | A subagent continued with SendMessage, with a `claude -p --resume` loop in a Terminal tab as the fallback |

Ali must decide whether to add the `excludedCommands` entry. Ali must also re-authenticate the CLI (`claude auth login`, or `claude setup-token` for unattended jobs), because the CLI's own login has expired and every headless run fails until it is renewed.

## Tests

### 1. Sandboxed writes

`mkdir -p ~/.orchestra-spike` failed with `Operation not permitted`. `touch ~/.claude/projects/spike-probe` failed the same way, and so did `touch ~/Workplace/orchestra/.git/spike-probe`. The session's sandbox config lists `~/.claude/projects` under `denyWithinAllow`, and its system notes say a repository's `.git/worktrees` is read-only apart from the session's own worktrees.

`git worktree add $TMPDIR/spike-wt -b wt` on a fresh repo in `$TMPDIR/spike-repo` succeeded, but only because that repo's `.git` sits under the writable `$TMPDIR`. A real project repo would fail at `.git/worktrees`. I did not add a worktree to the orchestra repo.

### 2. Headless run from sandboxed Bash

`claude -p "reply with the word ok" --output-format json --model haiku --session-id <uuid>` exited 1 in 3.5 seconds with `"result": "Not logged in · Please run /login"`, `"terminal_reason": "api_error"` and `"is_error": true`. The `session_id` in the JSON matched the UUID I passed. A probe of the keychain with `security find-generic-password` failed with `UNIX[Invalid argument]`, so the sandbox appears to hide the credential store from the child process.

`--resume <uuid>` then failed with `No conversation found with session ID`, which means the first run wrote no session file under `~/.claude/projects`.

### 3. The same run from the Terminal panel

From a script in a Terminal tab, both commands returned `"result": "Failed to authenticate: this login reached its time limit and cannot be renewed"`. Here the CLI found credentials, but they have expired. The first run wrote an 85 KB session file under `~/.claude/projects/<cwd-key>/<uuid>.jsonl`, and `--resume` found the conversation. Resume therefore works mechanically outside the sandbox. No model call has succeeded yet.

Every result JSON carries `session_id`, `total_cost_usd`, `usage` (input, output and cache tokens), `modelUsage`, `num_turns` and `terminal_reason`. All counts were zero and `modelUsage` was empty, so I could not see whether any field reports context size.

### 4. Background Bash

A `run_in_background` command ran `sleep 3` and then `mkdir -p ~/.orchestra-spike`. It completed and notified me. The `mkdir` failed with `Operation not permitted`, so background commands run in the same sandbox. The Bash tool's description caps the timeout at 600,000 ms for a foreground command and says a background command "keeps running across turns". I did not wait ten minutes to confirm it.

### 5. Terminal panel

`run_in_terminal` with `mkdir -p ~/.orchestra-spike && echo terminal-ok > ~/.orchestra-spike/terminal-test && cat ~/.orchestra-spike/terminal-test` printed `terminal-ok`, and sandboxed Bash could read the file back afterwards. The tool's description says commands run in the user's login shell, outside any sandbox, and keep running after the turn ends. Each command line needs approval, from Ali or the auto-mode classifier.

### 6. Sandbox settings (docs, code.claude.com/docs/en/sandboxing)

`sandbox.filesystem.allowWrite` adds write paths, for example `"allowWrite": ["~/.orchestra"]`. `sandbox.excludedCommands` takes `Bash(...)`-style patterns, for example `"orchestra *"`, and runs matching commands with no filesystem limits and no network proxy. Every command in a chain must match, and a redirect, `cd` or `$(...)` keeps the call sandboxed.

## Verified and inferred

Verified: tests 1 to 5 as observed above.

Inferred and not tested:

- `allowWrite` for `~/.orchestra` alone would not be enough. `submit` commits to the feature branch, which writes the main repo's `.git`. `~/.claude/projects` sits in the app's deny list, which an allow entry probably cannot override.
- `excludedCommands: ["orchestra *"]` would cover state, worktrees and children in one entry. I did not change any settings.
- `ORCHESTRA_PROXY_HUMAN` has to reach the CLI's environment through session `env` settings or the Terminal shell.
- A subagent's Bash shares the main session's sandbox and exclusions, and its native prompts reach Ali.

## Mode A in dry runs

A subagent gets a fresh context, so the agent that drafts the scenarios is not the one that approves them. It runs the `orchestra` skill until the envelope says to present something to the human, then returns the envelope. The main session decides as Ali with `--proxy-human` and continues the subagent with SendMessage. The risks are context growth across a whole flow and a possible lack of AskUserQuestion in subagents.

A `claude -p --resume` loop in a Terminal tab is the fallback. It gives exact cost figures but has no native prompts.

## Open for spike 2

- Repeat test 2 after re-authenticating, to get a real result JSON: cost and usage on a fresh run and on a resume, and any context-size field.
- Confirm SendMessage continuation of a subagent across several checkpoints, and whether AskUserQuestion and the native prompt work inside it.
- The existing spike 2 questions: resume after a kill, resume of a running session, and `--json-schema` with `--resume`.
- Confirm `excludedCommands` matches `orchestra ...` when the CLI is installed by `uv tool install`.

## Later results

- Ali added `sandbox.excludedCommands: ["orchestra *"]` to this repo's project settings by hand after this spike. With a stub on `PATH`, a bare `orchestra` call wrote to the home directory and the same call chained after `echo` was sandboxed (2026-11-27). Spike 6 confirmed the same for a CLI installed by `uv tool install`, and found that a full-path call stays sandboxed.
- Spike 2 re-ran test 2 after re-authentication. Spikes 4 and 5 closed the denial test.
- The v0 plan (draft 4) drops the subagent as mode A driver for dry runs. Mode A runs as a separate `claude -p --resume` process, so the drafting agent and the session playing Ali are different processes.
