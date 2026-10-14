# Superpowers

- Source: https://github.com/obra/superpowers, read from a clone of `main` at `bb92a77` (v7.0.0)
- Author: Jesse Vincent (named in `.claude-plugin/plugin.json`) and Prime Radiant (README)
- License: MIT
- Activity: first commit 2025-10-09; latest commit 2026-10-09 (v7.0.0); 684 commits
- Adoption: the GitHub page showed about 299k stars and 26.7k forks on 2026-10-14; I could not cross-check this through the API

## What it is (2-3 sentences)

Superpowers calls itself "a complete software development methodology for your coding agents, built on top of a set of composable skills." It is a library of 15 skills plus a SessionStart hook that forces the agent to check for and invoke a skill before acting. The core path is brainstorm, worktree, plan, execute with subagents, review, then finish the branch.

## Structure

It ships as one plugin for roughly 17 harnesses (Claude Code, Codex, Cursor, Gemini CLI, others), each with its own manifest directory. The current release has no `agents/` and no `commands/` directory. Per the release notes, `agents/code-reviewer.md` became a prompt template inside a skill, and the `/brainstorm`, `/write-plan` and `/execute-plan` commands were deprecated and then removed. Every subagent is now a `general-purpose` dispatch filled from a markdown template. The one hook, `hooks/session-start`, fires on startup, clear and compact, and injects the full `using-superpowers` skill wrapped in `<EXTREMELY_IMPORTANT>`.

The 15 skills (those covered under "Skills relevant to us" get detail there):

- **using-superpowers**: the bootstrap; invoke any skill with even a 1% chance of applying.
- **brainstorming**, **writing-plans**, **using-git-worktrees**, **test-driven-development**, **systematic-debugging**, **verification-before-completion**, **requesting-code-review**, **receiving-code-review**: see below.
- **subagent-driven-development (SDD)**: a fresh implementer subagent per task, a reviewer after each, a final branch review.
- **executing-plans**: run the plan inline, with one review at the end.
- **dispatching-parallel-agents**: one agent per independent problem domain.
- **finishing-a-development-branch**: verify tests, then merge, open a PR, keep, or discard.
- **writing-skills**: TDD applied to skill authoring.
- **diagnosing-superpowers**: analyse a session transcript to find where the skills misfired.

## Flows and phases

There is one main flow: brainstorming, using-git-worktrees, writing-plans, SDD or executing-plans, then finishing-a-development-branch, with TDD and code review inside execution. Debugging is a separate entry point ("Fix this bug" routes to systematic-debugging). Each phase hands off by naming the next skill: brainstorming's gate says "invoke superpowers:writing-plans and no other skill", and every plan header names SDD as a "REQUIRED SUB-SKILL". Brainstorming sizes the work first: a quick task is done on the spot, a small change is agreed in chat, and only a project gets a design doc and a plan.

## Checkpoints and human-in-the-loop

The user approves the work at three points:

1. Brainstorming's `<HARD-GATE>` blocks all building until the user approves the description, in chat or as the design doc. A "builder check" subagent reads the doc first, producing one round of questions only the user can answer.
2. After writing-plans, the user reviews the plan and picks subagent-driven or native execution, given a one-sentence recommendation.
3. Finishing offers merge, PR, keep or discard; discarding requires typing `discard`.

Execution is deliberately non-stop: "Do not pause to check in with your human partner between tasks." Four things stop it: irreversible operations, security-sensitive actions, side effects outside the worktree, and a plan so broken that every path is a guess. The agent decides everything else as a logged "Ruling" and lists all rulings at the end.

## Multi-agent model

Subagents do the work. The SDD controller dispatches one implementer per task, which returns one of four statuses: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED. A task reviewer then returns two verdicts, spec compliance and code quality. Context travels as files: a script extracts the task into a brief, and another builds a "review package" with the commit list, diff stat and full diff. Dispatch prompts must not carry session history; the skill cites one real dispatch of 42k characters, 99% of it pasted history. Subagents may not spawn subagents, and the reviewer prompt says "Do Not Trust the Report". Fix loops stop at five rounds: rounds 1 to 3 resume the implementer, rounds 4 and 5 use a fresh, more capable model. Every dispatch names its model tier, with the most capable reserved for the final review. Only one implementer runs at a time.

## State and handoff

- Design docs go to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` and are committed.
- Plans go to `docs/superpowers/plans/YYYY-MM-DD-<feature>.md`, using checkbox steps.
- Each plan gets a git-ignored workspace under `.superpowers/sdd/` holding a `progress.md` ledger, task briefs, reports and review packages. The ledger exists because memory does not survive compaction. The skill calls re-dispatching completed tasks "the single most expensive failure observed."
- Git commits act as the durable record; the workspace is deleted after the final review.

## How prescriptive it is

The discipline skills are very rigid. Process skills became softer in v7.

> "If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill." (using-superpowers)

> "Write code before the test? Delete it. Start over." (test-driven-development)

> "Ground to cover. This is territory, not a script. Never read these out as questions." (brainstorming, v7)

Most skills combine Iron Laws, Graphviz flowcharts and "rationalization" tables. `writing-skills/persuasion-principles.md` recommends authority and commitment techniques ("YOU MUST", forced announcements), citing Meincke et al. (2025). A 2026-06-10 design spec in the repo reports tests in which prohibitions on how to compose output backfired while positive recipes worked. My judgment: it is prescriptive by design and tuned for compliance, but the v7 brainstorming rewrite moves toward the guideline style we want.

## Skills relevant to us

- **TDD**: Strict red-green-refactor; you must watch the test fail, and code written before its test gets deleted.
- **Debugging**: Four phases, starting with root-cause investigation that includes per-component instrumentation. After three failed fixes the agent must stop and question the architecture with the user.
- **Code review**: The reviewer gets a diff file and the requirements, never session history, and reports by severity. Receiving-code-review bans performative agreement and requires verifying each item first.
- **Planning/task breakdown**: A plan is "the set of decisions the implementer cannot make alone": exact files, signatures, test assertions and an Interfaces block per task. A plan longer than the code "has written the code instead."
- **Brainstorming/briefing**: One open question per message, playback in 200 to 300 word chunks, explicit sizing, and a builder-check subagent that tests whether the doc is plannable.
- **Research**: No dedicated skill. Brainstorming offers recon (codebase, files, web) and lets the user decide.
- **Architecture**: No dedicated skill. Writing-plans has a "File Structure" step, and SDD routes architecture tasks to the most capable model.
- **Verification**: An "Iron Law" that makes every completion claim name a command, run it fresh and read the output. An agent's success report is not evidence.
- **Git/worktrees**: Detect existing isolation, prefer native harness tools, fall back to `git worktree` with a gitignore check, and finish with four explicit options.

## Ideas worth borrowing

- Pass context to subagents as files (brief, report, diff package) rather than pasting it into the prompt.
- A ledger per plan that survives compaction and lets a run resume.
- "Rulings, not stalls": make the call, log what it costs if wrong, and surface every ruling at the end.
- A builder-check subagent that pressure-tests a design doc before the user sees it.
- Sizing work before choosing a ceremony level.
- Explicit model tiers per role, and changing something on escalation rather than retrying.
- Testing skills against baseline agent behaviour, and measuring phrasing choices.

## Things to avoid

- A bootstrap that demands skill invocation before every response. It costs tokens and fights our trust-the-model goal.
- Persuasion-psychology framing and shouted Iron Laws as the default tone.
- Long skills: SDD runs about 4,900 words, and the repo itself notes that Codex re-reads SKILL.md about 500 times per session.
- Strict serial implementation where tasks are actually independent.
- Having one main flow only. We need understand-codebase, rewrite and debug as peer flows.

## Open questions

- I did not read the eval harness (`prime-radiant-inc/superpowers-evals`), so I cannot say how well behaviour claims are measured.
- I did not read `2026-07-06-sdd-plan-scoped-workspace-eval-results.md`, so I do not know whether per-task review beats native execution on quality.
- No skill covers research, architecture, or product management roles; I found nothing about why.
- I could not verify the star count outside the GitHub web page.
