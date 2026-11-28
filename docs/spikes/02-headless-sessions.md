# Spike 2: headless sessions

Run on 2026-11-27 against Claude Code 2.1.319 on macOS, from a Terminal panel tab, with `--model haiku --strict-mcp-config` on every call. The scripts are `spike2.py` and `spike2b.py` in the session scratchpad, and their logs sit next to them.

## Recommendation

The NEW/RESUME scheme works as the plan describes. Resume carries the conversation, resume after a kill works, and `--json-schema` works on a resume. Three changes are needed:

1. **Never resume a session that may still be running.** It does not fork. Both processes write the same session file under the same ID, and the transcript splits into two branches. The CLI must hold a per-session lock and kill a timed-out child before it resumes it.
2. **Record cost as a delta.** `total_cost_usd` is cumulative for the session across invocations. Store each invocation's cost as the new total minus the last stored total, or use `model_usage_since_last_result` from `stream-json`.
3. **Pin the permission mode and the setting sources.** A headless child inherits the user's `defaultMode` (here `auto`), the user's allow list and the user's SessionStart hooks. Spike 4 has to close this gap.

## Tests

### 1. New session, then resume

`claude -p "Remember the word PELICAN. Reply with only: ok" --output-format json --session-id <uuid>` exited 0 in 8.0 s and returned `"result":"ok"`. `claude -p "What word did I ask you to remember? ..." --output-format json --resume <uuid>` exited 0 in 7.2 s and returned `"PELICAN"` under the same `session_id`.

Beyond the fields spike 1 listed, the result JSON carries `permission_denials`, `is_error`, `subtype`, `stop_reason`, `duration_ms` and a `usage.iterations` list with one entry per API call. The `modelUsage` entry has `contextWindow: 1000000`, `maxOutputTokens: 128000` and `costBasis: "list"`.

### 2. Context fullness

No field reports how full the context is. `modelUsage.contextWindow` gives the window size only. Fullness can be derived from the last API call: `input_tokens + cache_read_input_tokens + cache_creation_input_tokens` of the last `usage.iterations` entry, or of the last `assistant` event in `stream-json`. For the third call in test 1's session that is 2 + 27,145 + 6,855 = 34,002 tokens. The top-level `usage` is the sum over the invocation's API calls, so it overstates context whenever the agent made more than one call. A trivial call already costs about 27,000 tokens, because the user's CLAUDE.md, plugins and skills load into the prompt.

### 3. Cost on resume

`total_cost_usd` was 0.00324 after the first call, 0.00642 after the first resume and 0.00806 after the second. The `stream-json` result also carried `model_usage_since_last_result` with `costUSD: 0.00165`, which is exactly the increment. `modelUsage` is cumulative too (cache reads 12,152, then 27,646). `usage` is per invocation. In test 5 the resume's total included the killed run's first call, so the total is persisted in the session file (a `cost-state` line) as each call completes.

`claude auth status` reports `authMethod: claude.ai` and `subscriptionType: enterprise`. The account is a subscription, so `costUSD` with `costBasis: "list"` is a list-price estimate, not a bill.

### 4. `--json-schema`

With `{"type":"object","properties":{"status":{"type":"string"}},"required":["status"]}`, a new session returned `"structured_output":{"status":"ready"}`, and `result` held the same object as a JSON string. `num_turns` was 2 and `stop_reason` was `tool_use`, so the schema works through a tool call. A `--resume` with the same schema returned `{"status":"done"}`. An invalid schema string exits 1 in 0.9 s with `Error: --json-schema is not valid JSON` on stderr.

### 5. Kill, then resume

A session asked to run `sleep 20` (`--allowedTools "Bash(sleep *)" --permission-prompts none`) was killed with SIGTERM to its process group after 6 s. It exited 143 with no stdout. The session file held the user prompt and the `tool_use`. A `--resume` exited 0 in 7.8 s. On resume the CLI appended a synthetic `tool_result` ("Tool call interrupted: the session ended before this call's result was recorded, so its outcome is unknown") and an assistant line "No response requested.", and the model answered that it had been asked to run `sleep 20` and could not confirm it finished.

### 6. Resume while running

A session started on the same `sleep 20` task was still running when, 6 s in, `--resume <same id> "Reply with only: concurrent"` ran. The resume exited 0 in 7.5 s and returned the same `session_id` with `"concurrent"`. No new session file appeared. The original kept running and finished with `"original-done"` (exit 0, `duration_ms` 27,046).

The single file now has two branches from the same `tool_use`. One holds the resume's synthetic "interrupted" result and the `concurrent` turn. The other holds the real `tool_result` and `original-done`. A later `--resume` followed the `original-done` branch and did not mention the `concurrent` turn. Each process's `total_cost_usd` counted only its own calls.

### 7. Errors, timing, permissions

`--resume` of an unknown ID exits 1 in 2.9 s with `No conversation found with session ID` on stderr and empty stdout. `--session-id` with an ID already in use exits 1 in 0.2 s with `Session ID ... is already in use`. Argument errors therefore come on stderr with no JSON, while spike 1's auth failures came as JSON with `is_error: true`. A trivial call took 7 to 12 s wall clock against a `duration_ms` of 3.2 to 8 s, so startup costs about 3 to 4 s.

The denial test did not test denial. Asked to run `echo hi > probe.txt` with only `Bash(sleep *)` allowed, the agent wrote the file in all three runs: with the inherited `auto` mode, with `--permission-mode manual` and with `--permission-mode dontAsk`. `permission_denials` stayed empty. The user's `~/.claude/settings.json` allows `Bash(echo *)`, and the child read it. The `stream-json` init event also showed `permissionMode: "auto"`, every user plugin's skills, and the user's SessionStart hooks running.

## Verified and inferred

Verified: everything under Tests, as observed.

Inferred and not tested:

- The kill-then-resume transcript is safe to continue, but the agent cannot know whether the killed command had side effects. The RESUME prompt after a timeout should say so and ask the agent to check the worktree.
- A later resume follows the most recently written branch. One sample only.
- `--permission-prompts none` denies, rather than stalls on, a tool that nothing allows. Not observed, see test 7.

## Implications for the plan

- **NEW/RESUME (2.4).** Keep it. The CLI must guarantee one live process per session ID: a lock file per session, and on timeout kill the process group and wait for exit before any RESUME. Treat `already in use` on `--session-id` as a CLI bug, not a retry.
- **Context threshold (4.4).** `--autocompact 150000` cannot be checked from the result alone, but the CLI can log last-call context per dispatch from `usage.iterations`. With a 1,000,000 window reported for haiku, check `contextWindow` for the models roles actually use.
- **Submissions.** Read `structured_output`, not `result`. Schema checking by the CLI (check 1 in 2.4) stays, as a second layer.
- **Timeouts and retries.** Detect failure from exit code, then `is_error`, then stderr when stdout is not JSON.
- **Cost recording.** See recommendation 2, and label figures as list-price estimates on a subscription.
- **Spike 4** must cover `--setting-sources`, an explicit `--permission-mode`, and whether user hooks and skills still load.

## Open

- A real denial test: a command outside both `--allowedTools` and the user's allow list, with `--permission-mode dontAsk --permission-prompts none`.
- Whether compaction changes any of the usage fields, and what `--autocompact` emits in `stream-json`.
- Session files created, all under `~/.claude/projects/<scratchpad-key>-spike2-work/`: `1050f80d…`, `25ea3bdc…`, `e7c2f523…`, `84febee2…`, `432896b1…`, `740b2778…`, `d75b8ebf…`. The throwaway `work` directory is deleted.
