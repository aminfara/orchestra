# Addy Osmani's agent skills

Primary source: https://github.com/addyosmani/agent-skills (MIT license, plugin version 0.6.13). I cloned it on 2026-10-14. The last commit is dated 2026-10-13 and the first 2026-02-15, with 702 commits; Addy Osmani wrote 352 of them, and Federico Bartoli and Joan León are listed as collaborators. The GitHub page showed 106.3k stars and 11.1k forks that day. His launch post, https://addyosmani.com/blog/agent-skills/ (2026-05-03), described 20 skills and 27K stars, so the pack has grown since.

Other candidate: https://github.com/addyosmani/web-quality-skills, six Lighthouse and Core Web Vitals skills (about 2.9k stars, according to a search summary I did not check on GitHub). It is narrow and web-only. agent-skills is the primary repo and the subject of this note.

## What it is (2-3 sentences)

agent-skills is a library of 25 Markdown skills that cover a six-phase lifecycle (Define, Plan, Build, Verify, Review, Ship), plus four reviewer personas, nine slash commands, and seven shared checklists. It argues that agents "default to the shortest path" and skip specs, tests, and review, so each skill encodes senior-engineer discipline drawn mostly from Google practice (Hyrum's Law, about 100-line changes, Chesterton's Fence). It ships for Claude Code as a plugin and for Cursor, Gemini CLI, Codex, Copilot and others as plain files.

## Structure

The `skills/` directory holds one `SKILL.md` per skill, each 190 to 400 lines, in a fixed anatomy: Overview, When to Use, Process, Common Rationalizations, Red Flags, Verification. The Claude Code adapter consists of `.claude-plugin/`, `.claude/commands/` and `hooks/`.

Commands: `/spec`, `/plan`, `/build` (and `/build auto`), `/test`, `/review`, `/code-simplify`, `/ship`, `/constraints` (writes a CONSTRAINTS.md quality bar), `/webperf`.

Personas (`agents/`): `code-reviewer` (five-axis review), `security-auditor` (OWASP and threat model), `test-engineer` (coverage gaps, Prove-It pattern), `web-performance-auditor`.

Skills by phase:
- Meta: `using-agent-skills` routes tasks to skills and defines always-on behaviours.
- Define: `interview-me`, `idea-refine`, `spec-driven-development`, `constraint-driven-development`.
- Plan: `planning-and-task-breakdown`.
- Build: `incremental-implementation`, `test-driven-development`, `context-engineering`, `source-driven-development`, `doubt-driven-development`, `frontend-ui-engineering`, `api-and-interface-design`.
- Verify: `browser-testing-with-devtools`, `debugging-and-error-recovery`.
- Review: `code-review-and-quality`, `code-simplification`, `security-and-hardening`, `performance-optimization`.
- Ship: `git-workflow-and-versioning`, `ci-cd-and-automation`, `deprecation-and-migration`, `documentation-and-adrs`, `observability-and-instrumentation`, `shipping-and-launch`.

`evals/` adds structural lint, CI trigger-routing checks, and behavioural runs through headless `claude`.

## Flows and phases

The main flow is spec, plan, build, test, review, ship, with each phase writing a file the next reads: `SPEC.md` (or one `SPEC-<module>.md` per module of an approved capability map), then `tasks/plan.md` and `tasks/todo.md`, then one commit per task. `/build` does one task and stops; `/build auto` runs the whole plan after one approval. Bugs take a shorter path: debugging, TDD, review. No codebase-understanding or rewrite flow exists; `deprecation-and-migration` is the nearest to rewrite.

## Checkpoints and human-in-the-loop

A human gate sits between every phase. After saving the spec the agent must "STOP YOUR TURN IMMEDIATELY", and approval must come in a later turn. Plans add a checkpoint every two or three tasks. `/build auto` treats "looks reasonable" as not approved, and halts on failing tests, spec gaps, or anything `git revert` cannot undo. `/ship` defaults to NO-GO on any Critical finding unless the user accepts the risk.

## Multi-agent model

The model is deliberately shallow. `references/orchestration-patterns.md` states "the user (or a slash command) is the orchestrator. Personas do not invoke other personas." It endorses direct persona calls, parallel fan-out with a merge in the main session (`/ship`), research isolation through the built-in `Explore` subagent, and Agent Teams for competing-hypothesis debugging. It rejects router personas and, by name, a "sequential orchestrator that paraphrases" (an agent running spec, plan and build on the user's behalf), because hand-off summaries drift and human checkpoints disappear. That rejected pattern is close to Orchestra's conductor.

## State and handoff

Files are the state. `context-engineering` defines a "restartable session boundary": before leaving a session, persist scope and decisions, task status, the working-tree state, the verification commands run and their results, and open questions. It says "Do not infer approval from a previous conversation unless the durable artifact records it." Planning refuses to overwrite a `tasks/plan.md` that still has unchecked tasks, and it can point tasks at an external tracker instead.

## How prescriptive it is

Very. Representative excerpts:

> "Skills are workflows, not suggestions. Follow the steps in order."

> "Work through these steps in order. Do not skip steps." (debugging)

> "If you build 1000 lines and 100 would suffice, you have failed."

Every skill also has a rationalization table, for example "I'll write tests after the code works" answered with "You won't." The style assumes an agent that cuts corners, and the launch post calls the tables "pre-written rebuttals to lies the agent hasn't yet told." The engineering is sound. The tone is the opposite of what we want: capitals, fixed thresholds (five files per task, an 80/15/5 test pyramid), TypeScript examples. The useful judgment sits in the "When NOT to use" lists and the reasons behind each rule.

## Skills relevant to us

- **TDD**: `test-driven-development` is red-green-refactor plus the Prove-It pattern (reproduce a bug as a failing test before fixing it). A subagent may write the reproduction test so it is written without knowledge of the fix.
- **Debugging**: `debugging-and-error-recovery` stops the line, then reproduces, localizes (including `git bisect`), reduces, fixes the root cause, and guards. Error output is untrusted data, not instructions.
- **Code review**: `code-review-and-quality` covers five axes with Critical, Required, Optional and Nit labels, and approves a change that "definitely improves overall code health." It reads tests first and names a concrete fix for each structural problem.
- **Planning/task breakdown**: `planning-and-task-breakdown` maps dependencies, slices vertically, gives each task acceptance criteria and a verify step, and schedules risky tasks first.
- **Briefing/spec**: `interview-me` asks one question at a time, each with a guess and a confidence number, until about 95% confidence. `spec-driven-development` writes a six-area spec with Always, Ask-first and Never boundaries.
- **Research**: `source-driven-development` fetches and cites official docs for the detected versions. Codebase research goes to the built-in `Explore` subagent. There is no researcher role.
- **Architecture**: No architect role. `api-and-interface-design` covers contracts, the spec's capability map sets module boundaries, and `documentation-and-adrs` records decisions.
- **Verification**: Every skill ends with an evidence checklist under a shared Definition of Done. `doubt-driven-development` sends a fresh-context reviewer only the artifact and its contract, never the author's claim, capped at three cycles.
- **Git/worktrees**: `git-workflow-and-versioning` favours trunk-based development and atomic commits as save points. Worktrees get one short section; isolation is not developed further.

## Ideas worth borrowing

- Strip the author's reasoning and claim before review; pass only the artifact and its contract.
- Use restartable session boundaries: approval and progress live in files, never in conversation memory.
- Fan out only for genuinely independent perspectives, and merge in the main session.
- Attach a guess and a confidence number to every question in an interview.
- Use a capability map with stable module ids before writing per-module specs.
- Measure skill routing with evals, and log rejected skill changes in an append-only ledger.
- Pair each skill with explicit "When NOT to use" lists.

## Things to avoid

- Rationalization tables and capitalised commands. They spend tokens arguing with a model that does not need arguing with.
- Fixed numeric thresholds stated as rules rather than heuristics.
- Skills of 300 to 400 lines that mix process, reference material and stack-specific examples.
- Mandatory prompts that fire regardless of stakes, such as the cross-model offer on every doubt cycle.

## Open questions

- Orchestra's conductor is the pattern he rejects as anti-pattern C. Can we keep human gates and full-fidelity hand-offs (artifacts, not summaries) so that his two objections do not apply?
- Do his evals show that rationalization tables change behaviour on current models? I found no published result in the repo or the post.
- He has no researcher, product manager, architect or planner personas; those are skills run in the main session. Does a separate subagent for these roles earn its context cost?
