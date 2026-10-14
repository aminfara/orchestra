# Other frameworks

Six frameworks matter most for Orchestra: GitHub Spec Kit, BMAD-METHOD, Kiro specs, OpenSpec, wshobson/agents (its `conductor` and `full-stack-orchestration` plugins), and Anthropic's `feature-dev` plugin. All six put a written spec or plan in front of code and gate it on human review. They differ most on how rigidly they sequence phases. Sources were fetched on 2026-10-14; star counts are as shown on the GitHub pages that day. The GitHub API was rate-limited, so licenses come from the repo pages.

Ruflo (formerly claude-flow, github.com/ruvnet/claude-flow, 74.6k stars, MIT) was checked and left out of the detailed review. It is a swarm runtime ("Hierarchical, mesh, and adaptive topologies with consensus", "314 MCP tools") rather than a set of guideline skills, which is the opposite of Orchestra's design. Anthropic's `anthropics/skills` (181k stars, mostly Apache 2.0, document skills source-available) is the reference for the SKILL.md format but contains no software-engineering flow.

## Comparison table

| framework | source URL | license | packaging | roles/agents | flows | human gates | state artifacts | prescriptiveness |
|---|---|---|---|---|---|---|---|---|
| GitHub Spec Kit (141.2k stars) | github.com/github/spec-kit | MIT | `specify` Python CLI (uv) that installs slash commands into many agents | none; one agent runs each command | constitution, specify, plan, tasks, implement, converge; opt-in bug and assess extensions | review after every command | `memory/constitution.md` (path per spec-driven.md), `specs/<branch>/spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `tasks.md` | high |
| BMAD-METHOD (54.1k stars) | github.com/bmad-code-org/BMAD-METHOD | MIT | npm installer (v6.12 stable); skills CLI or Claude Code/Codex marketplace (v7 alpha) | Analyst, PM, Architect, Developer, UX Designer personas | Clarify, Plan, Build and verify, Learn and adjust; entry point scales by size | approve plan, review result, story checkpoints | `_bmad-output/` with `prd-*.md`, `architecture-*.md`, `tickets.toml`, `plan-*.md`, `deferred-work.md` | medium (v7), high (v6) |
| Kiro specs | kiro.dev/docs/specs | proprietary IDE; kirodotdev/Kiro (4.4k stars) is an issue tracker only | built into Kiro IDE | none named | Requirements-First, Design-First, Bugfix, Quick Spec | review between phases (skipped in Quick Spec) | `.kiro/specs/*/requirements.md`, `design.md`, `tasks.md`; `.kiro/steering/*.md` | medium |
| OpenSpec (71.9k stars) | github.com/Fission-AI/OpenSpec | MIT | npm CLI that installs `/opsx:*` commands | none | explore, propose, apply, verify, sync, archive | review change folder before apply | `openspec/specs/`, `openspec/changes/<name>/{proposal,design,tasks}.md` plus delta specs | low to medium |
| wshobson/agents (40.6k stars) | github.com/wshobson/agents | MIT (conductor plugin Apache 2.0) | Claude Code marketplace, adapters for Codex, Cursor, others | 202 agents across 94 plugins | per plugin; e.g. 9-step full-stack feature, conductor tracks | two checkpoints (full-stack); plan review (conductor) | `.full-stack-feature/state.json` and `01-...09-*.md`; `conductor/` tree | high |
| Anthropic feature-dev | github.com/anthropics/claude-code/tree/main/plugins/feature-dev | not shown on page | Claude Code plugin | code-explorer, code-architect, code-reviewer | 7 phases, one flow | 5 interaction points | none; in-session todos only | medium |

## Per framework

### GitHub Spec Kit

Spec Kit is a Python CLI that installs Spec-Driven Development (SDD) commands into a coding agent. The flow is `/speckit-constitution`, `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement`, then `/speckit-converge`, repeated until it reports "Converged." Clarify, analyze, and checklist are optional quality gates, and bug-fix and idea-assessment flows ship as extensions. There are no roles: one agent runs each command, and the user reviews output before running the next. State lives entirely in files. `specify` creates a branch and `specs/<branch>/spec.md`; `plan` adds `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`; `tasks` writes `tasks.md` with `[P]` markers for parallel work. Command frontmatter declares `handoffs` to the next command.

The instruction style is template-driven and strict. The specify template says "LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total", and the default constitution declares test-first "NON-NEGOTIABLE".

Worth borrowing: a project constitution that every phase checks against, explicit `[NEEDS CLARIFICATION]` markers instead of silent guessing, the plan/research/contracts split, and handoff metadata between steps. Avoid: hard-coded architectural doctrine (Article I's "Every feature... MUST begin its existence as a standalone library") and a long chain of user-invoked commands that makes the human the scheduler.

### BMAD-METHOD

BMAD ("Breakthrough Method for Agile Ai Driven Development") is the most role-heavy framework here. Version 7 (alpha) ships persona agents (Analyst Mary, PM John, Architect Winston, Developer Amelia, UX Designer Sally) plus workflow skills such as `bmad-prd`, `bmad-spec`, `bmad-architecture`, `bmad-ticket`, `bmad-build`, `bmad-code-review`, and `bmad-retrospective`. The docs frame everything as one loop (Clarify, Plan, Build and verify, Learn and adjust) and pick the entry point by size: trivial, one session, epic-sized, project-sized ("roughly 20+ sessions").

`bmad-build` resolves intent from evidence, writes a light or full plan, and stops for "Approve the plan when it describes the right thing to build." It then implements and runs three independent reviewer lenses (Blind Hunter, Edge Cases Hunter, Verification Gap Finder), triaging findings into fix, defer to `deferred-work.md`, or send back to the plan layer. Artifacts sit in `_bmad-output/` initiative folders, with `tickets.toml` ordering stories. The docs tell users to start a fresh chat per workflow.

Worth borrowing: size-based routing into one loop, gaps as open questions on the plan rather than an upfront interview, the three-way review triage, and party mode's lesson that "One model voicing five personas tends to make them agree" (so spawn real subagents when independence matters). Avoid: named personas with menu codes, and frequent breaking changes in the v7 alpha.

### Kiro specs

Kiro is an AWS IDE whose specs turn a request into three files: `requirements.md` (or `bugfix.md`), `design.md`, and `tasks.md`. "All specs follow a three-phase workflow." Feature specs come in Requirements-First and Design-First variants; bugfix specs record current, expected, and unchanged behavior to prevent regressions. Requirements use EARS (Easy Approach to Requirements Syntax): "WHEN [condition/event] THE SYSTEM SHALL [expected behavior]". Standard specs pause for review between phases; Quick Spec generates all three "without approval gates." Running all tasks builds a dependency graph and executes independent tasks in concurrent waves. Specs do not update automatically; the user triggers Sync Files.

Kiro has no roles. Persistent context comes from steering files in `.kiro/steering/` (`product.md`, `tech.md`, `structure.md`) loaded always, by file glob, manually, or by description match.

Worth borrowing: the "unchanged behavior" section for bug fixes, a Quick Spec escape hatch for well-understood work, wave-based parallel task execution, and conditional steering. Avoid: tying the workflow to a single IDE, and EARS as a mandatory format for every requirement.

### OpenSpec

OpenSpec (npm `@fission-ai/openspec`) keeps live specs in `openspec/specs/` and each in-flight change in `openspec/changes/<name>/` with `proposal.md`, delta specs (`## ADDED Requirements`, `## REMOVED`), `design.md`, and `tasks.md`. `/opsx:archive` merges deltas into the live specs, so the spec tree describes the current system rather than a history of requests. The current OPSX workflow models artifacts as a dependency graph detected from files on disk; `/opsx:continue` builds the next ready artifact and `/opsx:ff` builds them all. Its stated philosophy is "fluid not rigid", "built for brownfield not just greenfield", and "Dependencies are **enablers**, not gates." The human gate is reviewing the change folder before `/opsx:apply`. There are no roles.

Worth borrowing: deltas against a living spec (a good fit for add-feature and rewrite), state derived from which files exist, and the explicit stance that dependencies enable rather than force sequence. Avoid: little guidance on review or testing, and no role separation.

### wshobson/agents

This marketplace holds 94 plugins with "202 agents, 184 skills, and 105 commands", maintained in Claude Code plugin format with adapters for other harnesses and per-agent model aliases (opus, sonnet, haiku, inherit). Two plugins overlap with Orchestra. `full-stack-orchestration` runs nine steps in three phases: requirements questions asked one at a time, database and architecture design, Checkpoint 1, implementation, parallel test, security, and performance agents, Checkpoint 2, then deployment and docs. It writes `state.json` and numbered step files that "Later steps read... rather than relying on memory," and offers resume-or-restart. `conductor`, adapted from Google's Conductor for Gemini CLI, enforces "Context → Spec & Plan → Implement" with a `conductor/` tree (`product.md`, `tech-stack.md`, `workflow.md`, `tracks.md`, per-track `spec.md` and `plan.md`) and git-aware revert per track, phase, or task.

The instruction style is procedural: "Execute steps in order. Do NOT skip ahead, reorder, or merge steps."

Worth borrowing: numbered step files plus a small `state.json` for resume, parallel specialist review, revert by unit of work, and model tiering per role. Avoid: the catalog sprawl and the step-locked style that Orchestra is explicitly rejecting.

### Anthropic feature-dev

`feature-dev` is a single `/feature-dev` command with seven phases: Discovery, Codebase Exploration, Clarifying Questions, Architecture Design, Implementation, Quality Review, Summary. It launches 2 to 3 parallel `code-explorer` agents to trace execution paths and return essential files, which the main session then reads itself. It launches 2 to 3 `code-architect` agents with different briefs (minimal changes, clean architecture, pragmatic balance) and asks the user to choose, waits for explicit approval before implementing, and runs three `code-reviewer` agents (simplicity, bugs, conventions) before offering "Fix now", "Fix later", or "Proceed as-is". It keeps no files; progress lives in TodoWrite.

The instruction style is short and directive. The architect agent says "Make confident architectural choices rather than presenting multiple options," so diversity comes from the conductor's differing briefs, not from each agent hedging.

Worth borrowing: almost all of it as the add-feature baseline, especially the explorer-returns-file-list pattern, divergent briefs for parallel architects, and the three-option review gate. Avoid: no persisted state, so a long feature cannot resume across sessions. The README also contradicts itself on the reviewer confidence threshold (80 versus 50 to 74 bands).

## Cross-cutting patterns

Every framework agrees that a written specification precedes code and that a human reviews it before implementation. Every one except feature-dev persists that spec, plan, and task list as Markdown in the repo, so files are the handoff between phases and sessions, not chat memory. Most separate what and why (requirements) from how (design) and from sequencing (tasks), and most mark parallelizable tasks. Several keep standing project context apart from per-change specs: Spec Kit's constitution, Kiro's steering, conductor's `product.md` and `tech-stack.md`, BMAD's project context. Review by several independent lenses run in parallel appears in BMAD, wshobson, and feature-dev.

They diverge on four things. On sequencing, Spec Kit and wshobson lock steps, Kiro gates by default with an opt-out, and OpenSpec and BMAD v7 treat phases as a loop or graph. On roles, BMAD uses named personas, feature-dev and wshobson use narrow functional subagents, and Spec Kit, Kiro, and OpenSpec have none. On spec lifetime, OpenSpec merges deltas into a living spec while the others leave per-change specs behind. On scaling, BMAD and Kiro size process to the work explicitly, while Spec Kit and full-stack-orchestration run the same chain regardless.

For Orchestra, the closest fit is feature-dev's subagent shape plus OpenSpec's fluid artifact graph, BMAD's size routing and review triage, and wshobson's resumable state file.

## Open questions

- Should Orchestra keep a living spec that changes merge into (OpenSpec) or per-flow artifacts only (feature-dev, Spec Kit)?
- Does a role need a persona, or only a brief and a tool set? BMAD's finding that inline personas converge suggests real subagents for any role whose independence matters (reviewer, architect alternatives).
- How many user gates per flow before the human becomes the scheduler? feature-dev uses five; Kiro and BMAD offer a quick path with fewer.
- Should Orchestra adopt a constitution or steering file, or rely on the repo's existing CLAUDE.md?
- What is the resume mechanism: a `state.json`, or inferring state from which artifacts exist (OpenSpec)?
- Not found: any published evaluation comparing these frameworks' outcomes; claims of effectiveness in all six are the authors' own.
