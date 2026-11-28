# Spikes 3 and 4: agent loading, pinning and sandboxing

Run on 2026-11-28 against Claude Code 2.1.319 on macOS, from a Terminal panel tab, with `--model haiku` throughout. The scripts (`spike34.py`, then `spike34b.py` as the one re-run), the fixture plugin, the settings files and both logs are in `spike34/` in the session scratchpad.

## Recommendation

Launch every role with `--setting-sources ""`, a role settings file, an empty strict MCP config and `--permission-prompts none`. Together these drop the user's permission mode, allow list, plugins, hooks, CLAUDE.md and MCP servers, and auth still works. Plan section 2.4 needs three changes:

1. **`--agent` gives the persona but does not preload the agent's `skills:`.** Preloading happens only when the agent runs as a subagent. The agent body must tell the agent to invoke its skills with the Skill tool, or the CLI must put the skill text in the prompt.
2. **On this machine a Bash sandbox and auto-approval of sandboxed Bash are always on.** They come from a source that `--setting-sources ""` does not remove. So in practice the sandbox, not the allow list, decides which Bash commands run. The role settings should state the sandbox explicitly so that the behaviour does not depend on that outside source.
3. **The sandbox confines Bash, not the Write and Edit tools.** In `acceptEdits` mode, Write created a file outside the work directory. The CLI's write-set check can only catch writes inside the worktree, so a role that edits files needs permission rules for Write and Edit. Those rules are untested.

## Fixtures

The fixture plugin `probe-plugin` holds four agents, each told to start its reply with its own marker word. `probe-agent` lists `skills: [probe-skill]`, `probe-agent-ns` lists `probe-plugin:probe-skill`, `probe-visible-agent` lists `probe-visible`, and `probe-control` lists none. `probe-skill` has `user-invocable: false`, the docs field that hides a skill from the `/` menu, and the secret word QUASAR7731. A plugin SessionStart hook prints PROBEHOOKFIRED. `pin.json` holds `{"permissions":{"allow":["Bash(ls *)"],"defaultMode":"default"},"enabledPlugins":{}}`. Prompts went on stdin, because the list-taking flags (`--tools`, `--allowedTools`, `--disallowedTools`, `--mcp-config`) would probably swallow a trailing prompt.

## Spike 3: agent loading

**a. Names.** `--agent probe-agent` and `--agent probe-plugin:probe-agent` both worked. `--agent no-such-agent` and `--agent other-plugin:probe-agent` exited 1 in about 1 s, with stdout empty and `--agent 'no-such-agent' not found. Available agents: claude, Explore, ..., probe-plugin:probe-agent, ...` on stderr.

**b. Persona.** It applied in every run. Each agent began its reply with its marker word, for example `ZEBRAMARK ok`.

**c. Skills.** `--agent probe-plugin:probe-agent` asked for the secret word without tools and answered `ZEBRAMARK UNKNOWN`. It reported that only the skill's one-line description was in its context. The result was the same for the namespaced reference, for the visible skill, and with tools on or off (5 runs). When the control agent called the Agent tool with `subagent_type probe-plugin:probe-agent`, the subagent answered `ZEBRAMARK QUASAR7731`. So `skills:` preloading works for subagents, the bare skill name resolves inside the plugin, and `user-invocable: false` does not block preloading. The control agent could also load the hidden skill itself with the Skill tool and then reported QUASAR7731. The hidden skill is missing from the init event's `skills` and `slash_commands`, which is the user's list, but it appears in the model's skill listing.

**d. `--agents` inline.** `--agents '{"inline-probe":{"description":...,"prompt":"...KESTRELMARK...","skills":[...]}}' --agent inline-probe` applied the persona and did not preload the skill, with either `probe-skill` or `probe-plugin:probe-skill`. It behaves the same as a plugin agent.

## Spike 4: pinning and sandboxing

**a. Setting sources.** Each row is one run of a trivial prompt. "Gates" means the model reported a heading from the user's CLAUDE.md.

| Flags | Mode | User plugins | PONYTAIL hook | CLAUDE.md | claude.ai MCP | Plugin-dir hook |
|---|---|---|---|---|---|---|
| none | auto | loaded | yes | yes | 8 servers, 101 tools | yes |
| `--setting-sources ""` | default | gone | no | no | none (strict) | yes |
| `--setting-sources project,local` | default | gone | no | no | none (strict) | yes |
| `--setting-sources ""  --settings pin.json` | default | gone | no | no | none (strict) | yes |
| `--settings pin.json` only | default | loaded | yes | yes | none (strict) | yes |

The empty string is accepted. `--settings` overrides `defaultMode`, but `enabledPlugins: {}` in it does not unload the user's plugins. Five org-managed plugins and the org-managed telemetry hooks load under every combination. Auth worked in all runs, with `is_error: false`.

**b. Denial test.** With `--setting-sources "" --settings pin.json --permission-mode default --permission-prompts none`, the agent was asked to run `ls`, `touch work/denied.txt`, `date`, `echo hi > work/echo.txt` and `touch` on a file in the scratchpad. All five ran, the files appeared, and `permission_denials` stayed empty. The transcript records each call as `permissionDecision: {"decision":"accept","source":"config"}`. It also shows that the child ran with a Bash sandbox that allows writes to `.`, `/tmp/claude*`, `$TMPDIR` and a few other paths. Neither the user's settings nor `pin.json` enables that sandbox, so it comes from another source, probably org-managed or desktop-provided settings. On 2.1.319, `autoAllowBashIfSandboxed` still defaults to true, so sandboxed Bash runs without asking. That source is inferred and was not confirmed.

Denial itself works without stalling. In run 1, with the work directory under `/tmp/claude-501`, each `touch` came back with "Permission for this tool use was denied ... this session has no approval surface" and was listed in `permission_denials`, and the run finished normally. Why that run prompted at all is unexplained.

**c. Tool flags.** `--tools Read,Bash --allowedTools "Bash(touch *)" --disallowedTools "Bash(ls *)"` reduced the init tool list to `["Bash","Read"]`. `ls` was denied and listed in `permission_denials`. `touch` ran. A Write call failed with `No such tool available: Write`. All three flags work under the pinned settings.

**d. Sandbox.** These tests used a work directory under the home directory, because run 1 showed that `/tmp/claude-501` is writable by default. The settings added `"sandbox":{"enabled":true,"allowUnsandboxedCommands":false,"autoAllowBashIfSandboxed":true}`. In both `default` and `acceptEdits` mode, and with `Bash(touch *)` allowed, `touch work/x` succeeded. `touch` in a sibling directory and `touch ~/probe` failed with `Operation not permitted`, and neither was recorded as a permission denial. Under `acceptEdits`, the Write tool created files both inside the work directory and in the sibling directory.

**e. MCP.** `--strict-mcp-config --mcp-config empty.json` gave `mcp_servers: []` with the user's sources loaded. Without it, the session loaded 8 claude.ai servers and a trivial call cost $0.117, against $0.0007 without them. `--setting-sources ""` alone also removed them.

**f. Sessions.** The full template, with `--agent`, `--session-id`, `--json-schema` and `--autocompact 150000`, returned `structured_output {"status":"ready","word":"PELICAN"}` and wrote `~/.claude/projects/<cwd-key>/<uuid>.jsonl`. A `--resume` with the same flags returned `{"status":"done","word":"PELICAN"}`.

## Verified and inferred

Each result above was observed once. Inferred, not tested: the source of the always-on sandbox, and that list-taking flags swallow a trailing prompt.

## Recommended launch

```bash
claude -p --model <model> --output-format json \
  --agent orchestra:<role> --session-id <uuid> --json-schema <schema> \
  --plugin-dir <orchestra> --setting-sources "" --settings <role-settings.json> \
  --strict-mcp-config --mcp-config <empty-mcp.json> \
  --permission-mode default --permission-prompts none \
  --tools <role tools> --autocompact 150000 < <prompt-file>
```

The command runs with the worktree as cwd. `<role-settings.json>`:

```json
{
  "permissions": {
    "allow": ["<role Bash rules, e.g. Bash(uv run pytest *)>"],
    "deny": ["Bash(git push *)", "<role-specific denials>"],
    "defaultMode": "default"
  },
  "sandbox": {
    "enabled": true,
    "allowUnsandboxedCommands": false,
    "autoAllowBashIfSandboxed": true,
    "filesystem": {"denyWrite": ["~/.orchestra"]}
  }
}
```

The allow and deny rules cover what the sandbox cannot see, such as network use and git operations on the main repository. `denyWrite` for `~/.orchestra` is untested and is there to keep agents away from CLI state.

## Implications for the plan

- **Section 2.4.** Add `--setting-sources ""` and `--mcp-config <empty>` to the template, pass prompts on stdin, and drop the idea that the settings pin which plugins load. Only `--setting-sources` and `--plugin-dir` control that.
- **Section 6.3.** "An agent names its skills" needs a mechanism for headless roles. The options are a first step in the agent body that invokes each skill (verified to work through the Skill tool), or CLI-injected skill text. Hidden skills work for both.
- **Section 2.3.** The human-decision hook can ship as a plugin hook, because hooks from `--plugin-dir` load under `--setting-sources ""`. Org-managed hooks also load and cannot be turned off.
- **Write set.** The sandbox covers Bash only. Plan check 2 sees only the worktree, so nothing stops Write or Edit outside it until permission rules for those tools are tested.

## Open

- Write and Edit confinement: `default` mode with `allow: ["Edit(./**)","Write(./**)"]` and a write outside, which should be denied.
- Where the always-on sandbox comes from, and what happens on a machine without it.
- Why run 1's sandboxed `touch` inside `/tmp/claude-501` was denied as needing approval.
- Whether `allowUnsandboxedCommands: false` holds when an agent asks for `dangerouslyDisableSandbox`.

## Session files

There were 33 session files under `~/.claude/projects`. Twenty-three are in `<scratchpad-key>-spike34-work/` and 10 in `-Users-<user>--orchestra-spike34-work/`. The two failed `--agent` runs wrote none. Both logs list every ID. The work directories and probe files are deleted.

## Later results

Spike 5 superseded the recommended role settings above. Write and Edit stay inside the worktree only with `permissions.blockWritesOutsideWorkingDirectories: true`, `Write(...)` allow rules are never matched, and the `denyWrite` entry for `~/.orchestra` was not carried into spike 5's settings. The v0 plan (draft 4, section 2.4) restores it for the resolved `ORCHESTRA_HOME`.
