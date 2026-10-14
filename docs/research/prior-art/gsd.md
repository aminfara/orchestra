# GSD (Get Shit Done)

- Original repo: https://github.com/glittercowboy/get-shit-done, which now redirects to https://github.com/gsd-build/get-shit-done. GitHub shows 64.3k stars and 5.4k forks. The owner archived it on 2026-06-26. Its README now reads "This repository is no longer the active home for GSD development." Last commit: 2026-05-31. npm package: `get-shit-done-cc`.
- Active successor: https://github.com/open-gsd/gsd-core ("GSD Core", npm `@opengsd/gsd-core`, v1.16.0 in `package.json`). 10.5k stars, last commit 2026-10-13.
- Author: `package.json` credits "TÂCHES". The original LICENSE names Lex Christopherson (GitHub user glittercowboy). GSD Core is copyright "Open GSD".
- License: MIT (both repos).

This note reads GSD Core at commit `08cde7a`. The archived repo has the same layout, so the findings apply to both.

## What it is (2-3 sentences)

GSD is a "meta-prompting, context engineering, and spec-driven development system" for Claude Code and about a dozen other agent runtimes. It runs a fixed loop per phase (Discuss, Plan, Execute, Verify, Ship) and pushes heavy work into fresh-context subagents, so the main session stays small. All state lives as Markdown and JSON under `.planning/`.

## Structure

An npm installer (`npx @opengsd/gsd-core@latest`) copies the files into each runtime's layout. The README says not to copy them by hand.

- **Commands/skills**: 72 user entry points (`/gsd-new-project`, `/gsd-plan-phase`, `/gsd-execute-phase`, `/gsd-debug`, `/gsd-quick`, and so on). Each exists as both `commands/gsd/*.md` and `skills/gsd-*/SKILL.md`, and each is a thin wrapper that loads a workflow.
- **Workflows** (`gsd-core/workflows/`, 89 files): the orchestrator scripts. `execute-phase.md` is 1,384 lines and `plan-phase.md` is 1,606.
- **Agents** (`agents/`, 33 roles, most also shipped as a `.compact.md` variant): researchers, synthesizer, roadmapper, planner, plan-checker, executor, verifier, debugger, code-reviewer, code-fixer, codebase-mapper, pattern-mapper, and UI, security, and docs auditors.
- **References and templates**: shared rules (`context-budget.md`, `checkpoints.md`, `tdd.md`, `questioning.md`) and artifact skeletons (`project.md`, `state.md`, `phase-prompt.md`).
- **Hooks** (28 scripts): context monitor, statusline, read/write/secret guards, commit validation.
- **`gsd-tools.cjs` CLI**: deterministic state queries and updates (`init`, `state patch`, `resolve-model`).

## Flows and phases

For a greenfield project, `/gsd-new-project` runs questioning, then four parallel researchers (stack, features, architecture, pitfalls), a synthesizer, requirements, and the roadmapper. The roadmapper writes `ROADMAP.md`, which splits a milestone into phases. For an existing codebase, `/gsd-onboard` or `/gsd-map-codebase` spawns mappers that write seven documents: STACK, INTEGRATIONS, ARCHITECTURE, STRUCTURE, CONVENTIONS, TESTING, and CONCERNS. `new-milestone`, `audit-milestone`, and `complete-milestone` manage versions. `/gsd-quick` and `/gsd-fast` skip the loop for small work.

Phases hand off through files. Discuss writes `CONTEXT.md`. Plan writes `RESEARCH.md` and the `NN-PLAN.md` files. Execute writes `SUMMARY.md` files and commits. Verify writes `VERIFICATION.md` and fix plans. Ship opens a PR and archives the phase. The docs give "Add HMAC-SHA256 signature validation middleware" as a well-sized phase and say "When in doubt, split."

## Context rot and orchestrator thinness

The docs define context rot as "the quality degradation that accumulates as an AI fills its context window," and every design choice in GSD answers it.

**What the orchestrator reads.** It loads one JSON payload from `gsd-tools.cjs init <workflow> <phase>` ("paths only to minimize orchestrator context"). `context-budget.md` sets the rules: "Never read agent definition files", "Never inline large files into subagent prompts", and, on 200k-token models, "Never read full SUMMARY.md, VERIFICATION.md, or RESEARCH.md bodies", only their frontmatter. The orchestrator "does not reason about the domain, does not write code." After it spawns an agent, it must "stop working on this task immediately. Do not read more files." The docs also set usage tiers: PEAK (0-30%), GOOD (30-50%), DEGRADING (50-70%), POOR (70%+). At POOR, the orchestrator recommends or auto-runs `/gsd-pause-work` at the next wave boundary.

**What each subagent gets.** Every executor starts in a clean context with its own `PLAN.md`, `PROJECT.md`, `STATE.md`, and the phase's `CONTEXT.md` and `RESEARCH.md`. The rule is "Pass paths only": executors read the files themselves. On models with 500k-token or larger windows, executors also receive prior-wave summaries. Isolation also cuts the other way: "anything the subagent needs must be on disk before it is spawned."

**Plan size.** "Each plan: 2-3 tasks maximum" and "Plans should complete within ~50% context (not 80%)." TDD plans target about 40%. The planner always splits a plan when it has more than 3 tasks, spans several subsystems, or has any task touching more than 5 files. Newer versions add a token `estimate` per plan, calibrated against measured history. The stated reason: quality falls as context fills, so a plan should finish before the executor reaches the degraded zone.

**What comes back.** The executor returns a short fixed block: `## PLAN COMPLETE`, plan ID, task count, SUMMARY path, commit hashes, and duration. The executor prompt says "Do NOT return the SUMMARY.md content in your response"; the orchestrator reads files from disk, not the message. The planner returns status headings such as `## PHASE SPLIT RECOMMENDED`, and the orchestrator routes on them.

**Verification without reading details.** A separate verifier subagent does the reading, and the orchestrator routes on its status (`passed`, `gaps_found`, `human_needed`). GSD admits the limit openly: "the orchestrator cannot verify semantic correctness of agent output -- only structural completeness."

**Peer communication.** None found. Agents coordinate only through `.planning/` files and the orchestrator. Parallel writers to `STATE.md` take an `O_EXCL` lockfile.

## Checkpoints and human-in-the-loop

Plans can hold `checkpoint:human-verify`, `checkpoint:decision`, and `checkpoint:human-action` tasks. The golden rule is "If Claude can run it, Claude runs it": humans judge and supply secrets, and Claude does everything else. Since #3309, human-verify checks default to one end-of-phase batch (`UAT.md`), because each mid-flight halt forces an executor cold start costing "tens of thousands of tokens." A `gate="blocking-human"` checkpoint stops even in auto mode. The executor's Rule 4 stops for architectural changes (a new table, a library switch). Discuss is the main upfront human step: the user picks which "gray areas" to decide.

## Multi-agent model

Workflows spawn agents through the runtime's Task/Agent tool. `resolve-model` assigns each agent a model tier (opus, sonnet, haiku). Researchers run four in parallel. The plan-checker runs a revision loop with the planner, "max 3 iterations", and stops early if the issue count stops falling. Executors run in parallel within a dependency wave and in sequence across waves, by default each in its own git worktree. GSD Core notes that on Claude Code, background agents cannot nest subagents, which drops wave parallelism. A beta capability moves orchestration onto the Workflow tool to work around this.

## State and handoff

Project files are `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `config.json`, and `STATE.md` ("the spine": current milestone, phase, completed plans, decisions, blockers). Each phase directory holds `CONTEXT.md`, `RESEARCH.md`, the plans and summaries, `VERIFICATION.md`, `UAT.md`, and `REVIEW.md`. `pause-work` and `resume-work` use a `continue-here` file. Debug sessions persist under `.planning/debug/`.

## How prescriptive it is

Very prescriptive, and it has grown more so. Examples:

- "**ALWAYS split if:** >3 tasks, multiple subsystems, or any task touching >5 files."
- "if you make 5+ consecutive Read/Grep/Glob calls without any Edit/Write/Bash action: STOP."
- "Never call `ScheduleWakeup` or any host wake/sleep-scheduling tool to literalize this wait (#4079)."

The philosophy files (`questioning.md`: "Don't follow a script. Follow the thread.") still trust the model. The workflows have since filled with numeric thresholds, bash blocks, and issue-number patches. Each patch fixes a real failure, but together they make procedures over 1,000 lines long that no reader, human or model, can hold at once.

## Skills relevant to us

- **TDD**: `tdd.md` says TDD is "about design quality, not coverage." TDD work gets its own plan, because red-green-refactor uses 40-50% of a context window. Tasks carry a `<behavior>` block listing tests before the `<action>`.
- **Debugging**: `gsd-debugger` investigates "using scientific method" (hypothesis testing). It keeps a debug file that survives resets and returns ROOT CAUSE FOUND or CHECKPOINT REACHED.
- **Code review**: `gsd-code-reviewer` writes `REVIEW.md` with findings graded by severity, and `--fix` hands those findings to `gsd-code-fixer`. The review covers only files changed in the phase.
- **Planning/task breakdown**: "Plans are prompts, not documents that become prompts." Tasks use XML (`<files>`, `<action>`, `<verify>`, `<done>`), and plans group into waves by dependency.
- **Briefing/questioning**: "You are a thinking partner, not an interviewer." Discuss-phase surfaces gray areas specific to the phase, not generic checklists.
- **Research**: four parallel project researchers plus a synthesizer, and a per-phase researcher that feeds the planner.
- **Architecture**: no architect role. Architecture appears in the research, the codebase-map documents, and the executor's Rule 4 escalation.
- **Verification**: goal-backward. "Task completion ≠ Goal achievement", and "Do NOT trust SUMMARY.md claims." The verifier asks what must be TRUE, what must EXIST, and what must be WIRED.
- **Git/worktrees**: one atomic commit per task. One worktree per executor, merged back by the orchestrator. Pre-commit hooks run once per wave, and `.planning/` stays out of git history.

## Ideas worth borrowing

- A thin conductor that routes on statuses and file paths and never reads bodies.
- A plan-size budget defined as a share of the executor's context, not as hours of work.
- Short, fixed return envelopes, with full detail kept on disk.
- A verifier that distrusts executor summaries and works backward from the goal.
- Batched end-of-phase human checks, with explicit never-skip gates.
- A deviation rule for executors: fix bugs and gaps inline, stop for architectural changes, and cap fix attempts at 3.
- A rule that anything a subagent needs must be on disk before it is spawned.

## Things to avoid

- Workflow files over 1,000 lines with embedded bash and issue-number patches.
- Hard numeric rules where judgment would do, such as the 5-read stop.
- 72 commands, which is too many entry points to discover. Orchestra should keep a few flows.
- Running five or more agents per phase by default; the docs themselves list cost and latency as trade-offs.
- Starting from `claude --dangerously-skip-permissions`. The full-cycle example in `docs/USER-GUIDE.md` (both repos) does this.

## Open questions

- Does the 2-3 task, 50% rule hold on 1M-token models? GSD only relaxes read depth at that size, not plan size.
- I found no published evaluation in either repo showing that the loop beats a single agent.
- The archived repo gives no reason for the move to Open GSD.
