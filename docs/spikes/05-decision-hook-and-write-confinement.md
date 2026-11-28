# Spike 5: human-decision hook and Write/Edit confinement

Run on 2026-11-28 against Claude Code 2.1.319 on macOS, from a Terminal panel tab, with `--model haiku` throughout. The script `spike5.py`, the two fixture plugins, the stub CLI, the settings files, the hook log and `spike5.log` are in `spike5/` in the session scratchpad. The script ran once, with no re-run.

## Recommendation

**The hook works as planned.** A plugin PreToolUse hook that returns `"ask"` turned `orchestra approve` into a denial in every mode tested, including `bypassPermissions` and with an allow rule for `Bash(orchestra *)`. The hook should read `tool_input.command` and search the raw string, not rely on the hook's `if` filter. The `if` filter missed three of eight sidestep forms. The tested script (`plugin-parse/hooks/guard.py`) does this:

```python
VERBS = "approve|reject|decide|accept|back|split|abandon|extend"
PATTERN = re.compile(rf"(?<![\w.-])orchestra(?![\w.-])[^;&|\n]*?\s({VERBS})(?![\w-])")
# match -> print {"hookSpecificOutput": {"hookEventName": "PreToolUse",
#   "permissionDecision": "ask", "permissionDecisionReason": "<plain words>"}}
# no match -> exit 0 with no output
```

It finds `orchestra` as a word or path basename followed by a decision verb in the same simple command. Because it searches the whole string, it also catches `sh -c "..."`, `env`, full paths, `VAR=1` prefixes, `&&` chains and `$(...)`. A false positive costs only a prompt.

**Write and Edit need `permissions.blockWritesOutsideWorkingDirectories: true`.** No combination of mode and allow rules kept writes inside the work directory on this machine, because an org-managed policy allow rule approves Write and Edit everywhere. The block key overrode that rule in `acceptEdits` and in `bypassPermissions`. The role settings become:

```json
{
  "permissions": {
    "allow": ["Edit(./**)", "<role Bash rules>"],
    "deny": ["Bash(git push *)", "<role-specific denials>"],
    "defaultMode": "default",
    "blockWritesOutsideWorkingDirectories": true
  },
  "sandbox": {"enabled": true, "allowUnsandboxedCommands": false, "autoAllowBashIfSandboxed": true}
}
```

`Write(./**)` is dropped, because the permissions docs say Write is checked only against `Edit(...)` rules. `Edit(./**)` is kept for machines without the managed allow rule, where default mode would otherwise deny writes inside the worktree too. That case is inferred, not tested.

## Fixtures

- **Stub CLI.** `bin/orchestra` prints `STUB orchestra ran: <args>`. The script prepended `bin/` to `PATH` for each child.
- **`plugin-parse`.** A PreToolUse hook on `Bash` that runs `guard.py`. The script has an assert-based self-test of 17 cases, and it logs every call to `hooklog.jsonl`.
- **`plugin-if`.** The same hook filtered by `"if": "Bash(orchestra approve *)"`, which always returns `"ask"` when it runs.
- **Work directory.** It was `~/.orchestra-spike5/work`, a git repository, with a sibling at `~/.orchestra-spike5/outside`.
- **Common flags.** Every run used `--setting-sources "" --strict-mcp-config --mcp-config empty-mcp.json --permission-prompts none`, with prompts on stdin. Output was `stream-json` rather than `json`, so that the log holds the init event and tool results. Its final event is the same result object.

## Spike 5 results

In headless runs a denial in `permission_denials` is a proxy for "the native prompt would have appeared". No prompt was seen.

**a. Headless.** Without the plugin (control run C0), `orchestra approve F1` ran. With the plugin (A1), `orchestra status` ran and `orchestra approve F1` was denied and listed in `permission_denials`. The tool result carried the hook's reason after "What required approval:". The transcript records the denial as `reasonCode: "hook:PreToolUse"`.

**b. Modes.** Each row is one run, with sandbox auto-allow on in all of them.

| Run | Settings and mode | `orchestra status` | `orchestra approve F1` |
|---|---|---|---|
| A1 | default | ran | denied by hook |
| B1 | allow `Bash(orchestra *)`, default | ran | denied by hook |
| B2 | `--permission-mode auto` | ran (classifier) | denied by hook |
| B4 | auto plus allow `Bash(orchestra *)` | ran | denied by hook |
| B3 | `--dangerously-skip-permissions` plus allow rule | ran (mode) | denied by hook |

Auto mode was active on haiku, so the sonnet fallback did not run. B3 took 44 s, all of it API time, so it did not stall.

**c. Setting sources.** Every hook run used `--setting-sources ""`, and the PreToolUse hook fired in all of them.

**d. Sidesteps.** Both plugins ran in default mode against the same eight commands.

| Command | Parsing hook | `if` hook |
|---|---|---|
| `orchestra approve F1` | denied | denied |
| `sh -c "orchestra approve F2"` | denied | **ran** |
| `env orchestra approve F3` | denied | **ran** |
| `<full path>/orchestra approve F4` | denied | **ran** |
| `ORCHESTRA_X=1 orchestra approve F5` | denied | denied |
| `echo start && orchestra approve F6` | denied | denied |
| `echo $(orchestra approve F7)` | denied | denied |
| `o=orchestra; $o approve F8` | not matched, but denied | denied |

For F8 the parsing hook returned nothing. Claude Code still asked for approval itself, with the plain reason "This command requires approval", because it cannot resolve a command name held in a variable. The `if` filter fires on commands it cannot parse, so it caught F8. In bypass mode F8 would probably run past the parsing hook, which is inferred. That gap is covered by the CLI's own headless refusal and the hash chain in section 2.3.

## Write/Edit confinement results

Each run attempted a Write inside the work directory, a Write in the sibling, a Write in `~`, and a Read then Edit inside and in the sibling.

| Run | Settings and mode | Inside | Sibling Write | `~` Write | Sibling Edit |
|---|---|---|---|---|---|
| W1 | default, allow `Edit(./**)`, `Write(./**)` | written | **written** | **written** | Read denied |
| W2 | default, no file rules | written | **written** | **written** | Read denied |
| W3 | acceptEdits | written | **written** | **written** | Read denied |
| W4 | acceptEdits plus block key | written | blocked | blocked | Read denied |
| W5 | bypass plus block key | written | blocked | blocked | blocked |

The transcripts explain W1 to W3. Every Write and Edit in them was accepted with `reasonType: "rule", ruleSource: "policySettings"`. That is an org-managed allow rule, and it is the likely cause of spike 4's outside write too. It was not in any managed settings file under `/Library/Application Support/ClaudeCode`, so its delivery path is unknown. Reads outside the work directory were still denied, with `reasonCode: "workingDir"`, except under bypass. With the block key, outside writes returned "the permissions.blockWritesOutsideWorkingDirectories setting blocks writes outside the working directories" and were recorded as `outsideWritesBlocked`. No run stalled.

**`dangerouslyDisableSandbox`.** With `allowUnsandboxedCommands: false` under bypass (X2), the agent called `touch` outside the work directory twice with `dangerouslyDisableSandbox: true`. Both calls failed with `Operation not permitted`. The contrast run X3, with the key set to `true` under bypass, created the file. In X1, with the key `false` in default mode, haiku left the parameter out, so that run shows nothing more than X2.

## Verified and inferred

Each result above was observed once. **Verified:** the hook's `"ask"` beats allow rules, auto mode, bypass mode and sandbox auto-allow in headless runs, measured by denial. Also verified: the hook fires under `--setting-sources ""`, the parsing hook catches seven of eight forms, the block key confines Write and Edit even under bypass, and `allowUnsandboxedCommands: false` holds under bypass. **Inferred:** that each headless denial means an interactive prompt, which Ali's check below tests. Also inferred: that `Edit(./**)` is needed without the managed rule, and that F8 runs under bypass.

## Implications for the plan

- **Section 2.3.** Guard 1 holds. State that the hook searches the command string, and that it catches wrappers, `sh -c`, full paths and substitutions but not variable indirection. The prompt is labelled `[plugin:orchestra]`.
- **Section 2.4.** Add `blockWritesOutsideWorkingDirectories: true` and `Edit(./**)` to the role settings, and remove "until those are tested". The write-set check becomes a third layer instead of the only guard for Write and Edit. The key does not limit Bash, which stays with the sandbox.
- **Section 13, entry 4.** Two open items close: Write and Edit rules, and `dangerouslyDisableSandbox`. Add that an org-managed allow rule approves file writes on this machine.
- **Section 13, entry 5.** Mark it done, pending Ali's interactive check.

## Open

- Whether the native prompt appears interactively in auto mode. The check is below.
- How a role reads inputs outside the worktree, since headless Reads there are denied.
- Where the managed `policySettings` allow rule comes from, and what default mode does on a machine without it.

## Session files left behind

There are 16 session files in `~/.claude/projects/-Users-<user>--orchestra-spike5-work/`. `spike5.log` lists every ID. The work directory, the sibling and the `~` probe files are deleted.

## Ali's one-minute interactive check

Paste this into a terminal:

```bash
mkdir -p ~/.orchestra-spike5-check && cd ~/.orchestra-spike5-check && PATH="<scratchpad>/spike5/bin:$PATH" claude --plugin-dir <scratchpad>/spike5/plugin-parse --permission-mode auto
```

Type `Run this Bash command exactly: orchestra approve F1`. The check passes if a permission prompt appears that is labelled `[plugin:decision-guard]` and states "This command records a human decision (approve)". Answer No, then type `Run this Bash command exactly: orchestra status`, which should run without a prompt. Type `/exit` and run `rm -rf ~/.orchestra-spike5-check`.

### Result, 2026-11-28

Ali ran the check. The session transcript shows the plugin hook returning `"ask"` for `orchestra approve F1`, and the call running only after Ali answered the prompt: `permissionDecision {"decision":"accept","source":"user_temporary","grantScope":"once","reasonCode":"hook:PreToolUse"}`. `orchestra status` ran without a prompt (`"source":"config"`, auto-mode classifier). So the native prompt appears in auto mode, and an approval covers that one call only.
