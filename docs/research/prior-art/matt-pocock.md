# Matt Pocock's skills

- Repo: https://github.com/mattpocock/skills (verified). Plugin manifest `.claude-plugin/plugin.json` names it `mattpocock-skills`, version 1.3.1.
- License: MIT, "Copyright (c) 2026 Matt Pocock" (`LICENSE`).
- Last activity: newest commit on `main` is 2026-10-09 ("wizard: template fixes ... (#1237)"), per the commits Atom feed fetched 2026-10-14.
- Local copy: `~/.claude/skills/`, files dated 2026-08-18, lagging upstream. Upstream renamed `CONTEXT.md` to `GLOSSARY.md` (and `CONTEXT-MAP.md` to `GLOSSARY-MAP.md`), added `implement-spec`, `retro` and `pr`, and no longer lists `resolving-merge-conflicts` in `plugin.json` or the README. This note describes the local copy unless a line says "upstream".

## What it is (2-3 sentences)

A library of about 27 short Markdown skills for coding agents (Claude Code, Codex, Copilot, Gemini CLI and others). The README positions it against process-owning frameworks: "Approaches like GSD, BMAD, and Spec-Kit try to help by owning the process. But while doing so, they take away your control." Its core techniques are grilling for alignment, a domain glossary plus sparse ADRs (Architecture Decision Records), TDD (test-driven development) at agreed seams, and deep-module design.

## Structure

U = user-invoked (`disable-model-invocation: true`); M = model-invoked.

| skill | what it does | inputs | outputs/artifacts | depends on |
|---|---|---|---|---|
| grilling (M) | Interviews in rounds over a design-tree "frontier", one recommended answer per question | plan or idea | shared understanding, no file | fact-finding subagents |
| grill-me (U) | Alias | same | same | grilling |
| grill-with-docs (U) | Grilling that also writes docs | same | `CONTEXT.md`, `docs/adr/` | grilling, domain-modeling |
| domain-modeling (M) | Challenges terms, writes glossary and ADRs inline | conversation, code | `CONTEXT.md`, `docs/adr/NNNN-slug.md` | none |
| codebase-design (M) | Deep-module vocabulary; "design it twice" | module in question | 3+ alternative interfaces | none |
| research (M) | Background agent reads primary sources | question | one cited Markdown file in the repo | none |
| prototype (M) | Logic demo (one HTML file) or UI variants behind `?variant=` | design question | `prototype/<name>` branch, verdict on issue | none |
| to-spec (U) | Synthesises the conversation into a spec, no interview | conversation | tracker issue labelled `ready-for-agent` | tracker config |
| to-tickets (U) | Tracer-bullet slices with blocking edges; expand-contract for wide refactors | spec, plan or issue ref | `.scratch/<feature>/issues/NN-slug.md` or tracker issues | tracker config |
| implement (U) | Builds the work, typechecks, tests, reviews, commits | spec or tickets | commits on current branch | tdd, code-review |
| implement-spec (U, upstream) | Works the ticket graph with parallel implementer subagents | spec + tickets | integration branch, draft PR | tdd, code-review |
| tdd (M) | Red-green rules, seams, mocking guidance | behaviour to build | tests and code | codebase-design |
| diagnosing-bugs (M) | Six gated phases from feedback loop to cleanup | bug report | fix, regression test | `hitl-loop.template.sh` |
| code-review (M) | Standards and Spec reviews in parallel subagents | fixed-point git ref | two side-by-side reports | tracker config |
| triage (U) | Label state machine over issues and external PRs | tracker queue | labels, agent briefs, `.out-of-scope/*.md` | grilling, domain-modeling |
| wayfinder (U) | Map issue plus child decision tickets, one ticket per session | foggy idea or map ref | `wayfinder:map` issue, tickets | grilling, domain-modeling, research, prototype |
| improve-codebase-architecture (U) | Surveys hot spots, HTML report, grills chosen candidate | optional direction | `$TMPDIR` HTML report, glossary/ADR edits | codebase-design, grilling, domain-modeling |
| handoff (U) | Compacts the session for another agent | next focus | Markdown file in OS temp dir | none |
| to-questionnaire (U) | Questionnaire for a third person | recipient, needs | `to-questionnaire-<slug>.md` | none |
| wizard (M) | Bash script for human-only steps | procedure | script, `.env`, GitHub secrets | `template.sh` |
| resolving-merge-conflicts (M, local) | Resolves hunks by intent, runs checks, finishes | in-progress conflict | commit | none |
| ask-matt (U) | Router over flows | situation | advice | none |
| setup-matt-pocock-skills (U) | Configures tracker, labels, doc layout | repo | `docs/agents/*.md`, CLAUDE.md block | none |
| teach, wait-what, writing-for-agents | Learning workspace; plain-English re-pitch; style guide for agent docs | varies | varies | none |
| retro, pr (upstream) | Environment retrospective; PR body template | session; diff | suggestions; PR body | writing-for-agents |

## Flows and phases

`ask-matt/SKILL.md` documents the flows. Main flow: `grill-with-docs`, an optional `handoff` → `prototype` → `handoff` detour, then `to-spec` → `to-tickets` → `implement` per ticket (with `/clear` between tickets) for multi-session work, or `implement` inline for small work. Upstream adds `implement-spec` as the whole-spec alternative, then `pr` and `retro`. On-ramps: `triage` feeds `implement`; `wayfinder` hands off at `to-spec`; `diagnosing-bugs` hands a "no good seam" finding to `improve-codebase-architecture`, whose candidates enter at `grill-with-docs`.

The only hard-wired chaining is explicit Skill-tool calls: implement calls tdd and code-review; grill-with-docs, triage, wayfinder and improve-codebase-architecture call grilling plus domain-modeling; tdd calls codebase-design. Everything else is a human typing the next command, per the README rule "A user-invoked skill may invoke model-invoked skills, but never another user-invoked one." ask-matt also says to keep grilling through `to-tickets` in one context window, inside a ~150k-token "smart zone".

## Checkpoints and human-in-the-loop

Most gates sit in planning. Grilling waits after each round and does not act "until the user confirms you have reached a shared understanding". to-spec checks test seams with the user; to-tickets iterates "until the user approves the breakdown"; tdd confirms seams before any test; triage recommends, then waits; wizard confirms irreversible steps. diagnosing-bugs shows ranked hypotheses but says "Don't block on it". Wayfinder labels tickets HITL (human in the loop) or AFK (away from keyboard); the `ready-for-agent` / `ready-for-human` labels encode the same split.

## Multi-agent model

Subagents are ad hoc prompts, not named roles. grilling dispatches non-blocking fact-finding subagents; research runs as a background agent; code-review runs Standards and Spec subagents in parallel and never reranks across them; codebase-design spawns 3+ subagents with different constraints (minimal interface, maximum flexibility, common caller, ports and adapters); improve-codebase-architecture uses an exploration subagent; wayfinder fires parallel research subagents. Upstream implement-spec is closest to Orchestra: an exploration subagent saves notes outside the repo, background implementer subagents each get a worktree, a merger subagent lands each on the integration branch, and communication stays "sparse", through context pointers.

## State and handoff

- `CONTEXT.md` (upstream `GLOSSARY.md`): glossary only, created lazily; `CONTEXT-MAP.md` for multi-context repos.
- `docs/adr/0001-slug.md`: one paragraph minimum, offered only when a decision is hard to reverse, surprising, and a real trade-off.
- Tickets: local `.scratch/<feature>/spec.md` and `issues/NN-slug.md` with a `Status:` line, or GitHub (`gh`) / GitLab (`glab`) issues with native blocking links.
- `.out-of-scope/<concept>.md`: rejected enhancements, checked during triage.
- Wayfinder: `wayfinder:map` issue, `wayfinder:<type>` child tickets, claim by assignment.
- Handoff doc in the OS temp dir with a "suggested skills" section; prototype and research live on throwaway branches.

setup-matt-pocock-skills writes `docs/agents/issue-tracker.md` (GitHub, GitLab, local, or a freeform paragraph for Jira/Linear, plus "Wayfinding operations" and an external-PR flag defaulted off), `docs/agents/triage-labels.md` (only if triage is installed), `docs/agents/domain.md` (read glossary and ADRs; "proceed silently" if absent), and an `## Agent skills` block in CLAUDE.md or AGENTS.md. Skills that lack config tell the user to run setup; wayfinder defaults to local markdown.

## How prescriptive it is

- tdd: "No test is written at an unconfirmed seam."
- diagnosing-bugs: "No red-capable command, no Phase 2."
- resolving-merge-conflicts: "Always resolve; never `--abort`."

Each skill is strict inside its scope: hard completion criteria, phase gates, and policed vocabulary (codebase-design bans "component", "service" and "boundary"). Across skills it is loose by design; no skill owns the end-to-end process, and implement is six lines. That suits a human driver and leaves orchestration to us.

## Skills relevant to us

- **TDD:** tdd. Pure reference plus one interactive step (seam confirmation).
- **Debugging:** diagnosing-bugs. The strongest skill here; mostly AFK.
- **Code review:** code-review. Two axes plus a 12-smell Fowler baseline.
- **Planning/task breakdown:** to-spec, to-tickets, wayfinder; upstream implement-spec for graph execution.
- **Briefing/grilling:** grilling, grill-with-docs, triage's `AGENT-BRIEF.md`, to-questionnaire.
- **Research:** research. Three steps; thin.
- **Architecture:** codebase-design, improve-codebase-architecture, domain-modeling ADRs.
- **Verification:** no dedicated skill. Pieces exist in diagnosing-bugs Phase 6, implement's test cadence, code-review's Spec axis, and upstream pr's before/after "Evidence".
- **Git/worktrees:** resolving-merge-conflicts (local only); upstream implement-spec's worktree-per-ticket; prototype branches.

## Fit as Orchestra companions

A role subagent could preload these as-is: tdd (engineer, tester; supply seams in the brief), diagnosing-bugs (engineer in debug), codebase-design (architect), domain-modeling's formats, code-review (reviewer), resolving-merge-conflicts, wizard. code-review and research spawn their own agents.

These need the main session because they are interactive: grilling, grill-with-docs, to-spec, to-tickets, triage, wayfinder, improve-codebase-architecture, prototype, to-questionnaire, setup. User-invoked skills are "reachable only when you type them" (README), so the conductor cannot call to-spec, to-tickets or implement through the Skill tool.

These duplicate or conflict with Orchestra: ask-matt (a router, the conductor's job), implement and implement-spec (the engineer loop; implement commits and runs code-review itself), handoff (Orchestra keeps its own state), and wayfinder (a competing multi-session plan store on the tracker).

## Ideas worth borrowing

- Frontier-based question rounds with a recommended answer each; facts are the agent's job, decisions the user's.
- Two review axes in separate contexts, reported side by side.
- Tracer-bullet tickets with blocking edges, a "frontier" of ready work, and expand-contract for wide refactors.
- A "red-capable" feedback loop as the gate before any debugging hypothesis; tagged `[DEBUG-xxxx]` logs.
- Agent briefs that are behavioural, path-free, with acceptance criteria and an out-of-scope list.
- The phase-boundary tree: continue, clear, handoff, subagent, compact, in that order.
- One config file per concern under `docs/agents/`, pointed to from CLAUDE.md; `.out-of-scope/` as rejection memory.

## Things to avoid

- Coupling to upstream names: the glossary file was renamed and a skill disappeared within two months. Vendor or pin.
- GitHub-first assumptions. Jira gets a freeform paragraph, and wayfinder leans on GitHub sub-issues and native dependencies.
- Relying on user-invoked skills for automated steps.
- Unannounced side effects from companions: implement commits, to-spec and triage write to the tracker, improve-codebase-architecture opens a browser.
- Stacked fan-out cost: conductor → reviewer → code-review's two subagents.

## Open questions

- Can role subagents in our harness spawn nested subagents, as code-review, research and codebase-design expect?
- Pin the local 2026-08-18 copy or upstream 1.3.1 (`GLOSSARY.md`)?
- Where did resolving-merge-conflicts go upstream? A scrape of `skills/deprecated` returned nothing; unverified.
- Does tdd accept seams pre-agreed in a spec with no live user? implement implies yes ("at pre-agreed seams"); tdd itself says "confirm them with the user".
- How would our Jira setup express blocking edges and wayfinding operations in `docs/agents/issue-tracker.md`?
